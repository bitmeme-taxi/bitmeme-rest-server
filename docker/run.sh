#!/bin/sh
#docker run --rm supertypo/kaspa-rest-server:latest
export SQL_URI="postgresql+asyncpg://postgres@postgres@172.18.0.1:5432/postgres"
sudo docker run -p 8000:8000 -e VERSION=2.1.0 --rm supertypo/gor-rest-server:latest
