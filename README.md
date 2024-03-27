# Khutruke - StreamersAlert

StreamersAlert is a platform for Streamers from Nepal who are looking forward to grow their stream using tools and techniqies.

### Build and Start the project

```
docker-compose build
docker-compose run app makemigrations
docker-compose run app migrate
docker-compose run app superuser
docker-compose up -d
```


### Installing Dependencies

Used pip-tools as package manager.

Add package name in `requirements.in` file.

```
docker-compose exec app bash

# Go to project rooot
pip-compile requirements.in
pip-sync requirements.in
```
