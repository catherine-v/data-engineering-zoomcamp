FROM python:3.9.1

RUN apt-get install wget

WORKDIR /app
COPY upload_data.py requirements.txt ./
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "upload_data.py" ]
