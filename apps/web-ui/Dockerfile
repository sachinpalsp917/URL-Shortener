# Stage 1: Builder (Node.js)
FROM node:18-alpine as builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
# Build the static files (Output goes to /app/dist)
RUN npm run build

# Stage 2: Runtime (Nginx)
FROM nginx:alpine
# Copy static files from builder
COPY --from=builder /app/dist /usr/share/nginx/html
# Copy a simple nginx config for the frontend
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]