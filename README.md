
# TG PLUS

## Features
- Saving deleted messages
- Saving media that can be viewed only 1 time
- Utils commands like:
  - !json -  send json of telegram update
  - !info -  send info about user/chat


## System dependencies
- Python 3.11+
- Docker
- docker-compose
- make
- poetry

## Deployment
### Via [Docker](https://www.docker.com/)
- Rename `.env.dist` to `.env` and configure it
- Create your telegram account session by `tools/create_session.py`
- Put your session file to `src/data/session` folder
- Rename `docker-compose.example.yml` to `docker-compose.yml`
- Run `make app-build` command then `make app-run` to start the tg plus

## Development
### Setup environment

    poetry install


## Used technologies:
- [Pyrogram](https://github.com/KurimuzonAkuma/pyrogram.git) (MTProto framework)
- [PostgreSQL](https://www.postgresql.org/) (database)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) (working with database from Python)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) (lightweight database migration tool)
- [Pydantic](https://docs.pydantic.dev/latest/) (modern data validation library)
