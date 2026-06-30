# NBU SDN Mininet + Floodlight Docker Compose Lab

## Assignment

This repository contains a Docker Compose setup for the semester completion exercise:

- install Docker and learn the basics;
- learn Docker Compose;
- learn Mininet;
- learn the Floodlight SDN controller;
- create a GitHub repository;
- write a Mininet Python script that creates a topology with `<XYZ>` switches and `<YX>` hosts;
- create a Docker Compose stack with Mininet, Floodlight and the custom script;
- configure bidirectional traffic rules between the two most distant hosts using the Floodlight REST API;
- demonstrate connectivity with ping.

## University / Course

- University: New Bulgarian University (NBU)
- Course: Computer Networks
- Lecturer: Nikolay Milovanov
- Student: Aleksandar Slavov

## Faculty number calculation

Faculty number used for the topology: `f119096`

Digits used:

- `Y` = first digit = `1`
- `X` = penultimate digit = `9`
- `Z` = last digit = `6`

Therefore:

- Number of switches `<XYZ>` = `196`
- Number of hosts `<YX>` = `91`

The topology is a chain of 196 OpenFlow switches. The hosts are distributed across the chain. Host `h1` is connected to the first switch and host `h91` is connected to the last switch, so they are the two most distant hosts.

```text
h1 -- s1 -- s2 -- s3 -- ... -- s195 -- s196 -- h91
```

## Files

```text
.
├── docker-compose.yml
├── floodlight/Dockerfile
├── mininet/Dockerfile
├── scripts/topology.py
├── scripts/install_rules.py
├── scripts/demo.sh
└── README.md
```

## How to run

### 1. Build the containers

```bash
docker compose build
```

### 2. Start the stack

```bash
docker compose up -d floodlight mininet
```

Wait 20–40 seconds for Floodlight to start.

### 3. Start Mininet

Open a shell in the Mininet container:

```bash
docker compose exec mininet bash
```

Then run:

```bash
service openvswitch-switch start
python3 /scripts/topology.py
```

This starts the topology and opens the Mininet CLI.

### 4. Install Floodlight traffic rules

Open a second terminal and run:

```bash
docker compose exec mininet bash
python3 /scripts/install_rules.py
```

The script adds bidirectional static flow rules between `h1` and `h91` through the Floodlight REST API.

### 5. Test ping

Go back to the Mininet CLI and run:

```bash
h1 ping -c 3 h91
```

Expected result: ping packets should be exchanged between `h1` and `h91`.

## Floodlight API endpoint

The rules are sent to:

```text
http://floodlight:8080/wm/staticflowpusher/json
```

## YouTube demonstration

Add the screen recording link here:

```text
https://youtube.com/your-video-link
```

Suggested video structure:

1. Show the GitHub repository.
2. Show `docker-compose.yml`.
3. Show `topology.py`.
4. Start the Docker Compose stack.
5. Start Mininet.
6. Run `install_rules.py`.
7. Run `h1 ping -c 3 h91`.
8. Explain that the static rules are installed through the Floodlight REST API.

## Notes

Mininet uses virtual network interfaces and Open vSwitch. Because of this, the Mininet container runs in privileged mode.
