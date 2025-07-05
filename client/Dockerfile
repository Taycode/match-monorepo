# Use an official Node.js runtime as a parent image
FROM node:20-alpine

# Set the working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production=false

# Copy source code including .env file
COPY . .

# Build the application (Vite will automatically pick up .env file)
RUN npm run build

# Install serve globally
RUN npm install -g serve

# Expose port
EXPOSE 5222

# Start the application
CMD ["serve", "-s", "dist", "-l", "5222"]
