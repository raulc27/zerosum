FROM python:3.8-alpine
WORKDIR /zerosum
ENV FLASK_APP api.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt /zerosum
RUN pip install -r ./requirements.txt
COPY . /zerosum
ENTRYPOINT ["python"]
CMD ["flask","run"]