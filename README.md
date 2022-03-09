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
  $ pipenv install -r "requirements.txt"
```

### Step 2: Run development server

```bash
  $ uvicorn app.main:app --reload
```

### For API documentation

`http://127.0.0.1:8000/docs`
