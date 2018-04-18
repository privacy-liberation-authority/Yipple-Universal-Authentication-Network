# SECedu COMP6443 
# Python WebApp Dockerfile

FROM python:3.6-alpine

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

CMD ["./run.py"]
EXPOSE 9447
