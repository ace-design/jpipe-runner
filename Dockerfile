FROM python:3.13-alpine

WORKDIR /app

RUN apk add --no-cache gcc musl-dev libffi-dev graphviz graphviz-dev

COPY . .

RUN pip install --no-cache-dir .

ENTRYPOINT ["python", "-m", "jpipe_runner"]
