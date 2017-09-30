# Readme
### Psuedo Credit Card/Banking App
Note: This readme assumes a shallow of Bakus-Naur documentation comprehension.

---
This app is to simulate credit card transactions, customer purchases for now, and displays them on their account ledger. Most of the endpoints are raw JSON, with the exception of the **accounts/<account_id>/ledgers** endpoint, which is a basic template showing the transactions.

### How to set up to run
This application uses Django with a postgresql database. I chose postgres as sqlite has concurrency lock.

I will assume familiarity and full setup of:

1. Git installed onto your local machine and basic git command usage.
2. pip
2. Virtualenvs/Virtualenv wrappers (the latter keeps virtualenvs in a common location).
3. Postgres installation
3. Unix-based commands (MacOS/*nix)

**Git Stuff**

In order to use this app, clone this repository onto your local machine (say, via terminal): `git clone <repository git clone link.git>`.

**Pre-Django Setup**

From there, create a virtual environment `virtualenv <your name of choice>` and assuming you're still on root directory as your virtualenv activate the environment via `source <your name of choice>/bin/activate`.

Install the banking app's requirements. Go to (`cd`) the root directory of `requirements.txt` in the banking app and to install use `pip install -r requirements.txt`.

**PostgreSQL Setup**

I'll assume [postgresql has been installed](https://www.postgresql.org/download/) onto the system and won't go into installation instructions. If you're on a mac, you can install homebrew to then install postgresql. 

Go into postgresql by typing in `psql` into terminal.

Then:

```
CREATE DATABASE banking;
CREATE USER myprojectuser WITH PASSWORD 'password';
```
where **myprojectuser** is your username of choice, **password** is your password of choice.
Then `\q` to get out of psql when finished.

**Django settings.py configuration for Postgres.**

Open core_banking/settings.py into a text editor and change **USER**, **PASSWORD** to your username and password you use for postgresql. Change the other dictionary keys if necessary. See below:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'banking',
        'USER': 'Munnu',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

**Django Server Run**

Upon success with the prior activities, run django, `cd` to the root directory of **manage.py** and type into terminal

```
python manage.py makemigrations 
python manage.py migrate
python manage.py runserver
```
Upon success, the application will assume localhost:8000 as the URI. This can be verified upon `runserver`'s success message: **Starting development server at http://127.0.0.1:8000/** Launch this into your browser and you're good to go.

### Important Endpoints

#### /health/ 
- **GET** endpoint, returns an HTTP 200 if the server is up and running

#### /accounts/ 
- **POST** endpoint for creating a new customer with an account, and initialize their 0th transaction (new customer) into the database. Returns back the account number as an integer in JSON format.
#### /accounts/<account_id>
- **GET** endpoint for viewing account data of a single customer. Will return back all customer transactions with respect to time of transaction, principal balance, and account id.
#### /accounts/<account_id>/ledgers 
- **GET** endpoint for viewing account transactions (purchases for now are the only type that is currently processed) in a graphical form.

#### /transactions/ 
- **POST** endpoint for submitting transactions for a single account.

### important cURL commands (POST)
I'll ignore GET as that's more or less something like `curl -G <url_with_endpoint_here>`, in this case <url_with_endpoint_here> woild be something like localhost:8000 or localhost:8000/accounts/1, for instance.

For creating a new customer account:
`curl -X POST localhost:8000/accounts/`

For creating a transaction of $50 to that account
`curl --data '{"account_id":<account_id_here>, "purchase_amount":50}' localhost:8000/transactions/` change **<account_id_here>** with the account ID that's currently registered in the database/provided in the prior POST request for creating a new customer account.


