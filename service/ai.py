from api.groq import GroqAPI


class AIService:
    def __init__(self):
        self.groq = GroqAPI()

    def write_article(self, data):
        prompt = (
            f"Using the given data from an eBird checklist, create a blog story "
            f"in 3rd person. Keep it simple, factual, and accessible. No fake quotes. "
            f"Include a title, but don't label it; just make it a bold header."
            f"The title should be one memorable phrase. No colons."
            f"Make no reference to eBird. {data}"
        )

        return self.groq.chat(prompt)
