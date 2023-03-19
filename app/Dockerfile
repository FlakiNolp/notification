FROM python:3.11
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN pip install -r requirements.txt
EXPOSE 1002
CMD uvicorn app.main:app --host 0.0.0.0 --port 1002 --workers 4