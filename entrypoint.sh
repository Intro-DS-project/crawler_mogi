#!/bin/sh
current_date_time=$(date +'%Y-%m-%d_%H-%M-%S')
scrapy crawl mogi -O "/app/data/${current_date_time}_mogi_output.json"