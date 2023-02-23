FROM python:3.11
WORKDIR /usr/src
ENV DB_USER: postgres
ENV DB_PASSWORD: password
ENV DB_HOST: localhost
ENV DB_PORT: 10000
ENV EMAIL_PASSWORD: password
ENV TELEGRAM_API_KEY: tg_key
ENV VK_API_KEY: vk_key
ENV LOGS_PATH: C:/Users/maksi/PycharmProjects/team_project/logs
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /usr/src/api
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/api"
CMD ["python", "/usr/src/api/main.py"]