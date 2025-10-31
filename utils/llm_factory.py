import os
import google.generativeai as genai
from crewai import LLM


class GeminiLLM:
    """Wrapper to make Google's Gemini LLM compatible with CrewAI agents."""

    def __init__(self, model: str = "gemini-2.5-flash", temperature: float = 0.3, api_key: str | None = None):
        self.model = model
        self.temperature = temperature

        # Use provided key or fall back to environment
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is required for GeminiLLM")

        # Configure the Gemini client
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(model_name=self.model)

    def __call__(self, prompt: str) -> str:
        """Direct call interface for LLM."""
        response = self.client.generate_content(
            prompt,
            generation_config={"temperature": self.temperature},
        )
        if hasattr(response, "text"):
            return response.text
        elif hasattr(response, "candidates") and response.candidates:
            return response.candidates[0].content.parts[0].text
        else:
            return str(response)

    def bind(self, **kwargs):
        """Return a callable suitable for CrewAI agents."""
        stop_words = kwargs.get("stop", None)

        def bound(prompt: str):
            response = self(prompt)
            if stop_words:
                for word in stop_words:
                    response = response.split(word)[0]
            return response.strip()

        return bound


def create_llm(config: dict):
    """Factory function for CrewAI-style LLM injection using Gemini."""
    model_name = config.get("gemini_model", "gemini-2.5-flash")
    temperature = float(config.get("temperature", 0.3))
    api_key = config.get("gemini_api_key") or os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is required")

    gemini = GeminiLLM(model=model_name, temperature=temperature, api_key=api_key)

    # Create CrewAI LLM wrapper — remove provider argument
    return LLM(
        model=model_name,
        call_fn=gemini.bind()
    )

