## DocProfiler

<i>Want to use multiple state-of-the art NLP frameworks/models to extract insights from any text data? </i>

#### <i> DocProfiler- an open source platform which uses microservice architecture(Docker containers) and asynchronous processing capabilities to run multiple Natural Language Processing tasks and extract important features from text.  </i>


### Currently supported NLP tools/frameworks

| Task | Framework/Model | Docker Image (GPU support available) | Ports |
| ----- | ----- | ----- | ---- |
| Unsupervised Keyphrase Extraction | [SIFRank-2020](https://github.com/sunyilgdx/SIFRank) | [docker pull aayushpatel007/sifrank-unsupervised-keyphrases-extraction](https://hub.docker.com/repository/docker/aayushpatel007/sifrank-unsupervised-keyphrases-extraction)| 5001 |
| Named Entity Recognition | [FlairNer](https://github.com/flairNLP/flair) | [docker pull aayushpatel007/flair-ner](https://hub.docker.com/repository/docker/aayushpatel007/flair-ner)| 5002 |
| Entity Linking | [TAGME](https://sobigdata.d4science.org/web/tagme/tagme-help) | [docker pull aayushpatel007/tagme](https://hub.docker.com/repository/docker/aayushpatel007/tagme)| 5003 |
| Text Summarization | [TextRank](https://radimrehurek.com/gensim/summarization/summariser.html) | [docker pull aayushpatel007/text-summarization](https://hub.docker.com/repository/docker/aayushpatel007/text-summarization)| 5004 | 
| GeoParsing | Mordecai (Upcoming) | --Upcoming-- | N.A |
| Language Detection | --Upcoming-- | --Upcoming-- | N.A |
| Readability Analysis | --Upcoming-- | --Upcoming-- | N.A |


### Getting Started

Step 1: Install Docker

https://docs.docker.com/engine/install/ubuntu/

Step 2: Install Docker compose (If required) 

https://docs.docker.com/compose/install/

Step 3: Using the provided docker-compose.yml file run "docker-compose up" to start the services and run all containers.

```
sudo docker-compose up
```

```
version: '3.3'
services:
    docprofiler:
        image: aayushpatel007/docprofiler
        ports: 
        - "5000:5000"
    unsupervised-keyphrase-extraction:
        image: aayushpatel007/sifrank-unsupervised-keyphrases-extraction
        ports:
        - "5001:5001"
        command: "-1"
    named-entity-recognition:
        image: aayushpatel007/flair-ner
        ports: 
        - "5002:5002"
    entity-linking:
        image: aayushpatel007/tagme
        ports:
        - "5003:5003"
    text-summariztion:
        image: aayushpatel007/text-summarization
        ports:
        - "5004:5004"
    
```
Note: You can remove the service from the above file if you don't require to perform a specific NLP task. 

#### <i> What tasks does DocProfiler performs and how? </i>

<img src="https://github.com/Aayushpatel007/Doc_Profiler/blob/master/images/docprofiler-img.png" width="500" height="400" style="vertical-align:center;">

Docprofiler serves as a REST API which perform asynchronous calls to other api's running inside other running containers and combine results from multiple NLP tasks. 

DocProfiler uses <b>Fast-api</b> inside for building a API and uses <b>async-await</b> for asynchronous processing. 

#### <i> How to use DocProfiler? </i>

Once the containers are up and running, you can go to "http://ip-addr:5000/docs" to see documentation provided by Fast-api. You can also try the API and see results. 

<img src="https://github.com/Aayushpatel007/Doc_Profiler/blob/master/images/fastapi1.png" width="950" height="590" style="vertical-align:center;">

##### Performing POST request with parameters

<img src="https://github.com/Aayushpatel007/Doc_Profiler/blob/master/images/docprofiler-model.png" width="900" height="600" style="vertical-align:center;">


<b>Using Python </b>

```
import requests

## Replace the URL by localhost or the ip-address where docker containers are running. 
URL = "http://34.222.108.44:5000/getDocumentProfile" 

text = """Soultaker is an American fantasy horror film written by Vivian Schilling and directed by Michael Rissi, released on October 26, 1990. It stars Joe Estevez in the title role, alongside Schilling, Gregg Thomsen, Chuck Williams, Robert Z'Dar, and David "Shark" Fralick. The film follows a group of young adults who try to flee from the Soultaker when their souls are ejected from their bodies after a car accident. Inspired by discussions with Action International Pictures producer Eric Parkinson, the script was based on a real-life car accident Schilling was involved in. The film was shot in five weeks on a $250,000 budget. Originally planned for a direct-to-video release, it saw limited theatrical screenings, with eight prints distributed in United States. Since its release, the film has received negative reviews, but won the Saturn Award for "Best Genre Video Release" in 1992. A sequel was planned but never made, and Schilling turned its premise into a novel titled Quietus, published in 2002. Soultaker was featured in the tenth-season premiere episode of the comedy television series Mystery Science Theater 3000 in 1999."""

parameters = {
              "text":text,
              "entity_linking_endpoint_tagme": "http://34.222.108.44:5003/tagme",
              "named_entity_recofnition_endpoint_flair" : "http://34.222.108.44:5002/getNamedEntities",
              "unsupervised_keyphrase_extraction_endpoint_sifrank": "http://34.222.108.44:5001/getKeyphrases",
              "text_summarization_endpoint_textrank": "http://34.222.108.44:5004/getSummaryByRatio",
              "tagme_score": 0.3,
              "tagme_token_api": "",
              "no_of_keyphrases": 10,
              "sifrank_algo": 0,
              "summary_words": 700,
              "summary_ratio": 0.3
}
headers = {'content-type': "application/json"}

response = requests.request("POST", URL, json=parameters, headers=headers)
print(response.text)
```


<b> Output </b>

```
{
  "Entities": [
    "Television program",
    "Mystery Science Theater 3000",
    "Vivian Schilling",
    "Joe Estevez",
    "David quot Shark quot Fralick",
    "Original video animation",
    "Soultaker film",
    "The SoulTaker",
    "The Quietus",
    "Action International Pictures",
    "Horror film",
    "Saturn Award"
  ],
  "Keyphrases": [
    "comedy television series mystery science theater",
    "tenthseason premiere episode",
    "soultaker",
    "michael rissi",
    "reallife car accident schilling",
    "genre video release",
    "action international pictures producer eric parkinson",
    "vivian schilling",
    "david shark fralick",
    "american fantasy horror film"
  ],
  "Summary": "Soultaker is an American fantasy horror film written by Vivian Schilling and directed by Michael Rissi, released on October 26, 1990. The film follows a group of young adults who try to flee from the Soultaker when their souls are ejected from their bodies after a car accident.",
  "GPE": [
    "United States"
  ],
  "ORG": [
    "Action International Pictures"
  ],
  "PERSON": [
    "Joe Estevez",
    "Schilling",
    "Chuck Williams",
    "Vivian Schilling",
    "Michael Rissi",
    "Soultaker",
    "Gregg Thomsen",
    "Eric Parkinson",
    "Robert ZDar",
    "David Shark Fralick"
  ],
  "LOC": [],
  "NORP": [
    "American"
  ],
  "EVENT": [],
  "DATE": [
    "October 26, 1990",
    "five weeks",
    "1992",
    "1999",
    "2002"
  ],
  "MONEY": [],
  "ADDITIONAL": [
    "250,000",
    "the Saturn Award for Best Genre Video Release",
    "Soultaker",
    "eight",
    "Quietus",
    "Mystery Science Theater 3000"
  ]
}

```


<b> Using CURL </b>
```
curl -X POST "http://34.222.108.44:5000/getDocumentProfile" -H  "accept: application/json" -H  "Content-Type: application/json" 
-d "{
    "text":"text",
    "entity_linking_endpoint_tagme":"http://34.222.108.44:5003/tagme","named_entity_recofnition_endpoint_flair":"http://34.222.108.44:5002/getNamedEntities\",
    "unsupervised_keyphrase_extraction_endpoint_sifrank":\"http://34.222.108.44:5001/getKeyphrases\",
    "text_summarization_endpoint_textrank":"http://34.222.108.44:5004/getSummaryByRatio\",
    "tagme_score":0.3,
    "tagme_token_api":"",
    "no_of_keyphrases":10,
    "sifrank_algo":0,
    "summary_words":700,
    "summary_ratio":0.3
    }"
```

