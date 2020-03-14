FROM python:3.8-alpine

WORKDIR /src/

ADD requirements.txt /src/
RUN pip install -r /src/requirements.txt
ADD main.py /src/main.py

CMD /src/main.py