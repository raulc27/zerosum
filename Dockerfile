FROM python:3.8-slim-buster
WORKDIR /zerosum
#ENV FLASK_APP api.py
#ENV FLASK_RUN_HOST 0.0.0.0
#RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt
COPY . .
ENTRYPOINT ["python"]
#CMD ["flask","run"]
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
