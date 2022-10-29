<h1>Микросервис на flask, для логгировани и оповещения событий</h1>

<h2>Подготовка к использованию</h2>
1. Чтобы начать пользоваться нужно, чтобы вы были в файле конфигурации, на данный момент этот процесс не автоматизирован</br>
</br>
Файл конфигурации содержит:</br>
    1. source - ip, с которого будут приходить запросы.</br>
    2. telegram - telegram_id, на который будет отправляться оповещения.</br>
    3. email - почта, на которую будет отправляться оповещения.</br>
    4. В будушем будет добавлена возможность добавления своих ресурсов, куда нужно будет отправлять post запросы.</br>
</br>
2. Запустить бота в телеграмме https://t.me/notification_program_bot, чтобы была возможность вам отправить сообщения. Он попросит у вас ip, который вы можете узнать у нас, а после введите почту, на которую хотите получать оповещения.</br>
</br>
3. Спустя пару минут вас добавят в конфиг и вы сможете пользоваться сервисом.
<h2>Правила использования</h2>
Чтобы микросервис обработал ваш запрос нужно отправить POST запрос с json в теле запроса, включающим ключи "code", "message" и "additional" на сайт https://notifications-telegram-bot.herokuapp.com/</br>
</br>
Получить все логи, вы можете по GET запросу на https://notifications-telegram-bot.herokuapp.com/logs</br>
</br>
<hr>
На данный момент, к сожалению telegram bot не синхронизирован в логами на сервере, поэтому кнокпи информация в нем не достоверна
