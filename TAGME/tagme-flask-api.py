from flask import Flask,jsonify,request,make_response,url_for,redirect
import requests, json
import tagme
import re
import sys

# Set the authorization token for subsequent calls.
tagme.GCUBE_TOKEN = str(sys.argv[2])
score_higher_than = 0.2
score_higher_than = float(sys.argv[1])

app = Flask(__name__)
@app.route('/tagme', methods=['POST'])
def return_tags():
    req_data = request.get_json(force=True)
    text = req_data['text']
    lunch_annotations = tagme.annotate(text)
    # Print annotations with a score higher than 0.1
    entities = []
    for ann in lunch_annotations.get_annotations(score_higher_than):
        s = str(re.findall(r'->(.*?)score:',str(ann)))
        entity = re.sub('[^A-Za-z0-9]+', ' ', s).strip()
        entities.append(entity)

    entities = list(dict.fromkeys(entities))
    entities_output = {
        "Entity-Linking-Entities" : entities
    }
    return jsonify(entities_output)

    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 5002,debug=False, use_reloader=True,threaded=True)



