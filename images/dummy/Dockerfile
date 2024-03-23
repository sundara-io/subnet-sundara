FROM docker.m.daocloud.io/python:3.10

ENV TZ 'Asia/Shanghai'
ENV PYTHONUNBUFFERED '1'

WORKDIR /app

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt -i https://mirrors.ustc.edu.cn/pypi/web/simple

COPY . /app

CMD ["python", "run.py"]