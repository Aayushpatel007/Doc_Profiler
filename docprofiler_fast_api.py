from docprofiler import generate_profile
from typing import Optional
from fastapi import FastAPI
import re
import sys
from pydantic import BaseModel
import requests, json
import asyncio
import uvicorn
#import nest_asyncio
#nest_asyncio.apply()

app = FastAPI()

class DOCPROFILER_MODEL(BaseModel):
    text: str
    entity_linking_endpoint_tagme: Optional[str] = "http://localhost:5003/tagme"
    unsupervised_keyphrase_extraction_endpoint_sifrank: Optional[str] = "http://localhost:5001/getKeyphrases"
    named_entity_recofnition_endpoint_flair: Optional[str] = "http://localhost:5002/getNamedEntities"
    text_summarization_endpoint_textrank:Optional[str] = "http://localhost:5004/getSummaryByRatio"
    tagme_score: Optional[float] = 0.1
    tagme_token_api : Optional[str] = ""
    no_of_keyphrases: Optional[int] = 10
    sifrank_algo:Optional[int] = 0
    summary_words: Optional[int] = 600
    summary_ratio: Optional[float] = 0.4


@app.get("/healthcheck")
async def healthcheck():
    return {"Hello": "World"}


@app.post("/getDocumentProfile")
def getDocumentProfile(body:DOCPROFILER_MODEL):
    asyncio.set_event_loop(asyncio.new_event_loop())

    text = body.text
    text = re.sub('[^.,a-zA-Z0-9 \.]', '', text)
    summary_words = body.summary_words
    summary_ratio = body.summary_ratio
    no_of_phrases = body.no_of_keyphrases
    sifrank_algo = body.sifrank_algo
    tagme_score = body.tagme_score
    tagme_token_api = str(body.tagme_token_api)
    url_list = []
    if body.entity_linking_endpoint_tagme!="":
        url_list.append(body.entity_linking_endpoint_tagme)
    if body.unsupervised_keyphrase_extraction_endpoint_sifrank!="":
        url_list.append(body.unsupervised_keyphrase_extraction_endpoint_sifrank)
    if body.named_entity_recofnition_endpoint_flair!="":
        url_list.append(body.named_entity_recofnition_endpoint_flair)
    if body.text_summarization_endpoint_textrank!="":
        url_list.append(body.text_summarization_endpoint_textrank)
    print(url_list)
    data,final_time = generate_profile(text, URL_LIST=url_list,no_of_keyphrases=no_of_phrases,sifrankalgo=sifrank_algo,summarywords=summary_words,summaryratio=summary_ratio,tagmescore=tagme_score,tagmetokenapi=tagme_token_api)
    print(final_time)
    #print(data)
    print(type(data))
    return data


if __name__ == "__main__":
    uvicorn.run("docprofiler_fast_api:app", host="0.0.0.0", port=5000, log_level="info")



"""
@app.route('/docprofiler', methods=['POST'])
def return_tags():
    asyncio.set_event_loop(asyncio.new_event_loop())
    req_data = request.get_json(force=True)
    text = req_data['text']
    text = ''.join(char for char in text if ord(char) < 128)
    print(text)
    if "docid" in req_data:
        docid = req_data["document_id"]
    if "title" in req_data:
        title = req_data["document_title"]
    if "url" in req_data:
        url= req_data["document_url"]
    url_list = []
    if "flair_ner_endpoint" in req_data:
        flair_enpoint = req_data['flair_ner_endpoint']
        url_list.append(flair_enpoint)
    if "sifrank_keyphrases_endpoint" in req_data:
        sifrank_keyphrases_endpoint = req_data['sifrank_keyphrases_endpoint']
        url_list.append(sifrank_keyphrases_endpoint)
    if "text_summarization_endpoint" in req_data:
        text_summarization_endpoint = req_data['text_summarization_endpoint']
        url_list.append(text_summarization_endpoint)
    if "entity_endpoint" in req_data:
        dbpedia_flask_endpoint = req_data['entity_endpoint']
        url_list.append(dbpedia_flask_endpoint)
    
    
    if "no_of_keyphrases" in req_data:
        no_of_keyphrases = req_data["no_of_keyphrases"]
    else:
        no_of_keyphrases = 10
    if "dbpedia_score" in req_data:
        dbpedia_score = req_data["dbpedia_score"]
    else:
        dbpedia_score=0.65
    if "dbped_host_url" in req_data:
        dbped_host_url = req_data["dbped_host_url"]
    else:
        dbped_host_url = "none"
    
    print(url_list)
    
    data,final_time = generate_profile(text, URL_LIST=url_list,no_of_keyphrases=no_of_keyphrases,entity_linking_dbpedia_sc=dbpedia_score,dbped_host_url=dbped_host_url)
    print(final_time)
    print(data)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 5000,debug=False, use_reloader=True,threaded=True)



"""
