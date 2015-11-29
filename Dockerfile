FROM alpine

# ENV http_proxy='http://proxy2.justice.gouv.fr:8080'
# ENV https_proxy='http://proxy2.justice.gouv.fr:8080'
# ENV ftp_proxy='http://proxy2.justice.gouv.fr:8080'

RUN echo "http://dl-4.alpinelinux.org/alpine/edge/main" > /etc/apk/repositories ; \
    echo "@edge http://dl-4.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
RUN apk --update add python py-pip py-psycopg2@edge py-pyramid@edge \
    py-sqlalchemy@edge py-gunicorn py-mako@edge
RUN echo -e "import sys\nreload(sys)\nsys.setdefaultencoding('utf8')\n" > /usr/lib/python2.7/sitecustomize.py
RUN adduser -u 50000 -D -H pyramid
COPY . /app
WORKDIR /app
VOLUME /db
RUN pip install -e '.'
USER pyramid
EXPOSE 9876
ENTRYPOINT gunicorn --paster development.ini
