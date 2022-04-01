###############################################################
#Initial Image
FROM python:3.9.10-slim-bullseye as builder

RUN apt-get update && apt-get install -y bzip2 g++ cmake libsqlite3-dev sqlite3 libtiff-dev \
                                        libssl-dev libcurl4-openssl-dev curl wget g++ cmake

# Compile geos
ENV GEOS_VERSION=3.7.2
RUN wget http://download.osgeo.org/geos/geos-${GEOS_VERSION}.tar.bz2 -P /tmp/resources/ && \
        cd /tmp/resources && \
        tar xjf geos-${GEOS_VERSION}.tar.bz2 && \
        cd geos-${GEOS_VERSION} && \
        ./configure  && \
        make -j4 install

# Compile proj
ENV PROJ_VERSION=8.0.0
RUN wget https://download.osgeo.org/proj/proj-${PROJ_VERSION}.tar.gz -P /tmp/resources/ && \
        cd /tmp/resources && \
        tar xfv proj-${PROJ_VERSION}.tar.gz && \
        cd proj-${PROJ_VERSION} && \
        mkdir build && \
        cd build && \
        cmake .. -DCMAKE_INSTALL_PREFIX=/usr && \
        cmake --build . --parallel 4 && \ 
        cmake --build . --target install
##############################################################
#Final Image
FROM python:3.9.10-slim-bullseye as runner 
WORKDIR /APP
LABEL maintainer="Renato Gomes <renatogomessilverio@gmail.com>"
ENV LANG C.UTF-8

COPY --from=builder  /usr/local/bin/ /usr/local/bin/
COPY --from=builder  /usr/lib /usr/lib
COPY --from=builder   /usr/local/lib /usr/local/lib
COPY --from=builder   /usr/bin /usr/bin

COPY requirements.txt ./
RUN apt-get update && apt-get -y install python3-dev libproj-dev libgeos-dev gcc libpq-dev python-dev libgeos++-dev libproj-dev python3-pip
RUN pip3 install pyshp==2.2.0 shapely==1.8.1 cartopy==0.20.2

RUN pip3 install -r requirements.txt && \
    apt-get update &&  \
    apt-get install -y git vim htop net-tools procps wget curl && \
    rm -rf /var/lib/apt/lists/* && \ 
    apt-get clean autoclean && \
    apt-get autoremove --yes && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/
