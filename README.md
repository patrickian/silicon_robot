# silicon_robot

## Description
An application consist of the following endpoints: get current users, login, signup, email activation , change password.

## Requirements
Copy `keys.json.example` in the `config/` folder of the app and rename it as `keys.json`. Fillup and replace the 
following fields with the appropriate data.

## Run
Run the following commands to install dependencies.
```
pip install -r requirements.txt
python manage.py migrate --settings=config.settings
python manage.py runserver --settings=config.settings
```
## Endpoints
__user List__
`/api/v1/users/`
__signup__
`/api/v1/users/user_signup/`
__activate__
`/api/v1/users/{pk}/activate/`
__login__
`/api/v1/users/user_login/`
__change password__
`/api/v1/users/change_password/`
