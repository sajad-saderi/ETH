FROM alpine

ENV APP=/cross-secrecy
ENV ADMINPANEL=/cross-secrecy/adminpanel
ENV DATA=/cross-secrecy/data
ENV DATABASE=/cross-secrecy/database

ENV LIBRARY_PATH=/lib:/usr/lib

RUN mkdir $APP $ADMINPANEL $DATA $DATABASE
WORKDIR $APP

RUN apk update && apk upgrade && apk add --no-cache python3 py3-pip build-base python3-dev zlib-dev jpeg-dev libffi-dev cairo-dev cairo cairo-tools freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
RUN pip3 install --upgrade pip && pip3 install --upgrade setuptools wheel

COPY adminpanel/* $ADMINPANEL/
COPY setup.py $APP/

RUN python3 setup.py install

COPY ./data/ $APP/data/

ENTRYPOINT cross-secrecy-servers --data=$DATA --logging=$LOGGING --database=$DATABASE/database.sqlite3
