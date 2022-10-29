import json, requests, smtplib, time, os.path
from flask import Flask, jsonify, request
from email.mime.text import MIMEText


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        response = request.get_json(silent=True)
        if response != None and 'code' in response and 'message' in response and 'additional' in response:
            if 100 <= int(response['code']) <= 526 and response['message'] != '' or None and response['additional'] != None:
                with open('configuration.json', 'r') as f:
                    sources = json.load(f)
                ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
                print(ip)
                for source in sources['sources']:
                    if source['source'] == ip:
                        text = f'''code: {response['code']}\nmessage: {response['message']}\nadditional: {response['additional']}'''

                        if 'telegram' in source:
                            requests.get(f'''https://api.telegram.org/bot(api ключ telegram бота)/sendMessage?chat_id={source['telegram']}&text={text}''')

                        if 'email' in source:
                            recipient = source['email']
                            send_mail(recipient, text)

                        response['time'] = str(time.strftime("%m/%d/%Y, %H:%M:%S", time.gmtime(time.time())))
                        save_logs(response, source)

                        return jsonify('OK'), 200
                else:
                    return jsonify('Forbidden'), 403
            else:
                return jsonify('Bad Request'), 400
        else:
            return jsonify('Bad Request'), 400
    else:
        return jsonify({"code": "Method not allowed",
                       "message": "Need POST request with JSON having code, message and additional"}), 405
def save_logs(response, source):
    try:
        with open(f'''logs/{source['source']}.json''', 'r+') as f:
            logs_dict = json.load(f)
            logs_list = logs_dict['logs']
            logs_list.append(response)
            logs_dict = logs_dict
        with open(f'''logs/{source['source']}.json''', 'w+') as f:
            json.dump(logs_dict, f, ensure_ascii=False)
    except:
        logs_dict = {'logs': [response]}
        with open(f'''logs/{source['source']}.json''', 'x+') as f:
            json.dump(logs_dict, f, ensure_ascii=False)

def send_mail(recipient, text):
    sender = 'check.telegram.bot@gmail.com'
    password = '(Пароль от приложения почты)'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(f'{text}')
        msg['Subject'] = 'Error notification'
        server.sendmail(sender, recipient, msg.as_string())

        return f'Письмо успешно отправлено на {recipient}'

    except Exception as ex:
        print(ex)
        print('Не получилось отправить письмо')

@app.route('/logs', methods=['GET'])
def get_logs():
    ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    print(ip)
    if os.path.exists(f'logs/{ip}.json'):
        with open(f'logs/{ip}.json', 'r') as f:
            logs = json.load(f)
            return jsonify(logs), 200
    else:
        with open('configuration.json', 'r') as f:
            sources = json.load(f)
            for source in sources['sources']:
                if source['source'] == ip:
                    return jsonify('От вас еще не было запросов'), 200
            else:
                return jsonify('Forbidden'), 403


if __name__ == '__main__':
    app.run(debug=True)