# base image
FROM node:21.6.1-alpine

# set working directory
WORKDIR /usr/src/app

# add `/usr/src/app/node_modules/.bin` to $PATH
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# COPY package-lock.json /usr/src/app/package-lock.json
COPY package*.json /usr/src/app/

# install and cache playola dependencies
RUN npm install

# start playola
CMD ["npm", "run", "dev"]
