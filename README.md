# LayrD Server

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Built Using](#built_using)

## About <a name = "about"></a>

Layrd is a social platform that connects unique ideas with the ideal collaborators for academic initiatives.

## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

##### Isolated python environment setup

Install [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)

Install python 3.11 using pyenv 
```
pyenv install 3.11
```

Install [pipx](https://github.com/pypa/pipx)

Install virtual env using pipx

```
pipx install virtual env
```

Create virtual env

```
virtualenv .venv
```

### Installing

Activate the environment
```
source .venv/bin/activate
```

Install required packages
```
source ./install.sh
```

### Run migrations


```
alembic upgrade head
```

## Usage <a name = "usage"></a>

After running the migrations, to start the server

```
python3 app.py
```

The `.env` file must be present to run the server, `.env` format speicified in [.env_examples](./.env_example)


## ⛏️ Built Using <a name = "built_using"></a>

- [Python](https://www.python.org) - Language
- [pipx](https://github.com/pypa/pipx) - Environment
- [AWS RDS MySQL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.MySQL.html) - Database
- [Flask](https://flask.palletsprojects.com/en/3.0.x/) - Server Framework
