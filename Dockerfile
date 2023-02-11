FROM python:3.8-alpine
WORKDIR /zerosum
ENV FLASK_APP api.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt /zerosum
COPY . /zerosum
RUN pip install -r requirements.txt
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["flask","run"]