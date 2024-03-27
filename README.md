# Stone on fire

Stone on fire is a platform from where, owner of a restaurant or cafe owner can connect with customers.

And customers can make booking and can check what restaurant / Cafe has to offer.

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

# Go to project root
pip-compile requirements.in
pip-sync requirements.in
```
