#!/bin/bash
sshpass -p "$1" scp  -o "StrictHostKeyChecking no" ../backend.tgz root@164.90.165.230:/root/wtd
sshpass -p "$1" ssh -o "StrictHostKeyChecking no" root@164.90.165.230 "cd wtd && \
docker-compose down && \
docker rmi wtd_backend  && \
rm -rf wtd-backend && \
tar -xvf backend.tgz && \
rm backend.tgz && \
docker-compose up -d && \
cp wtd-backend/nginx/default.conf /var/lib/docker/volumes/wtd_wtd-nginx/_data/ && \
docker restart nginx"
