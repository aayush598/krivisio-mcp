"""
LLM Client Utility - Handles communication with OpenAI's Chat API.
Includes preprocessing for prompt outputs.
"""

import re
from typing import List, Dict, Optional
from openai import OpenAI
from krivisio_tools.report_generation.app.core.config import KRVISIO_SIDE_TOOLS

# Initialize OpenAI client once
client = OpenAI(api_key=KRVISIO_SIDE_TOOLS)


def strip_code_fences(text: str) -> str:
    """
    Removes Markdown code fences (``` and language tags like ```json, ```python).
    
    Args:
        text (str): Text containing code blocks.
    
    Returns:
        str: Cleaned text without code fences.
    """
    pattern = r"```(?:json|python|markdown|sh|text)?\s*([\s\S]*?)```"
    return re.sub(pattern, lambda m: m.group(1).strip(), text, flags=re.IGNORECASE)


def chat_with_llm(
    prompt: str,
    model: str = "gpt-4o",
    temperature: float = 0.7,
    max_tokens: int = 800,
    frequency_penalty: float = 0.3,
    presence_penalty: float = 0.2,
    conversation_history: Optional[List[Dict[str, str]]] = None
) -> str:
    """
    Sends a prompt to OpenAI's chat model and returns the cleaned response.
    
    Args:
        prompt (str): User input to the model.
        model (str): LLM model name. Default is "gpt-4o".
        temperature (float): Sampling temperature.
        max_tokens (int): Max number of tokens in the response.
        frequency_penalty (float): Discourage repetition.
        presence_penalty (float): Encourage new topic introductions.
        conversation_history (Optional[List[Dict]]): If provided, used to add past context.
    
    Returns:
        str: Cleaned response from the LLM.
    """
    messages = conversation_history[-8:] if conversation_history else []
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )

    raw_response = response.choices[0].message.content.strip()
    return strip_code_fences(raw_response)
