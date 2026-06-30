FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y mininet openvswitch-switch openvswitch-common iputils-ping net-tools curl python3 python3-pip && pip3 install requests && rm -rf /var/lib/apt/lists/*
WORKDIR /scripts
CMD ["bash"]
