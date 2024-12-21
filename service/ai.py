from api.groq import GroqAPI


class AIService:
    def __init__(self):
        self.groq = GroqAPI()

    def write_article(self, data):
        prompt = (
            f"Based on the given eBird checklist data, write a blog story "
            f"in 3rd person. Keep it entertaining but factual. No fake quotes. "
            f"Include a title, but don't label it; just make it a bold header. "
            f"The title should be descriptive and summarize the story. "
            f"Do not treat the given bird list as chronological. "
            f"Make no reference to eBird. {data}"
        )

        return self.groq.chat(prompt)
