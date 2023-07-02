#!/bin/bash

# example: ./start.sh frontend.localhost backend.localhost http

# exit on fail
set -e

FRONTEND_DOMAIN=$1
BACKEND_DOMAIN=$2
HTTP=$3

# set domains needed in docker-compose
export FRONTEND_DOMAIN=$FRONTEND_DOMAIN
export BACKEND_DOMAIN=$BACKEND_DOMAIN

# set backend api url in frontend
grep -qxF "REACT_APP_BACKEND_BASE_URL=$HTTP://$BACKEND_DOMAIN"/api ./frontend/.env || echo "REACT_APP_BACKEND_BASE_URL=$HTTP://$BACKEND_DOMAIN"/api >> ./frontend/.env

# add backend domain to allowed hosts
sed -i "s/ALLOWED_HOSTS = \[.*\]/ALLOWED_HOSTS = ['$BACKEND_DOMAIN']/" ./backend/api/settings.py

# add frontend domain to CORS origin whitelist in backend
sed -i "s/CORS_ORIGIN_WHITELIST = \[.*\]/CORS_ORIGIN_WHITELIST = ['$HTTP:\/\/$FRONTEND_DOMAIN']/" ./backend/api/settings.py

# build images
docker build -t starting-page-frontend ./frontend
docker build -t starting-page-backend ./backend

# start application
docker compose up -d
