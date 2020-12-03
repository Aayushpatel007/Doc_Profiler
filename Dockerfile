FROM python:3.7
COPY . /
RUN pip3 install -r requirements.txt 
ENTRYPOINT ["python3","docprofiler_fast_api.py"]
