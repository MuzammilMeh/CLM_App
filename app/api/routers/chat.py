from typing import List

from fastapi.responses import StreamingResponse

from app.utils.json import json_to_model
from app.utils.index import get_index
from fastapi import APIRouter, Depends, HTTPException, Request, status
from llama_index.core import VectorStoreIndex
from llama_index.core.llms import MessageRole, ChatMessage
from pydantic import BaseModel
from llama_index.core import Settings

from llama_index.embeddings.huggingface import HuggingFaceEmbedding

chat_router = r = APIRouter()


class _Message(BaseModel):
    role: MessageRole
    content: str


class _ChatData(BaseModel):
    messages: List[_Message]


embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-mpnet-base-v2", max_length=512
)
# load the documents and create the index
Settings.embed_model = embed_model


@r.post("")
async def chat(
    request: Request,
    # Note: To support clients sending a JSON object using content-type "text/plain",
    # we need to use Depends(json_to_model(_ChatData)) here
    data: _ChatData = Depends(json_to_model(_ChatData)),
    index: VectorStoreIndex = Depends(get_index),
):
    # check preconditions and get last message
    if len(data.messages) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No messages provided",
        )
    lastMessage = data.messages.pop()
    if lastMessage.role != MessageRole.USER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Last message must be from user",
        )
    # convert messages coming from the request to type ChatMessage
    messages = [
        ChatMessage(
            role=m.role,
            content=m.content,
        )
        for m in data.messages
    ]

    # query chat engine
    query_engine = index.as_retriever(
        similarity_top_k=2, sparse_top_k=12, vector_store_query_mode="hybrid"
    )
    # chat_engine = index.as_chat_engine()

    # chat_engine = index.query_engine()
    # response = chat_engine.stream_chat(lastMessage.content, messages)
    response = query_engine.retrieve(lastMessage.content)
    file_names = []

    for node in response:
        file_name = node.metadata.get("file_name", None)
        if file_name:
            print(file_name)
            file_names.append(file_name)

    # # stream response
    # async def event_generator():
    #     for token in response.response_gen:
    #         # If client closes connection, stop sending events
    #         if await request.is_disconnected():
    #             break
    #         yield token
    return {"file_names": file_names}
