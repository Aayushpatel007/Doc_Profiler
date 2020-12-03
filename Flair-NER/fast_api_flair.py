from typing import Optional
from fastapi import FastAPI
import re
import sys
from pydantic import BaseModel
import uvicorn

import requests, json

from flair.data import Sentence
from flair.models import SequenceTagger

import sys

model_ = "ner-ontonotes"
# load the NER tagger
tagger = SequenceTagger.load(model_)

app = FastAPI()

class FLAIR_NER_MODEL(BaseModel):
    text: str



@app.get("/healthcheck")
async def healthcheck():
    return {"Hello": "World"}


@app.post("/getNamedEntities")
async def getNamedEntities(body:FLAIR_NER_MODEL):
    text = body.text
    text = re.sub('[^.,a-zA-Z0-9 \n\.]', '', text)
    sentence = Sentence(text)
    tagger.predict(sentence)
    o = sentence.to_dict(tag_type='ner')
    output = o['entities']
    #print(output)
    GPE = []
    ORG =[]
    LOC =[]
    PERSON =[]
    EVENT = []
    DATE = []
    MONEY =[]
    NORP = [] #NATIONALITIES
    ADDITIONAL = []
    for i in range(len(output)):
        if "GPE" in str(output[i]["labels"]):
            GPE.append(output[i]["text"])
        elif "PERSON" in str(output[i]["labels"]):
            PERSON.append(output[i]["text"])
        elif "ORG" in str(output[i]["labels"]):
            ORG.append(output[i]["text"])
        elif "LOC" in str(output[i]["labels"]):
            LOC.append(output[i]["text"])
        elif "EVENT" in str(output[i]["labels"]):
            EVENT.append(output[i]["text"])
        elif "DATE" in str(output[i]["labels"]):
            DATE.append(output[i]["text"])
        elif "MONEY" in str(output[i]["labels"]):
            MONEY.append(output[i]["text"])
        elif "NORP" in str(output[i]["labels"]):
            NORP.append(output[i]["text"])
        else:
            ADDITIONAL.append(output[i]["text"])
    entities = {
        'GPE': list(set(GPE)),
        'ORG': list(set(ORG)),
        "PERSON" : list(set(PERSON)),
        "EVENT": list(set(EVENT)),
        "DATE": list(set(DATE)),
        "MONEY" : list(set(MONEY)),
        "NORP" :list(set(NORP)),
        "LOC": list(set(LOC)),
        "ADDITIONAL" : list(set(ADDITIONAL))

    }
    return entities



if __name__ == "__main__":
    uvicorn.run("fast_api_flair:app", host="0.0.0.0", port=5002, log_level="info")