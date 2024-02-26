FROM nginx:latest
#VOLUME /etc/letsencrypt/

RUN apt-get update && apt-get install -y certbot python3-certbot-nginx 
RUN apt-get install -y openssl
RUN apt-get install -y certbot

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80 443
COPY index.html /usr/share/nginx/html/index.html

#RUN mkdir -p /etc/letsencrypt/live/selfsigned/
#RUN chmod 755 /etc/letsencrypt/live/selfsigned/
#RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/letsencrypt/live/selfsigned/nginx-selfsigned.key -out /etc/letsencrypt/live/selfsigned/nginx-selfsigned.crt -subj "/C=US/ST=NH/L=Nashua/O=uvdove/CN=www.miasurreal.com" -addext "subjectAltName=DNS:miasurreal.com,DNS:www.miasurreal.com" -addext "extendedKeyUsage=serverAuth" -addext "keyUsage=digitalSignature,keyEncipherment" -addext "basicConstraints=CA:FALSE" -addext "authorityKeyIdentifier=keyid,issuer" -addext "subjectKeyIdentifier=hash" -addext "authorityInfoAccess=OCSP;URI:http://ocsp.int-x3.letsencrypt.org" -addext "crlDistributionPoints=URI:http://crl.int-x3.letsencrypt.org"
#RUN echo "ssl_certificate /etc/letsencrypt/live/selfsigned/nginx-selfsigned.crt;"
#RUN cat /etc/letsencrypt/live/selfsigned/nginx-selfsigned.crt
#RUN echo "ssl_certificate_key /etc/letsencrypt/live/selfsigned/nginx-selfsigned.key;"
#RUN cat /etc/letsencrypt/live/selfsigned/nginx-selfsigned.key
#RUN chown nginx:nginx /etc/letsencrypt/live/selfsigned/nginx-selfsigned.crt /etc/letsencrypt/live/selfsigned/nginx-selfsigned.key 
#USER nginx
#RUN certbot certonly --nginx -d miasurreal.com --non-interactive --agree-tos --email deninnodp@gmail.com --no-eff-email --staging

CMD ["nginx", "-g", "daemon off;"] 
