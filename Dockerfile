# pull official base image
FROM python:3.11

# set work directory
WORKDIR /code

# install dependencies
RUN pip install --upgrade pip
COPY poetry.lock pyproject.toml /code/
RUN pip install poetry && poetry install --no-root


# copy project
COPY . /code/