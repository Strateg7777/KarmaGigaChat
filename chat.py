from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat


class Chat:
    def __init__(self, initial_prompt: str, request_prompt: str, sber_chat: GigaChat):
        self.chat = sber_chat
        self.prompt = request_prompt
        self.initial_prompt = SystemMessage(content=initial_prompt)

    def answer(self, message: str | list[str]):
        if isinstance(message, list):
            message = "\n".join(message)
        prompt = self.prompt.format(message=message)
        full_prompt = [self.initial_prompt, HumanMessage(content=prompt)]
        res = self.chat(full_prompt).content
        return res
