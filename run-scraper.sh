#!/bin/bash

IMAGE_NAME="scraper:latest" 
DOCKERFILE_PATH="./scraping" 
ENV_FILE="./db.env" 
CRON_JOB="0 */12 * * * docker run --rm --env-file $ENV_FILE $IMAGE_NAME"

docker build -t $IMAGE_NAME -f $DOCKERFILE_PATH .

docker run --rm --env-file $ENV_FILE $IMAGE_NAME

(crontab -l | grep -q "$CRON_JOB") || (echo "$CRON_JOB" | crontab -)
