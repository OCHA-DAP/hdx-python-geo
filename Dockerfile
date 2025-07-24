FROM public.ecr.aws/unocha/python:3.13-stable

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apk add --no-cache --virtual .build-deps \
    build-base \
    gdal-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache

COPY src ./

CMD ["python", "-m", "src.hdx.geo"]
