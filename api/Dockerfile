FROM python:3.11
WORKDIR /usr/src/api
COPY . /usr/src/api
RUN pip install -r requirements.txt
EXPOSE 1001
CMD uvicorn api.main:app --host 0.0.0.0 --port 1001 --workers 4