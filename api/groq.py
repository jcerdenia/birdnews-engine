from groq import Groq

from misc.decorators import handle_error


class GroqAPI:
    ROLE_USER = "user"
    MODEL_LLAMA3_8B = "llama-3.1-8b-instant"
    MODEL_LLAMA3_70B = "llama3-70b-8192"

    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

    @handle_error
    def chat(self, prompt, model=MODEL_LLAMA3_8B):
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": self.ROLE_USER, "content": prompt}],
            model=model,
        )

        return chat_completion.choices[0].message.content
