import os

import google.generativeai as genai


class TextSummarizer:
    def __init__(
        self,
        *,
        prompt: str,
        model_name: str = "gemini-1.5-flash-8b",
        max_output_tokens: int = 1000,
        enable_protection: bool = False,
    ):
        self.model_name = model_name
        self.max_output_tokens = max_output_tokens
        self.prompt = prompt
        self.enable_protection = enable_protection

        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

        # Check that the prompt contains the {text} placeholder, this is how we will inject the text to summarize
        if "{text}" not in self.prompt:
            raise ValueError("Prompt must contain {text} placeholder")

    def summarize(self, text: str) -> str:
        response_text = self.model.generate_content(self.prompt.format(text=text)).text
        if self.enable_protection:
            prompt_start = self.prompt.split("{text}")[0][:50]

            # If this distinctive prompt fragment appears in the response, it's likely a leak
            if prompt_start in response_text:
                return "Error: Unable to generate a valid summary."

        return response_text
