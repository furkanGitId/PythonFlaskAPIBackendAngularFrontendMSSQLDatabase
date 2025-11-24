# ---------- Build Angular App ----------
FROM node:20-alpine AS build
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build


# ---------- Nginx Stage ----------
FROM nginx:alpine

# Remove default config
RUN rm -f /etc/nginx/conf.d/default.conf
RUN rm -rf /usr/share/nginx/html/*

# Copy Angular build output
COPY --from=build /app/dist/my-app/browser/ /usr/share/nginx/html


# Copy Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose Angular UI port
EXPOSE 4200

CMD ["nginx", "-g", "daemon off;"]
