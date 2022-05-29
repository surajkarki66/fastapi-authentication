# fastapi-authentication

## To run the web app locally

### Step 1: Install dependencies

```bash
  $ pip install -r "requirements.txt"
```

OR

```bash
  $ pip install pipenv
  $ pipenv --python 3.X
  $ pipenv shell
  $ pipenv install -r "requirements.txt"
```
### Step2: Install Postgresql locally
### Step3: Create .env file in root directory and add following info.
```
database_hostname=<database-host>
database_port=<database-port>
database_password=<database-password>
database_name=<database-name>
database_username=<database-username>
secret_key=<jwt-secretkey>
algorithm=<algorithm>
jwt_expire_seconds=<jwt-expire>

```


### Step4: Create a database with suitable name in Postgresql

### Step5: Run database migration
```bash
  $ alembic upgrade heads
```

### Step 6: Run development server

```bash
  $ uvicorn app.main:app --reload
```

### For API documentation

`http://127.0.0.1:8000/docs`
