FROM nginx:1.17.1

## Copy our default nginx config
COPY /root/wtd/wtd-backend/nginx/default.conf /etc/nginx/conf.d/


CMD ["nginx", "-g", "daemon off;"]