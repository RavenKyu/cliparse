FROM python:3.7.7-alpine3.11

# ==============================================================================
# 타임존 설정
RUN apk add tzdata && \
    cp /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    echo "Asia/Seoul" > /etc/timezone

ENV PYTHONUNBUFFERED=0
ENV TABULATE_INSTALL="lib-only pip install tabulate"
# ==============================================================================
RUN mkdir -p /src/cliparse
ADD cliparse /src

# ==============================================================================
# 파일 복사

ADD . /src
WORKDIR /src

# ==============================================================================
# 설치
RUN python setup.py install

# ==============================================================================
# 설치파일 정리
WORKDIR /root
RUN rm -rf /src

VOLUME ["/root"]
ENTRYPOINT ["python" , "-m", "cliparse"]