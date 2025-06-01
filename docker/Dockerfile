FROM ubuntu:latest

RUN apt update
RUN apt install python3 -y
WORKDIR /usr/app/src
COPY test.py ./
RUN apt update
RUN apt install default-jdk -y
COPY . .
RUN javac javatest.java
CMD ["python3", "./test.py"]
CMD ["java", "javatest.java"]