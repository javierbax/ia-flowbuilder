import os
import json
import re
from services.gancho.models import GanchoOutput

from core.client import client
from core.utils import detect_language
import uuid
import time
from core.supabase_client import supabase


def generar_hooks(tema: str, formato: str) -> GanchoOutput:
    idioma = detect_language(tema)

    prompt = f"""
You are a viral content strategist. Based on this topic: "{tema}" and format: "{formato}", generate content hooks.

Respond in this JSON format:
{{
  "hooks": ["", "", ""],
  "titulo": "",
  "caption": "",
  "asunto_email": ""
}}

If the topic is in Spanish, respond in Spanish. If it's in English, respond in English.
"""

    start = time.time()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=500
    )

    duration = int((time.time() - start) * 1000)
    content = response.choices[0].message.content.strip()

    # Clean markdown-style JSON
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", content, re.DOTALL)
    if match:
        content = match.group(1)

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        parsed = {
            "hooks": [],
            "titulo": "",
            "caption": "",
            "asunto_email": ""
        }

    # Ensure all fields exist
    result = {
        "hooks": parsed.get("hooks", []),
        "titulo": parsed.get("titulo", ""),
        "caption": parsed.get("caption", ""),
        "asunto_email": parsed.get("asunto_email", "")
    }

    # Save usage log
    usage = response.usage.model_dump() if hasattr(response.usage, "model_dump") else response.usage
    supabase.table("usage_logs").insert({
        "microservice": "gancho-express",
        "prompt_tokens": usage["prompt_tokens"],
        "completion_tokens": usage["completion_tokens"],
        "total_tokens": usage["total_tokens"],
        "duration_ms": duration
    }).execute()

    return GanchoOutput(**result)
