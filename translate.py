import re
from groq import Groq
def split_text(text, max_length=1000):
    # 문장 단위로 텍스트를 분할합니다.
    sentences = re.split(r'\n+', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # 현재 문장과 함께 현재 청크의 길이를 계산합니다.
        if len(current_chunk) + len(sentence) + 1 <= max_length:
            current_chunk += sentence + "\n"
        else:
            # 현재 청크가 최대 길이에 도달하면 청크 목록에 추가하고 새 청크를 시작합니다.
            chunks.append(current_chunk + "\n")
            current_chunk = sentence + " "

    # 마지막 청크가 비어 있지 않다면 청크 목록에 추가합니다.
    if current_chunk:
        chunks.append(current_chunk + "\n")

    return chunks

class LLM():
    def __init__(self, api_key=""):
        self.model_id = "llama3-70b-8192"
        self.client = Groq(api_key=api_key)

    def chat(self, query):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": query,
                }
            ],
            model=self.model_id,
            temperature=0,
            max_tokens=1024,
            top_p=1e-8,
            seed=42,
        )
        return chat_completion.choices[0].message.content

ChatBot = LLM(api_key='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')

def translate_text(text):
    # 텍스트를 최대 길이에 따라 나눕니다.
    text_chunks = split_text(text)
    translated_chunks = []

    for chunk in text_chunks:
        model_input = f'''translate this to Korean. 
If the language is already Korean, do nothing and just response original text.
Here is the text you have to translate: 
        ```
        {chunk}
        ```
Do not print phrases like 'Here is the translation' or 'Translated by'.
        '''
        print(f"Translating: {model_input}")
        translated_chunk = ChatBot.chat(model_input)
        print(f"Translated: {translated_chunk}")
        model_input = f'''Check if the translation to Korean is correct. 
        If not, translate it again to Korean.
        Do not make corrections of the translation. Just print the re-translated text. 
        Here is the original text: {chunk} 
        Here is what you have translated: \n```\n{translated_chunk}\n```
        Do not print phrases like 'Here is the translation' or 'Translated by'.'''
        translated_chunk = ChatBot.chat(model_input)
        print(f"Checked: {translated_chunk}")
        translated_chunks.append(translated_chunk)

    # 번역된 청크들을 하나의 문자열로 결합합니다.
    translated_text = " ".join(translated_chunks)
    return translated_text