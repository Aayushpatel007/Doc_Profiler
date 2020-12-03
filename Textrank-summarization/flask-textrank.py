from flask import Flask,jsonify,request,make_response,url_for,redirect
import requests, json
import re
import sys
from gensim.summarization import summarize

app = Flask(__name__)

@app.route("/healthcheck")
def hello():
    return "Yes, I am ohk. Health check success"

@app.route('/getsummary', methods=['POST'])
def return_summ():
    req_data = request.get_json(force=True)
    text = req_data['text']
    if 'summary_words' in req_data:
        summary_words = int(req_data['summary_words'])
    else:
        summary_words= 500
    summary = str(summarize(text, word_count=summary_words))
    summary_output = {
        "Summary" : summary
    }
    return jsonify(summary_output)


@app.route('/textrank', methods=['POST'])
def return_tags():
    req_data = request.get_json(force=True)
    text = req_data['text']
    if 'summary_ratio' in req_data:
        summary_ratio = float(req_data['summary_ratio'])
    else:
        summary_ratio= 0.5
    summary = str(summarize(text, ratio=summary_ratio))
    summary_output = {
        "Summary" : summary
    }
    return jsonify(summary_output)

    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 5003,debug=False, use_reloader=True,threaded=True)



