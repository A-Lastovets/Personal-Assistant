# Personal-Assistant

Файл .env має бути створений у корені проекту і заповнений згідно прикладу .env.sample
Залежності встановлюються з файлу requirements.txt

Якщо записувати данні на хмарну базу данних Koyeb то контейнери не потрібні.

Якщо записувати данні до локальної бази данних, то можна створити контейнери(для Postgres та PgAdmin) :
БД піднімається командою:

docker-compose build

docker compose up -d

Застосунок доступний за адресою: http://127.0.0.1:8000/home

В застосунку PgAdmin для того щоб перевірити чи користувачі додані, треба написати таку команду:

SELECT * FROM contacts_app_contact;

Через термінал при запущеному контейнері для пвдключення до локальної бази PostgreSQL треба написати:

docker exec -it assistant_postgres psql -U assistant -d assistant

а потім написати :
 
SELECT * FROM contacts_app_contact;  - таблиця з контактами з відповідними id користувачів
SELECT * FROM  notes_app_note;       - таблиця з нотатками з відповідними id користувачів
SELECT * FROM   notes_app_note_tags; - таблиця яка показує який id нотатки прив'язаний до id тегу
SELECT * FROM    notes_app_tag;      - таблиця яка показує теги та відповідний id
SELECT * FROM    users_app_profile;  - таблиця яка показує чи завантажені аватари користувачів з відповідними id
SELECT * FROM    files_app_file;     - таблиця яка показує які файли були завантаженні на хмарний сервіс Claudinary

