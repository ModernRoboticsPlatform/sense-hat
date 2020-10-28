#FROM python:3.9
FROM protik77/python3-sensehat:version-0.2.1

RUN apt-get update && apt-get install -y \
      software-properties-common \
      vim \
      python3-pip

#RUN echo 'syntax on' > ~/.vimrc

#RUN add-apt-repository 'deb http://raspbian.raspberrypi.org/raspbian/ buster main contrib non-free rpi' && \
#    add-apt-repository 'deb http://archive.raspberrypi.org/debian/ buster main' && \
#    wget https://archive.raspbian.org/raspbian.public.key -O - | apt-key add - && \
#    wget http://archive.raspberrypi.org/debian/raspberrypi.gpg.key -O -| apt-key add -

#RUN apt-get update
#RUN apt-get install -y \
#      sense-hat

#RUN useradd -ms /bin/bash pybot
#USER pybot
#WORKDIR /home/pybot

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "./sense.py" ]
