# Stage 1: Build the Vue app
FROM node:18-alpine AS builder

WORKDIR /app
COPY src/webapp-frontend/app /app
RUN npm install
RUN npm run build

# Stage 2: Build the final Caddy image
FROM caddy:2.9.1-alpine

# Copy Caddyfile
COPY config/Caddyfile /etc/caddy/Caddyfile

# Copy the built web app into the Caddy web root
COPY --from=builder /app/dist /srv