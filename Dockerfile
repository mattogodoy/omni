FROM python:3.8-alpine

# Dependencies for psutil lib to work
RUN apk add --update gcc libc-dev linux-headers && rm -rf /var/cache/apk/*

WORKDIR /app

COPY src/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src/main.py src/stats.py ./

CMD [ "python3" , "main.py"]
