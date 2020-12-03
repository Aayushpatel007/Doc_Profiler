FROM nvidia/cuda:10.1-base-ubuntu18.04

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip \
  && apt-get update 
	
COPY . /
RUN pip3 install -r requirements.txt 
ENTRYPOINT ["python3","fast_api_flair.py"]



