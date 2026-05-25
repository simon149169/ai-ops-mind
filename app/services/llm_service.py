from openai import AsyncOpenAI
from app.config import settings
from typing import List, Dict, Any, AsyncGenerator

client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_API_BASE
)

async def chat_completion(messages: List[Dict[str, str]], 
                         model: str = None,
                         stream: bool = False,
                         temperature: float = 0.7) -> Any:
    if model is None:
        model = settings.OPENAI_MODEL_NAME
    
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        stream=stream,
        temperature=temperature,
        max_tokens=4096
    )
    
    if stream:
        return response
    return response.choices[0].message.content

async def stream_chat_completion(messages: List[Dict[str, str]],
                                 model: str = None,
                                 temperature: float = 0.7) -> AsyncGenerator[str, None]:
    if model is None:
        model = settings.OPENAI_MODEL_NAME
    
    stream = await client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
        temperature=temperature,
        max_tokens=4096
    )
    
    async for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

def build_messages(system_prompt: str, user_prompt: str) -> List[Dict[str, str]]:
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

def build_conversation_history(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    return messages
