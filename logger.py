# logger.py
import os
import sys
import threading
import queue
import signal
import time
import socket
import contextvars
import traceback
from typing import Any, Dict, Optional, List


import picologging
from picologging.handlers import RotatingFileHandler


# --- Context vars (MDC) ---
_log_context: contextvars.ContextVar[Dict[str, Any]] = contextvars.ContextVar("log_context", default={})


def bind_context(**values: Any) -> None:
   ctx = dict(_log_context.get())
   ctx.update(values)
   _log_context.set(ctx)


def clear_context() -> None:
   _log_context.set({})


# --- JSON serialization ---
try:
   import orjson
   def _dumps(obj: Any) -> str:
       return orjson.dumps(obj, option=orjson.OPT_UTC_Z).decode()
except ImportError:
   import json
   def _dumps(obj: Any) -> str:
       return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


# --- JSON Formatter ---
class JsonFormatter(picologging.Formatter):
   def __init__(self, *, include_context: bool = True, static_fields: Optional[Dict[str, Any]] = None):
       super().__init__()
       self.include_context = include_context
       self.static_fields = static_fields or {}
       self.hostname = socket.gethostname()
       self.pid = os.getpid()


   def format(self, record: picologging.LogRecord) -> str:
       ts = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(record.created))
       ts = f"{ts}.{int(record.msecs):03d}Z"
       base = {
           "timestamp": ts,
           "level": record.levelname,
           "logger": record.name,
           "message": record.getMessage(),
           "file": f"{record.filename}:{record.lineno}",
           "func": record.funcName,
           "process": self.pid,
           "thread": record.threadName,
           "hostname": self.hostname,
       }
       if record.exc_info:
           base["exception"] = "".join(traceback.format_exception(*record.exc_info))
       if self.include_context:
           base.update(_log_context.get())
       if hasattr(record, "extra_data"):
           base.update(record.extra_data)
       if self.static_fields:
           base.update(self.static_fields)
       return _dumps(base)


# --- Async queue + worker ---
class DropCounter:
   def __init__(self): self.dropped=0; self.lock=threading.Lock()
   def increment(self):
       with self.lock: self.dropped+=1
   def snapshot(self):
       with self.lock: return self.dropped


class AsyncQueueHandler(picologging.Handler):
   def __init__(self, q: queue.Queue, drop_counter: DropCounter):
       super().__init__(); self.q=q; self.drop_counter=drop_counter
   def emit(self, record):
       try: self.q.put_nowait(record)
       except queue.Full: self.drop_counter.increment()


class BatchWorker(threading.Thread):
   def __init__(self, q: queue.Queue, stop: threading.Event, sinks: List, fmt: JsonFormatter, batch_size=512, flush_interval=0.25, drop_counter=None):
       super().__init__(daemon=True)
       self.q, self.stop, self.sinks, self.fmt, self.batch, self.flush, self.dc = q, stop, sinks, fmt, batch_size, flush_interval, drop_counter
       self.buf=[]; self.last=time.monotonic()
   def run(self):
       while not (self.stop.is_set() and self.q.empty()):
           try: rec=self.q.get(timeout=self.flush); self.buf.append(self.fmt.format(rec)); self.q.task_done()
           except queue.Empty: pass
           if self.buf and (len(self.buf)>=self.batch or time.monotonic()-self.last>=self.flush):
               for s in self.sinks: s.write_many(self.buf)
               self.buf.clear(); self.last=time.monotonic()


class StdoutSink:
   def write_many(self, lines):
       for l in lines: sys.stdout.write(l+"\n")


class RotatingFileSink:
   def __init__(self, path, fmt, max_bytes=128*1024*1024, backups=3):
       self.h=RotatingFileHandler(path,maxBytes=max_bytes,backupCount=backups); self.h.setFormatter(fmt)
   def write_many(self, lines):
       for l in lines: self.h.stream.write(l+"\n"); self.h.flush()


# --- Setup / Global logger factory ---
_worker=None; _stop=None
def setup_logging(level=picologging.INFO, logfile="app.log", use_stdout=True, static_fields=None):
   global _worker,_stop
   q=queue.Queue(maxsize=10000); dc=DropCounter()
   fmt=JsonFormatter(static_fields=static_fields)
   sinks=[];
   if use_stdout: sinks.append(StdoutSink())
   if logfile: sinks.append(RotatingFileSink(logfile, fmt))
   root=picologging.getLogger(); root.setLevel(level)
   for h in list(root.handlers): root.removeHandler(h)
   root.addHandler(AsyncQueueHandler(q,dc))
   _stop=threading.Event()
   _worker=BatchWorker(q,_stop,sinks,fmt); _worker.start()


   def _grace(sig,frm): shutdown_logging()
   try: signal.signal(signal.SIGINT,_grace); signal.signal(signal.SIGTERM,_grace)
   except Exception: pass


def shutdown_logging(timeout=10.0):
   global _worker,_stop
   if not _worker: return
   start=time.monotonic()
   while not _worker.q.empty() and (time.monotonic()-start)<timeout: time.sleep(0.05)
   _stop.set(); _worker.join(timeout)


def get_logger(name:str)->picologging.Logger:
   return picologging.getLogger(name)