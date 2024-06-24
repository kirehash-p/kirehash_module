import google.generativeai as genai

class GeminiPro():
    def __init__(self, api_key=None):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.chats = {}

    def generate(self, prompt: str|list, **kwargs) -> genai.types.GenerateContentResponse:
        if not prompt:
            raise ValueError('Prompt is required')
        return self.model.generate_content(prompt, **kwargs)
    
    def create_chat(self, idx=None, history: list=[]) -> str:
        if idx is None:
            idx = 0
            while idx not in self.chats.keys():
                idx += 1
        self.chats[idx] = self.model.start_chat(history=history)
        return idx

    def delete_chat(self, idx) -> bool:
        if idx not in self.chats.keys():
            return False
        del self.chats[idx]
        return True
    
    def chat(self, idx, message: str) -> str:
        if idx not in self.chats.keys():
            raise ValueError(f'Chat with index {idx} not found')
        return self.chats[idx].send_message(message)
    
    def count_tokens(self, prompt: str|list) -> int:
        return self.model.count_tokens(prompt)