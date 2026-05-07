#!/bin/bash
docker run -d -v $PWD:/mosquitto/config -p 1883:1883 --name broker --restart always eclipse-mosquitto