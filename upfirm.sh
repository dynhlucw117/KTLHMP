#!/bin/bash
echo "httpd -k"> /tmp/s
echo "sleep 10">> /tmp/s
echo "httpd -r&">> /tmp/s
echo "sleep 10">> /tmp/s
echo "httpd -k">> /tmp/s
echo "sleep 10">> /tmp/s
echo "httpd -f">> /tmp/s
sh /tmp/s
