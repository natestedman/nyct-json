#!/usr/bin/env bash

protoc --python_out=../src/proto/ gtfs-realtime.proto nyct-subway.proto
