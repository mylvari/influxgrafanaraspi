from python:3-alpine

WORKDIR /usr/src/stockapp
ADD requirements.txt /usr/src/stockapp/
RUN pip install -r /usr/src/stockapp/requirements.txt

ADD ./ /usr/src/stockapp/

CMD [ "python", "stockLogger.py" ]