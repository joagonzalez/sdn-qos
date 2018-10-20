FROM node:8

RUN mkdir -p /app/src
COPY ./src ./app/src

WORKDIR /app/src

RUN npm install

CMD ["npm", "start"]
