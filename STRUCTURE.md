+---personal_assistant
|   .env
|   .env.sample
|   .gitignore
|   docker-compose.yaml
|   dockerfile
|   LICENSE
|   README.md
|   
+---personal_assistant
|   |   manage.py
|   
+---contacts_app
|   |   __init__.py
|   |   admin.py
|   |   apps.py
|   |   models.py
|   |   tests.py
|   |   views.py
|   +---migrations
|   |       __init__.py
|           
+---files_app
|   |   __init__.py
|   |   admin.py
|   |   apps.py
|   |   models.py
|   |   tests.py
|   |   views.py
|   +---migrations
|   |       __init__.py
|           
+---notes_app
|   |   __init__.py
|   |   admin.py
|   |   apps.py
|   |   models.py
|   |   tests.py
|   |   views.py
|   +---migrations
|   |       __init__.py
|           
+---news_app
|   |   __init__.py
|   |   admin.py
|   |   apps.py
|   |   models.py
|   |   tests.py
|   |   views.py
|   +---migrations
|           __init__.py
|           
+---users_app
|   |   __init__.py
|   |   admin.py
|   |   apps.py
|   |   forms.py
|   |   models.py
|   |   tests.py
|   |   views.py
|   +---migrations
|   |       __init__.py
|   
+---personal_assistant
|   |   asgi.py
|   |   settings.py
|   |   urls.py
|   |   wsgi.py
|   |   __init__.py
|   
+---templates
|   +---contacts_app
|   |       add_contact.html
|   |       contact_detail.html
|   |       contact_list.html
|   |       edit_contact.html
|   +---files_app
|   |       file_detail.html
|   |       file_list.html
|   |       upload_file.html
|   +---notes_app
|   |       add_note.html
|   |       edit_note.html
|   |       note_detail.html
|   |       note_list.html
|   +---users_app
|           login.html
|           logout.html
|           password_reset_done.html
|           password_reset_email.html
|           password_reset_form.html
|           password_reset_request.html
|           profile.html
|           signup.html
|           
+---static
|   |   style.css
|   
+---cloudinary
|   |   __init__.py
|   |   cloudinary_config.py
|   |   cloudinary_utils.py
