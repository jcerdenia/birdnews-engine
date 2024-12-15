import os

from groq import Groq

from misc.decorators import handle_error


class _GroqAPI:
    ROLE_USER = "user"
    MODEL_DEFAULT = "llama3-8b-8192"

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    @handle_error
    def chat(self, prompt):
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": self.ROLE_USER, "content": prompt}],
            model=self.MODEL_DEFAULT,
        )

        return chat_completion.choices[0].message.content


GroqAPI = _GroqAPI()
