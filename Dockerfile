FROM python:3

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "rtsp.py" ]