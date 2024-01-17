# Stage 1: Build the application
# Use an official Node.js runtime as a parent image
FROM node:21.5-bookworm as build-stage

# Set the working directory to /app
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files to the container
COPY . .

# Build the application
RUN npm run build


# Stage 2: Serve the application using Apache
# Use an Apache image
FROM httpd:2.4-bookworm

# Copy the build output from the build stage to the Apache server directory
COPY --from=build-stage /app/dist/ /usr/local/apache2/htdocs/

# Copy custom httpd.conf file to the Apache configuration directory
COPY ./httpd.conf /usr/local/apache2/conf/httpd.conf
COPY ./.htaccess /usr/local/apache2/htdocs/.htaccess

# Apache runs on port 80 by default, so expose it
EXPOSE 80