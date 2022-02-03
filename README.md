## Backend CRUD API wiht FastAPI and MongoDB

Backend in Python that uses the API [ViaCEP](http://viacep.com.br) to create a simple CRUD with MongoDB integration.

### Install dependencies

```
pip install fastapi uvicorn pydantic pymongo requests pytest pytest-asyncio HTTPX
```

### Run app

```
uvicorn app.main:app --reload
```

### Run test

```
pytest tests --asyncio-mode=strict
```

### P.S.:
To use MongoDB remember to change a URI in the [configuration file](./bootstrap/mongodb.py#L6)

#### Thanks for coming this far! ❤️