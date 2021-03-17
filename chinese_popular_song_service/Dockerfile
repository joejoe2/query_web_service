FROM joejoe2/ub_py3:01

COPY . /app

WORKDIR /app

RUN apt-get update && \
    apt-get -y install sqlite3 && \
    pip3 install -r requirements.txt

ENV LC_ALL C.UTF-8

EXPOSE 8000

ENTRYPOINT ["gunicorn"]

CMD ["app:app","-w","2","--threads","2"]