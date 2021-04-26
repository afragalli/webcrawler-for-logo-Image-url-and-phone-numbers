FROM python:3.8

COPY webcrawler.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD [ "python", "./webcrawler.py"]