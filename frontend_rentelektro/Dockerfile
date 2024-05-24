# Use the official Node.js image as the base image
FROM node:16

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code into the container
COPY . .

# Expose port 8080 for the Vue.js application
EXPOSE 8080

# Command to build the Vue.js application
CMD ["npm", "run", "build"]

# Dockerfile
# Stage 1 - the build process
#FROM node:16.13 AS build
#WORKDIR /app
#COPY package*.json ./
#RUN npm install
#COPY . .
#RUN npm run build
#
## Stage 2 - the production environment
#FROM nginx:1.25.3
#COPY --from=build /app/dist /usr/share/nginx/html
#EXPOSE 80
#CMD ["nginx", "-g", "daemon off;"]