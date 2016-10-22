FROM pyramid

COPY production.ini dist/easytan-1.0.tar.gz ./
RUN pip install easytan-1.0.tar.gz
VOLUME /db
USER pyramid
EXPOSE 9876
ENTRYPOINT gunicorn --workers=3 --paster production.ini
