"""
Hugging Face Neural Translation Adapter for Bodo.
Supports Meta NLLB-200 (brx_Deva) and AI4Bharat IndicTrans2 models.
"""

from typing import Optional, Tuple


class HuggingFaceTranslator:
    def __init__(self, model_name: str = "facebook/nllb-200-distilled-600M"):
        self.model_name = model_name
        self._pipeline = None
        self._tokenizer = None
        self._model = None

    def is_available(self) -> bool:
        """Check if torch and transformers are installed."""
        try:
            import torch
            import transformers
            return True
        except ImportError:
            return False

    def load_model(self):
        """Lazy load Hugging Face model and tokenizer."""
        if self._model is not None:
            return
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self._model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)

    def translate(
        self,
        text: str,
        src_lang: str = "eng_Latn",
        tgt_lang: str = "brx_Deva"
    ) -> Optional[str]:
        """
        Translate using NLLB-200 model.
        Codes: 'brx_Deva' for Bodo, 'eng_Latn' for English, 'hin_Deva' for Hindi.
        """
        if not self.is_available():
            return None
            
        try:
            self.load_model()
            inputs = self._tokenizer(text, return_tensors="pt")
            forced_bos_token_id = self._tokenizer.lang_code_to_id.get(tgt_lang)
            
            gen_tokens = self._model.generate(
                **inputs,
                forced_bos_token_id=forced_bos_token_id,
                max_length=128
            )
            return self._tokenizer.batch_decode(gen_tokens, skip_special_tokens=True)[0]
        except Exception:
            return None
