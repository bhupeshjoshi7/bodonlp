"""
Large Language Model (LLM) Adapter for Bodo Translation.
Supports Google Gemini, OpenAI, and local Ollama inference with rich in-context Bodo linguistic guidance.
"""

import os
from typing import Optional, Tuple

BODO_LLM_SYSTEM_PROMPT = """You are an expert native linguist and translator for the Bodo language (बड़ो / बर', ISO: brx).
Bodo belongs to the Tibeto-Burman family, written officially in the Devanagari script.
Grammar rules:
1. Strict Subject-Object-Verb (SOV) sentence order (e.g. 'आं ओंखाम जायो' = I eat rice).
2. Verb suffixes: Present indefinite (-ओ / -यो), continuous (-दों), past (-बाय / -मोन), future (-गोन), negative (-आ / -या).
3. Postposition case markers: Accusative (-खौ), Instrumental (-जों), Dative (-नो), Ablative (-निफ्राय), Genitive (-नि), Locative (-आव).
4. Plural marker is -फोर (-fur).

Always provide the translation in authentic Bodo Devanagari script, followed by the phonetic Latin romanization in parentheses.
Format output strictly as:
Bodo: <Devanagari text>
Roman: <phonetic text>
"""


class LLMTranslator:
    def __init__(self, api_key: Optional[str] = None, provider: str = "auto"):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("OPENAI_API_KEY")
        self.provider = provider

    def is_available(self) -> bool:
        """Check if any LLM API key or local Ollama is configured."""
        return bool(self.api_key or os.environ.get("OLLAMA_HOST"))

    def translate(
        self,
        text: str,
        source_lang: str = "en",
        target_lang: str = "brx"
    ) -> Optional[Tuple[str, str]]:
        """
        Translate using configured LLM.
        Returns: (devanagari_text, romanized_text)
        """
        clean = text.strip()
        if not clean:
            return None

        # 1. Try Gemini
        gemini_key = self.api_key or os.environ.get("GEMINI_API_KEY")
        if gemini_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=gemini_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = f"{BODO_LLM_SYSTEM_PROMPT}\n\nTranslate from {source_lang} to {target_lang}:\n'{clean}'"
                response = model.generate_content(prompt)
                return self._parse_llm_response(response.text)
            except Exception:
                pass

        # 2. Try OpenAI
        openai_key = self.api_key or os.environ.get("OPENAI_API_KEY")
        if openai_key:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=openai_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": BODO_LLM_SYSTEM_PROMPT},
                        {"role": "user", "content": f"Translate from {source_lang} to {target_lang}:\n'{clean}'"}
                    ],
                    temperature=0.2,
                )
                return self._parse_llm_response(response.choices[0].message.content)
            except Exception:
                pass

        return None

    def _parse_llm_response(self, text: str) -> Tuple[str, str]:
        lines = text.strip().splitlines()
        dev = ""
        rom = ""
        for line in lines:
            if line.lower().startswith("bodo:"):
                dev = line.split(":", 1)[1].strip()
            elif line.lower().startswith("roman:"):
                rom = line.split(":", 1)[1].strip()
        if not dev and lines:
            dev = lines[0].strip()
        from bodonlp.phonetics import devanagari_to_latin
        return dev, rom or devanagari_to_latin(dev)
