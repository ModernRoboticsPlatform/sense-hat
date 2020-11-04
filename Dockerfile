FROM protik77/python3-sensehat:version-0.2.1

RUN apt-get update && apt-get install -y \
      software-properties-common \
      vim \
      python3-pip

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "./sense.py" ]
