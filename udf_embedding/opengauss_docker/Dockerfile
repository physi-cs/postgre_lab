FROM centos/python-38-centos7

COPY openGauss-5.1.0-pl-CentOS-64bit.tar.bz2
COPY gosu-amd64 /usr/local/bin/gosu

ENV LANG en_US.utf8

#RUN yum install -y epel-release

USER root

RUN ln -s /opt/rh/rh-python38/root/usr/lib64/libpython3.so.rh-python38 /opt/rh/rh-python38/root/usr/lib64/libpython3.so
RUN pip install pyarrow
RUN set -eux; \
    yum install -y bzip2 bzip2-devel curl libaio&& \
    groupadd -g 70 omm;  \
    useradd -u 70 -g omm -d /home/omm omm;  \
    mkdir -p /var/lib/opengauss && \
    mkdir -p /usr/local/opengauss && \
    mkdir -p /var/run/opengauss  && \
    mkdir /docker-entrypoint-initdb.d && \
    tar -jxf openGauss-5.1.0-pl-CentOS-64bit.tar.bz2 -C /usr/local/opengauss && \
    chown -R omm:omm /var/run/opengauss && chown -R omm:omm /usr/local/opengauss && chown -R omm:omm /var/lib/opengauss &&  chown -R omm:omm /docker-entrypoint-initdb.d && \
    chmod 2777 /var/run/opengauss && \
    rm -rf openGauss-5.1.0-pl-CentOS-64bit.tar.bz2 && yum clean all

RUN set -eux; \
    echo "export GAUSSHOME=/usr/local/opengauss"  >> /home/omm/.bashrc && \
    echo "export PATH=\$GAUSSHOME/bin:\$PATH " >> /home/omm/.bashrc && \
    echo "export LD_LIBRARY_PATH=\$GAUSSHOME/lib:\$LD_LIBRARY_PATH" >> /home/omm/.bashrc

ENV GOSU_VERSION 1.12
RUN set -eux; \
     chmod +x /usr/local/bin/gosu


ENV PGDATA /var/lib/opengauss/data

COPY entrypoint.sh /usr/local/bin/
RUN chmod 755 /usr/local/bin/entrypoint.sh;ln -s /usr/local/bin/entrypoint.sh / # backwards compat

ENTRYPOINT ["entrypoint.sh"]

EXPOSE 5432
CMD ["gaussdb"]
