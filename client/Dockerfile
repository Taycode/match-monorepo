# Development Dockerfile for React/Vite
FROM node:20-alpine

# Set the working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Expose port for dev server
EXPOSE 5173

# Start development server with proper host binding
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
