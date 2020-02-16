FROM debian:latest

MAINTAINER Valentin Hubert <valentin.hubert@groupe-nehs.com>

ENV JOB_LAUNCHER_DIRECTORY ./tmp
ENV JOB_LAUNCHER_NUMBER 10

WORKDIR /app

CMD mkdir -p app
COPY ./tests/create_files.sh /app
CMD chmod +X /app/create_files.sh

ENTRYPOINT /app/create_files.sh $JOB_LAUNCHER_DIRECTORY $JOB_LAUNCHER_NUMBER
