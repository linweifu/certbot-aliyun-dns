FROM certbot/certbot
ENV PATH=$pwd:$PATH
ADD alidns.py alidns.py
