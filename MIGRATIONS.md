### create a migrations
```
alembic revision -m "your migration name"
```

### migrate up
```
alembic upgrade +1
```

### migrate down
```
alembic downgrade -1
```