ARG DISTRO=alpine:3.10
FROM $DISTRO
# python3 shared with most images
RUN apk add --no-cache \
    python3 py3-pip git bash py3-multidict \
  && pip3 install --upgrade pip

# Shared layer between nginx, dovecot, postfix, postgresql, rspamd, unbound, rainloop, roundcube
RUN pip3 install socrate==0.2.0

# Image specific layers under this line
RUN apk add --no-cache certbot nginx nginx-mod-mail openssl curl \
 && pip3 install watchdog

COPY core/nginx/conf /conf
COPY core/nginx/static /static
COPY core/nginx/*.py /

EXPOSE 80/tcp 443/tcp 110/tcp 143/tcp 465/tcp 587/tcp 993/tcp 995/tcp 25/tcp 10025/tcp 10143/tcp
VOLUME ["/certs"]
VOLUME ["/overrides"]

CMD /start.py

HEALTHCHECK CMD curl -k -f -L http://localhost/health || exit 1
