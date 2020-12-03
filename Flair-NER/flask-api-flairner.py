from flask import Flask,jsonify,request,make_response,url_for,redirect
import requests, json

from flair.data import Sentence
from flair.models import SequenceTagger

#GPU OR CPU 
import sys

#cpu_or_gpu = int(sys.argv[1])
model_ = "ner-ontonotes"
# load the NER tagger
tagger = SequenceTagger.load(model_)

app = Flask(__name__)


@app.route("/healthcheck")
def hello():
    return "Yes, I am ohk. Health check success"

@app.route('/flairner', methods=['POST'])
def sifrank():
    req_data = request.get_json(force=True)
    text = req_data['text']
    sentence = Sentence(text)
    tagger.predict(sentence)
    o = sentence.to_dict(tag_type='ner')
    output = o['entities']
    print(output)
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
    
    return jsonify(entities)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 5001,debug=False, use_reloader=True,threaded=True)
