# Mediusware Python Intern Exam

## Setting Up the Development Environment

### Creating a Virtual Environment
1. Open your terminal or command prompt.
2. Navigate to the directory where you want to create your project.
3. Run the following command to create a new virtual environment named `env`:
   ```bash
   virtualenv env
   cd env
   cd Scripts
   activate

   pip install django djangorestframework pillow psycopg2-binary django-filter markdown

   git clone https://github.com/akborhossain/mediusware.git

Git repo link 
https://github.com/akborhossain/mediusware.git


4. Use POSTGRESQL as database according to your database change setting.py database section.
5. import task and auth_user table to database.
6. makemigrations and migrate
7. login with admin and password "though" as superuser.


## Only superuser can create, update and delete task. Normal user can see and partial update.