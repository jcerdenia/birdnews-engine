from groq import Groq

from misc.decorators import handle_error


class GroqAPI:
    ROLE_USER = "user"
    MODEL_DEFAULT = "llama3-8b-8192"

    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

    @handle_error
    def chat(self, prompt):
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": self.ROLE_USER, "content": prompt}],
            model=self.MODEL_DEFAULT,
        )

        return chat_completion.choices[0].message.content
