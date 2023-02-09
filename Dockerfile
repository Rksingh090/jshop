FROM alpine

RUN apk add --update --no-cache --virtual .tmp gcc g++ python2 py3-pip libc-dev linux-headers \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip3 install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip3 install Pillow \
    && apk del build-deps


COPY ./requirements.txt /app/


RUN pip3 install -r /app/requirements.txt

COPY . /app

WORKDIR /app/

# RUN python3 manage.py makemigrations
# RUN python3 manage.py migrate

EXPOSE 8000

CMD ["python3", "manage.py", "runserver"]

