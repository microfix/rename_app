FROM nginx:alpine

# Copy static files to nginx directory
COPY index.html /usr/share/nginx/html/index.html

# Expose port 80 (standard for Nginx)
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
