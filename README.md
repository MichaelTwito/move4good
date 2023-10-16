# Run local with docker
Run:
```
docker-compose up
docker exec -it python_container python app/create_user.py admin admin 1
```

And go to: http://localhost:8000/docs#/ for the docs