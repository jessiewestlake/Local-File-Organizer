from ollama import chat
from ollama import ChatResponse
import ollama

print(ollama.list())
response: ChatResponse = chat(model='qwen3:8b', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response)
# or access fields directly from the response object
print(response.message.content)