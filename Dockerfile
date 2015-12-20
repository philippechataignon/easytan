FROM alpine

RUN echo "http://dl-4.alpinelinux.org/alpine/v3.3/main" > /etc/apk/repositories ; \
    echo "@community http://dl-4.alpinelinux.org/alpine/v3.3/community" >> /etc/apk/repositories ; \
    echo "@edge http://dl-4.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
RUN apk --update add python py-pip py-psycopg2@edge py-pyramid@edge \
    py-sqlalchemy@edge py-gunicorn py-mako py-zope-component@community
RUN echo -e "import sys\nreload(sys)\nsys.setdefaultencoding('utf8')\n" > /usr/lib/python2.7/sitecustomize.py
RUN adduser -u 50000 -D -H pyramid
COPY . /app
WORKDIR /app
VOLUME /db
RUN pip install -e '.'
RUN chown pyramid: /app/easytan/templates/__compile__/
USER pyramid
EXPOSE 9876
ENTRYPOINT gunicorn --workers=3 --paster production.ini
