FROM gliderlabs/alpine:3.4

RUN addgroup user
RUN adduser user -D -G user
RUN chown -R user:user /home/user/
RUN mkdir -p /home/user/flask-graph


WORKDIR /home/user/flask-graph
ADD ./ /home/user/flask-graph/

RUN apk add --update python=2.7.12-r0 openssl ca-certificates py-pip libffi-dev openssl-dev 
RUN pip install --upgrade pip
RUN apk --update add --virtual build-dependencies python-dev build-base
RUN pip install -r /home/user/flask-graph/requirements.txt
RUN rm -rf /root/.cache/
RUN apk del build-dependencies

EXPOSE 8888
ENTRYPOINT gunicorn project.main:app -c project.gunicorn
