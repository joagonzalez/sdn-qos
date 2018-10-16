FROM alpine:latest

RUN echo "http://dl-5.alpinelinux.org/alpine/v3.4/main/" >> /etc/apk/repositories
RUN apk update
RUN apk add less curl nano asterisk asterisk-curl asterisk-speex asterisk-sample-config asterisk-sounds-en
RUN mkdir /conf

ADD /conf/sip.conf /conf/sip_conf
ADD /conf/extensions.conf /conf/extensions_conf
ADD /conf/ari.conf /conf/ari_conf

RUN cat /conf/sip_conf >> /etc/asterisk/sip.conf
RUN cat /conf/extensions_conf >> /etc/asterisk/extensions.conf
RUN cat /conf/ari_conf > /etc/asterisk/ari.conf

RUN echo "noload => res_pjsip.so" >> /etc/asterisk/modules.conf
RUN sed -i '/;enabled=yes/c\enabled=yes' /etc/asterisk/http.conf
RUN sed -i '/bindaddr=127.0.0.1/c\bindaddr=0.0.0.0' /etc/asterisk/http.conf
RUN sed -i '/;bindport=8088/c\bindport=8088' /etc/asterisk/http.conf

CMD ["/usr/sbin/asterisk", "-cvvvv"]
