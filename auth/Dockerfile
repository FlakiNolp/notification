FROM python:3.11
WORKDIR /usr/src
ENV DB_USER: postgres
ENV DB_PASSWORD: password
ENV DB_HOST: localhost
ENV DB_PORT: 10000
ENV SECRET_KEY: super_secret_key
ENV ALGORITHM: HS256
ENV ACCESS_TOKEN_EXPIRE_MINUTES: 15
ENV REFRESH_TOKEN_EXPIRE_HOURS: 720
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /usr/src/auth
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/auth"
CMD ["python", "/usr/src/auth/main.py"]