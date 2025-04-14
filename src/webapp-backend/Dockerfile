FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# Maybe in future because it is behind a proxy: "--proxy-headers"
CMD ["fastapi", "run", "app/main.py", "--port", "80"]