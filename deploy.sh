#!/bin/bash
sshpass -p "$1" scp  -o "StrictHostKeyChecking no" ../backend.tgz root@164.90.165.230:/root/wtd
sshpass -p "$1" ssh -o "StrictHostKeyChecking no" root@164.90.165.230 "cd wtd && \
docker-compose down && \
docker rmi wtd-backend && \
rm -rf backend && \
tar -xvf backend.tgz && \
rm backend.tgz && \
docker-compose up -d"
