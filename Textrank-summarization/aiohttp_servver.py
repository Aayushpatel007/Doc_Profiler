from typing import Optional
from fastapi import FastAPI
import re
import sys
from gensim.summarization import summarize
from pydantic import BaseModel
import uvicorn


app = FastAPI()


class TextRank_Words(BaseModel):
    text: str
    summary_words: Optional[int] = 600

class TextRank_Ratio(BaseModel):
    text: str
    summary_ratio: Optional[float] = 0.4


@app.get("/healthcheck")
async def healthcheck():
    return {"Hello": "World"}


@app.post("/getSummaryByWords")
async def getSummaryByWords(body:TextRank_Words):
    text = body.text
    text = re.sub('[^.,a-zA-Z0-9 \n\.]', '', text)
    summary_words = body.summary_words
    summary = str(summarize(text, word_count=summary_words))
    summary = re.sub('[^.,a-zA-Z0-9 \n\.]', '', summary)
    summary_output = {
        "Summary" : summary
    }
    return summary_output

@app.post("/getSummaryByRatio")
async def getSummaryByRatio(body:TextRank_Ratio):
    text = body.text
    text = re.sub('[^.,a-zA-Z0-9 \n\.]', '', text)
    summary_ratio = body.summary_ratio
    summary = str(summarize(text, ratio=summary_ratio))
    summary = re.sub('[^.,a-zA-Z0-9 \n\.]', '', summary)
    summary_output = {
        "Summary" : summary
    }
    
    return summary_output

if __name__ == "__main__":
    uvicorn.run("aiohttp_servver:app", host="0.0.0.0", port=5004, log_level="info")