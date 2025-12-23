FROM node:24-alpine

WORKDIR /app

# copy package files first (Caching)
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose port 3000
EXPOSE 3000

# Run in development Mode
CMD ["npm", "run", "dev"]