# start by pulling the python image
FROM python:3.8-alpine

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["view.py" ]

#FROM python:3.8-alpine 
#ENV FLASK_APP api.py 
#ENV FLASK_RUN_HOST 0.0.0.0
#RUN apk add --no-cache gcc musl-dev linux-headers 
#COPY ./requirements.txt /zerosum/requirements.txt
#WORKDIR /zerosum
#RUN pip install -r requirements.txt 
#COPY . /zerosum
#RUN pip install -r requirements.txt 
#CMD ["flask","run"]