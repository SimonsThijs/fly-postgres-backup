FROM python:3.8-slim-buster
ENV LANG C.UTF-8

RUN apt-get -y update && apt-get -y autoremove

RUN mkdir /app
WORKDIR /app

RUN apt-get install -y python python-pip python-dev libpq-dev curl wget lsb-release

# install fly
RUN curl -L https://fly.io/install.sh | sh
ENV FLYCTL_INSTALL="/root/.fly"
ENV PATH="$FLYCTL_INSTALL/bin:$PATH"
RUN echo 'export PATH="$FLYCTL_INSTALL/bin:$PATH"' >> /root/.bash_profile

# install pg_dump that supports postgres 15
# Create the file repository configuration:
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update
RUN apt-get install -y postgresql-client-15

# install cron
# Latest releases available at https://github.com/aptible/supercronic/releases
ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.2.1/supercronic-linux-amd64 \
    SUPERCRONIC=supercronic-linux-amd64 \
    SUPERCRONIC_SHA1SUM=d7f4c0886eb85249ad05ed592902fa6865bb9d70

RUN curl -fsSLO "$SUPERCRONIC_URL" \
 && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
 && chmod +x "$SUPERCRONIC" \
 && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
 && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic

# You might need to change this depending on where your crontab is located
COPY crontab crontab


ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
ADD . /app

EXPOSE 8000

ADD run.sh /app/
RUN chmod +x /app/run.sh
CMD /app/run.sh