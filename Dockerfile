FROM python:3.5-alpine
WORKDIR /app/hista
COPY requirements.txt /app/hista

#RUN sed -i '1ihttp://mirrors.ustc.edu.cn/alpine/v3.4/main\' /etc/apk/repositories \
RUN echo 'https://mirrors.tuna.tsinghua.edu.cn/alpine/v3.4/main' > /etc/apk/repositories \
    && apk add --no-cache python3-dev gcc musl-dev postgresql-dev \
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt 

ADD hista.tar.gz /app/hista/
CMD ["python", "index.py"]