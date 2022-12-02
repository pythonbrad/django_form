# EasyForm
An opensource alternative to Google Form.

## How to deploy
- Download the source code
```sh
git clone https://github.com/pythonbrad/django_form.git
cd django_form
```
- Create a virtual environment
```sh
python3 -m venv .form_venv
source .form_venv/bin/activate
```
- Install the requirements
```sh
pip install -r requirements.txt
```
- Config the environement (.env file)
```sh
cp .env_example .env
```
- Config the database
```sh
python manage.py makemigrations
python manage.py migrate
```