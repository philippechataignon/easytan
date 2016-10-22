FROM alpine

RUN echo "http://dl-4.alpinelinux.org/alpine/v3.4/main" > /etc/apk/repositories
RUN apk --update add python py-pip py-psycopg2 py-requests py-gunicorn py-mako
RUN echo -e "import sys\nreload(sys)\nsys.setdefaultencoding('utf8')\n" > /usr/lib/python2.7/sitecustomize.py
RUN adduser -u 50000 -D -H pyramid
RUN mkdir /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
VOLUME /app
WORKDIR /app
#RUN pip install -e '.'
#RUN chown pyramid: /app/easytan/templates/__compile__/
USER pyramid
EXPOSE 9876
ENTRYPOINT gunicorn --workers=3 --paster production.ini
