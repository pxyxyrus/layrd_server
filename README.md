
migration

```
alembic revision -m "your migration name"
```

migrate up
```
alembic upgrade head
```

or 

```
alembic upgrade +1
```


migrate down
```
alembic downgrade -1
```



start flask server
```
python3 app.py
```