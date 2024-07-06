# metis_fastapi

<<<<<<< Updated upstream
## Project setup
```
poetry install
```

### Compiles and hot-reloads for development
```
poetry run uvicorn metis_fastapi.main:app --reload
```

Run with some options may be convenient.

### Compiles and minifies for production
```
poetry build
```

=======
The metis_fastapi serves the api for the slow control.

## Requirement
This project uses poetry for version control of modules. Please install poetry first.
For the other dependencies, please refer to pyproject.toml.

## Installation and activation
```shell
redis-server &
git clone http://github.com/rcnp-ws/metis_fastapi.git
cd metis_fastapi
poetry install
poetry run  uvicorn metis_fastapi.main:app --reload --host 0.0.0.0 --port 8000
```

Then you can access http://localhost:8000 from browsers.
For api document, please access http://localhost:8000/docs
>>>>>>> Stashed changes
