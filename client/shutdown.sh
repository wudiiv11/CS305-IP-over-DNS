#! /bin/bash

pkill -f "ssh -tt -i"
unset {http,https,ftp,rsync,all}_proxy {HTTP,HTTPS,FTP,RSYNC,ALL}_PROXY
