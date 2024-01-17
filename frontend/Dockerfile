# Use an official Node.js runtime as a parent image
FROM node:20.9-bookworm as build

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

# Set the NODE_ENV environment variable to "production"
ENV NODE_ENV=production

## EXPOSE [Port you mentioned in the vite.config file]
EXPOSE 5173

# Start the server
CMD ["npm", "run", "dev"]