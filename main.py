from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from selection import SemanticRecommender
import os
import LLm



recommender = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global recommender
    print("🚀 Encoding product data into vector space...")
    recommender = SemanticRecommender()
    yield
    print("🔚 Application shutting down...")
app = FastAPI(lifespan=lifespan)

class Message(BaseModel):
    role: str
    text: str

class ChatInput(BaseModel):
    text: Optional[str]
    image_path: Optional[str] = None  # 可选
    history_prompt: Optional[str]

@app.post("/chat")
async def chat_with_path(data: ChatInput):
    response = LLm.getResponse(data.text, data.history_prompt)
    recommendations = None
    if response["is_recommendation_request"] or data.image_path:
        if data.image_path:
            user_request = LLm.analyze_image(data.image_path)
            recommendation_list = recommender.query_by_image(data.image_path, user_request["categories"])
            final_result = LLm.double_check(recommendation_list, None, data.image_path)
        else:
            user_request = LLm.analyze_text(data.text, data.history_prompt)
            recommendation_list = recommender.query(user_request["semantic_query"], user_request["categories"])
            final_result = LLm.double_check(recommendation_list, user_request["semantic_query"], None)
        valid_indices = final_result.get("valid_indices", [])
        reply_text = final_result.get("reply_text", "Sorry, An error appears.")
        recommendations = [recommendation_list[i] for i in valid_indices]

    else:
        reply_text = response["response"]

    return JSONResponse(content={
        "text": reply_text,
        "recommendations": recommendations if recommendations else None,
    })



