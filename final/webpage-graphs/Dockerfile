# Use an nginx base image
FROM nginx:alpine
COPY . /usr/share/nginx/html

# Copy custom Nginx configuration file
COPY custom.conf /etc/nginx/conf.d/default.conf

# Copy the webpage.html file to the nginx server root directory
COPY webpage.html /usr/share/nginx/html
