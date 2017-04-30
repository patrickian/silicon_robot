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
__user List__ </br>
`/api/v1/users/`</br>
__signup__</br>
`/api/v1/users/user_signup/`</br>
__activate__</br>
`/api/v1/users/{pk}/activate/`</br>
__login__</br>
`/api/v1/users/user_login/`</br>
__change password__</br>
`/api/v1/users/change_password/`
