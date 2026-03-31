FROM alpine:latest

RUN apk add --no-cache bash curl jq python3 py3-pip py3-mutagen ffmpeg tzdata

RUN wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp && \
    chmod a+rx /usr/local/bin/yt-dlp

WORKDIR /app

COPY crontab /etc/crontabs/root
COPY scripts/ /app/scripts/
RUN chmod +x /app/scripts/*.sh

CMD ["crond", "-f", "-d", "8"]