#!/bin/bash

# Simple Deployment Script for CI-Style Automation

echo " Starting Deployment..."

# 1. Pull latest changes (if in a git repo)
# git pull origin main

# 2. Check if .env exists, if not, copy from example (manual step usually, but automated for demo)
if [ ! -f .env ]; then
    echo " .env file not found. Creating from .env.example..."
    cp .env.example .env
fi

# 3. Build and start services in detached mode
echo " Building and starting containers..."
docker compose -f docker-compose.prod.yml up -d --build

# 4. Clean up unused images/volumes
echo " Cleaning up old images..."
docker image prune -f

echo " Deployment successful!"
echo " Access the app at http://localhost:8081"
