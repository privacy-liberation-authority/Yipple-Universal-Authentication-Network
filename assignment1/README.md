# Build 1 - COMP6443

Your task is to complete the registration and login components of this banking application.

## Set up and install

```shell
git clone git@github.com:sajidanower23/Yipple-Universal-Authentication-Network.git Yipple
cd Yipple/
git remote add pla git@github.com:privacy-liberation-authority/Yipple-Universal-Authentication-Network.git
cd assignment1/
virtualenv env --python=`which python3`
pip install -r requirements.txt
pip install -e . # don't forget the (dot)
source env/bin/activate
```

## Branching out

Once you have the repository downloaded and the setup out of the way,
make your own git branch

```shell
git checkout -b dev-<identity>
```

Note that `identity` here can be anything that can traced back to you.
Initials or first name are commonly used identities for git branches.

## Run

```shell
./run.py
# or
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
