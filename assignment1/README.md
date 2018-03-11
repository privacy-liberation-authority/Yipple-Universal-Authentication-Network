# Build 1 - COMP6443

Your task is to complete the registration and login components of this banking application.

## Install

```shell
virtualenv env
source env/bin/activate
pip install -r requirements.txt
pip install -e .

export FLASK_APP=run.py
flask run
```

## Specification

### Register

The register logic is contained within `flaskr/basic/views.py` and `flaskr/models.py`. You are specifically required to complete the `registerUser` and `register` functions. 

- On successful registration, you should:
    - Redirect to the login page
- On unsuccessful registration, you should:
    - Notify the user that username is taken with a 400 return code if that is the case
    - Notify the user of a general failure with a 500 return code

### Login

The login logic is contained within `flaskr/basic/views.py` and `flaskr/models.py`. You are specifically required to complete the `validateUser` and `login` functions. 

- On successful login, you should:
    - Store the logged in username in `session['username']`
    - Redirect to `/users/me`
- On unsuccessful login, you should:
    - Display a 403

#### Model Logic

You should do your model edits like so:

```python
def doWork(questionable_argument):
    komrade = KomradeConfig("user")

    data = komrade.read()

    data['things'] = questionable_argument

    komrade.write(data)
```

## Testing

Unit tests can be run through:

```shell
py.test tests -sv
```
