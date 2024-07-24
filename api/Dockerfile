FROM python:alpine as builder

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]
CMD ["api.py"]