from krivisio_tools.report_generation.app.utils.doc_formatter import

# From raw text
print(extract_text("Hello, world!", "text"))

# From a PDF file
print(extract_text("docs/sample.pdf", "pdf"))

# From DOCX
print(extract_text("docs/report.docx", "docx"))

# From TXT
print(extract_text("docs/notes.txt", "txt"))
