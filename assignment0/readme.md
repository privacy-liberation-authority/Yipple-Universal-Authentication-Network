# Build 0

Welcome to Build 0. The codebase is laid out in a way that will reflect the later assignments. It may look a little complex at first but we'll guide you through it.

The project is laid out as follows:

## /flaskr

* The python module that contains all the website source files

`/flaskr/app.py`
* This contains the major methods for creating the application and registering endpoints
* It is not important yet

`/flaskr/basic/`
* This is a **blueprint**. It is like a submodule/self-contained flask application
* We will be using blueprints like this for the various parts of your later application
* This is the part you will be modifing today

`/flaskr/basic/views.py`
* This contains all the **routes**. These are the endpoints and the logic behind handling them

`/flaskr/basic/templates`
* This contains the HTML templates that will be access via the routes
* **You will have to modify the correct template here.**

`/flaskr/templates`
* This contains project-wide templates. Typically blueprint templates will inherit from these

`/flaskr/static`
* This will contain any static files you have. Including CSS files, JS files etc

## /tests

* The testing suite. This will include all the necessary tests for the task
* If you pass all the tests, you are likely to pass the assignment for the week and get full marks

## Setup/Running

To setup, we will first create a virtual environment for python3. Much like npm (nodeJS), rvm (ruby), this will avoid polluting your global namespace.

Note, please have python3.5+ installed. We will be testing on python3, not python2. There are compatability differences. If you insist on writing in python2, do note we will not provide any support for unit-testing/auto-marking python2, and you may fail the weekly assignments as result.

These instructions presume you're using a *nix based OS. We provide minimal support for Windows, but it should be largely the same assuming you have Python in your PATH.

```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
pip install -e .

export FLASK_APP=run.py
flask run
```

Now you can access the website at localhost:9447 unless otherwise modified/specified.

## Testing

```
py.test tests
```

If there are no failures. You're good to go.
