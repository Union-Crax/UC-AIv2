FROM node:18-slim

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY index.js .

# Copy environment file
COPY .env .env

# Run the bot
CMD ["npm", "start"]