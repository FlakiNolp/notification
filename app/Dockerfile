FROM python:3.11
WORKDIR /usr/src
ENV DB_USER: postgres
ENV DB_PASSWORD: password
ENV DB_HOST: localhost
ENV DB_PORT: 10000
ENV SECRET_KEY: super_secret_key
ENV EMAIL_PASSWORD: password
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /usr/src/app
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"
CMD ["python", "/usr/src/app/main.py"]