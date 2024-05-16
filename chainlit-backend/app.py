import os
# from fastapi import FastAPI, HTTPException
# from openai import AsyncOpenAI
# from langchain.llms import OpenAI
# from langchain_community.llms import OpenAI

from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from chainlit.auth import create_jwt
from chainlit.server import app
import chainlit as cl
from langchain_community.vectorstores import Chroma
# from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
#from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable, RunnablePassthrough, RunnableConfig
from langchain.callbacks.base import BaseCallbackHandler
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


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

embeddings_model = OpenAIEmbeddings()

model = ChatOpenAI(model_name="gpt-4",
                   temperature=0.5,
                   max_tokens=700,
                   streaming=True)

persist_directory = '/Users/arnur/projects/ai-legal-assistant/db'
doc_search = Chroma(persist_directory=persist_directory, embedding_function=embeddings_model)


async def setup_runnable():
    template = """As a legal assistant specializing in Kazakhstani law, your role is to provide accurate and detailed responses in Russian. Your responses should always include the name of the relevant law and specific sources whenever possible. 

    Please consider the following context to answer the question:

    Context: {context}

    Question: {question}

    Remember, your expertise is in Kazakhstani law. Please provide a detailed response in Russian, citing the relevant law and sources.
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    
    retriever = doc_search.as_retriever()
    
    runnable = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    return runnable

@cl.on_chat_start
async def on_chat_start():
    runnable = await setup_runnable()
    cl.user_session.set("runnable", runnable)
    
    await cl.Message(content="Здравствуйте! Я ваш ИИ-ассистент по законодательству Республике Казахстан. На текущий момент я владею знаниями о следующих законах:\"Закон о персональных данных и их защите\", \"Закон о банках и банковской деятельности\" и \"Закон о связи.\"").send()
    
@cl.on_message
async def on_message(message: cl.Message):
    message_history = cl.user_session.get("message_history", [])
    message_history.append({"role": "user", "content": message.content})

    runnable = cl.user_session.get("runnable")
    
    msg = cl.Message(content="")
    
    class PostMessageHandler(BaseCallbackHandler):
        def __init__(self, msg: cl.Message):
            BaseCallbackHandler.__init__(self)
            self.msg = msg
            self.sources = set()
            
        def on_retriever_end(self, documents, *, run_id, parent_run_id, **kwargs):
            for d in documents:
                #print(d)
                source_page_pair = (d.metadata['source'])
                
                self.sources.add(source_page_pair)
                
        def on_llm_end(self, response, *, run_id, parent_run_id, **kwargs):
            if len(self.sources):
                sources_text = "\n".join([f"{source}" for source in self.sources])
                print(sources_text)
                self.msg.elements.append(
                    cl.Text(name="Sources", content=sources_text, display="block")
                )
    
    history_string = "\n".join([f"{msg['role']}: {msg['content']}" for msg in message_history])

    async with cl.Step(type="run", name="QA Assistant"):
        async for chunk in runnable.astream(
            history_string,
            config=RunnableConfig(callbacks=[
                cl.LangchainCallbackHandler(),
                PostMessageHandler(msg)
            ])
        ):
            await msg.stream_token(chunk)
    await msg.send()
    
    message_history.append({"role": "assistant", "content": msg.content})
    cl.user_session.set("message_history", message_history)
