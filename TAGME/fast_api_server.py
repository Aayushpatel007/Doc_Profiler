from typing import Optional

from fastapi import FastAPI
import re
import sys
from pydantic import BaseModel
import uvicorn
import requests, json
import tagme


app = FastAPI()


class TAGME_MODEL(BaseModel):
    text: str
    tagme_score: Optional[float] = 0.1
    tagme_token_api : str


@app.get("/healthcheck")
async def healthcheck():
    return {"Hello": "World"}


@app.post("/tagme")
async def getEntities(body:TAGME_MODEL):
    text = body.text
    text = re.sub('[^.,a-zA-Z0-9 \n\.]', '', text)
    score = body.tagme_score
    tagme.GCUBE_TOKEN = str(body.tagme_token_api)
    lunch_annotations = tagme.annotate(text)
    # Print annotations with a score higher than 0.1
    entities = []
    for ann in lunch_annotations.get_annotations(score):
        s = str(re.findall(r'->(.*?)score:',str(ann)))
        entity = re.sub('[^A-Za-z0-9]+', ' ', s).strip()
        entities.append(entity)

    entities = list(dict.fromkeys(entities))
    entities = list(set(entities))
    entities_output = {
        "Entities" : entities
    }
    return entities_output


if __name__ == "__main__":
    uvicorn.run("fast_api_server:app", host="0.0.0.0", port=5003, log_level="info")
