import os
from fastapi import FastAPI, HTTPException
from openai import AsyncOpenAI

from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from chainlit.auth import create_jwt
from chainlit.server import app
import chainlit as cl


client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])

settings = {
    "model": "gpt-3.5-turbo",
    "temperature": 0,
    "max_tokens": 500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

# app = FastAPI()

# Set up CORS middleware
origins = [
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/custom-auth")
async def custom_auth():
    try:
        # Your logic here
        token = create_jwt(cl.User(identifier="Test User"))
        return JSONResponse(content={"token": token}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful Kazakhstan legal assistant. You always reply in Russian."}],
    )
    await cl.Message(content="Connected to D&A AI Assistant!").send()


@cl.on_message
async def on_message(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()

    stream = await client.chat.completions.create(
        messages=message_history, stream=True, **settings
    )

    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await msg.stream_token(token)

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()