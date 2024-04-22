# Use an official Node.js runtime as a parent image
FROM node:20-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (if you use npm) or yarn.lock (if you use yarn)
COPY package*.json ./
# If using yarn, you might want to uncomment the next line and comment out the npm install line
# COPY yarn.lock ./

# Install dependencies
RUN npm install
# If you are using yarn, you might use:
# RUN yarn install

# Copy the rest of your app's source code from your host to your image filesystem.
COPY . .

# Build the application using TypeScript and Vite
RUN npm run build
# If using yarn, you might use:
# RUN yarn build

# Install `serve` to run the application (if not already installed globally)
RUN npm install -g serve
# If using yarn, you might use:
# RUN yarn global add serve

# Inform Docker that the container is listening on the specified port at runtime.
EXPOSE 5222

# Run the application using serve
CMD ["serve", "-s", "dist", "-l", "5222"]
