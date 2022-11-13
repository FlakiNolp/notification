<h1>Микросервис на FAST API, для логгировани и оповещения событий</h1>

<h2>Подготовка к использованию</h2>
1. Чтобы начать пользоваться нужно, чтобы вы были в файле конфигурации, на данный момент этот процесс не автоматизирован</br>
</br>
Файл конфигурации содержит:</br>
    1. source - ip, с которого будут приходить запросы.</br>
    2. telegram - telegram_id, на который будут отправляться оповещения.</br>
    3. email - почта, на которую будут отправляться оповещения.</br>
    4. vk - vk_domain, на который будут отправляться оповещение.</br>
    5. website - домен сайта, на который будут приходить post запрос с оповещением.</br>
    6. В будушем будет добавлена возможность добавления своих ресурсов, куда нужно будет отправлять post запросы.</br>
</br>
2. Запустить бота в телеграмме https://t.me/notification_program_bot, чтобы была возможность вам отправить сообщения, если такое требуется.</br>
3. Разрешить сообществу https://vk.com/notifications_service писать сообщения, либо просто отправить что-то самому.</br>
4. Спустя пару минут вас добавят в конфиг и вы сможете пользоваться сервисом.</br>
</br>
<h2>Правила использования</h2>
Чтобы микросервис обработал ваш запрос нужно отправить POST запрос с json в теле запроса, включающим ключи "code", "message" и "additional" на сайт https://telegram-bot-notification.herokuapp.com/api</br>
</br>
Получить все логи, вы можете по GET запросу на https://telegram-bot-notification.herokuapp.com/api/logs</br>
Так же поддерживаются параметры для фильтрации:</br>
    1. code - list[int], номера кодов http .</br>
    2. time_from - datetime, datetime время в формате "2022-11-06 10:14:36" для обозначения начала промежутка времени.</br>
    3. time_to - datetime, datetime в формате "2022-11-06 10:14:36" время для обозначения конца промежутка времени.</br>
    4. message - list[str], строки, которые точно равны значениям в logs.</br>
    5. addtional - list[str], строки, которые точно равны значениям в logs.</br>
</br>
Еще есть панель админа с возможностью добавления, удаления и редактирования пользователей (доступна только людям в while list админов по ip):</br>
    1. https://telegram-bot-notification.herokuapp.com/settings - основное меню.</br>
    2. https://telegram-bot-notification.herokuapp.com/settings/add - добавление нового пользователя (формы с post запросом).</br>
    3. https://telegram-bot-notification.herokuapp.com/settings/delete - удаление пользователя (форма с post запросом).</br>
    4. https://telegram-bot-notification.herokuapp.com/settings/edit - редактирование пользователя (формы с post запросом).</br>
</br>
<hr>
На данный момент, к сожалению telegram bot не синхронизирован в логами на сервере, поэтому кнокпи информация в нем не достоверна
