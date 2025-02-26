import os

import google.generativeai as genai


class TextSummarizer:
    def __init__(self, *, prompt: str, model_name: str = "gemini-1.5-flash-8b", max_tokens: int = 1000):
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.prompt = prompt

        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

        # Check that the prompt contains the {text} placeholder, this is how we will inject the text to summarize
        if "{text}" not in self.prompt:
            raise ValueError("Prompt must contain {text} placeholder")

    def summarize(self, text: str) -> str:
        response = self.model.generate_content(self.prompt.format(text=text))
        return response.text
