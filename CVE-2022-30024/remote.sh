#!/bin/bash

PID=$(ps | ./busybox grep httpd | ./busybox tail -5 | ./busybox head -1 | ./busybox awk '{print $1}')

echo "$PID"