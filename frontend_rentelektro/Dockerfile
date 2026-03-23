# Use the official Node.js image as the base image
FROM node:20

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the application code into the container
COPY . .

# Expose port 8080 for the Vite development server
EXPOSE 8080

# Command to run the Vite development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
