FROM openjdk:8-jdk
RUN apt-get update && apt-get install -y git ant python3 curl && rm -rf /var/lib/apt/lists/*
WORKDIR /opt
RUN git clone https://github.com/floodlight/floodlight.git
WORKDIR /opt/floodlight
RUN ant
EXPOSE 8080 6653 6633
CMD ["java", "-jar", "target/floodlight.jar"]
