# Чат-бота для Медиа-отдела 

### Run the project @granate_media_bot
1. `pip install -r requirements.txt`
2. Нужно создать бд в PostgreSQL. Создать файл .env и добавить туда PASSWORD базы данных и также бот-токен с названием TOKEN_API. Характеристки бд есть в bot/database.py. 
3. В файле bot/main_handlers.py в строке 56 нужно добавить id группы, в которую будут отправляться вопросы. И также нужно добавить в эту группу бота @granate_media_bot в качестве админа.
4. Наконец для запуска бота: `python main.py`


## Таблицы БД
#### Users
В этой таблице хранятся id всех людей, когда-либо общавшихся с ботом. Данные из этой таблицы используются для рассылки всем пользователям бота. Также сохраняется информация о том, отправлять ли все рассылки.
#### Question
В этой таблице хранятся все вопросы, которые пользователи задают вместе со своим id. Еще есть поля – answered, чтобы понять, ответили ли мы на этот вопрос.

## Команды
`/start` - для повяления меню с выбором: вопрос, рассылка, возможности, о проектке

`/send_to_user chat_id question_id ANSWER` - после того, как вы получили вопрос от пользователя, вы можете отправить ему ответ на его вопрос с помощью этой команды. Эту команду могут использовать только пользователи ботов, у которых в поле admin указано значение true. (После общения с ботом пользователь появится в базе данных в таблице users и там вы сможете изменить значение этого поля и сделать себя админом)

`/send_to_all NOTIFICATION` - для отправки рассылок всем пользователям (используется только админами)

`/send_to_all_on NOTIFICATION` - для отправки рассылок только пользователям, которые подписаны на рассылку (используется только админами)
