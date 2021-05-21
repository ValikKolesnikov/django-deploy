FROM node:alpine

RUN npm install -g serve

WORKDIR /usr/src/app/frontend
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build