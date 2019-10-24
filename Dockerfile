FROM amazonlinux:latest

RUN yum -y update

RUN yum -y install \
python3 \
python3-venv \
python3-dev \
python3-pip \
shadow-utils

COPY requirements.txt requirements.txt
RUN python3 -m venv hireme_venv
RUN hireme_venv/bin/pip install -r requirements.txt
RUN hireme_venv/bin/pip install gunicorn

RUN useradd -ms /bin/bash hireme

COPY hireme/ hireme/

WORKDIR ./hireme/
RUN chmod +x ./boot-app.sh
ENV FLASK_APP wsgi.py

RUN chown -R hireme:hireme ../hireme/
USER hireme

EXPOSE 5000
ENTRYPOINT ["./boot-app.sh"]
