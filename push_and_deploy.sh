#!/bin/bash

# Remote server details
remote_server="ec2-18-183-74-167.ap-northeast-1.compute.amazonaws.com"
remote_user="ubuntu"
ssh_file_path="~/.ssh/aws_admin.pem"
# remote_password="your_password"
remote_port="22"
git push origin master
# SSH into the remote server
# sshpass -p "$remote_password" ssh -p $remote_port $remote_user@$remote_server << EOF
ssh -i $ssh_file_path $remote_user@$remote_server << EOF

  # Run your commands here
  sudo su
  cd /opt/stone-on-fire/
  git stash
  git pull origin master
  git stash pop
  docker-compose down && docker-compose up -d && docker-compose ps
EOF
