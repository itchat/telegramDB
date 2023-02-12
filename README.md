# Telegram Notes Bot

## The release process for versions

### Python Virtual Environment

```shell
docker run -itd --name mysql -p 127.0.0.1:3306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql:8.0
pip install virtualenv
virtualenv venv
# Windows：
venv\Scripts\activate
# Linux/MacOS：
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

Exit the virtual environment after configuring the relevant dependencies by entering `deactivate`

### .gitignore

```txt
.gitignore

# Virtual Environment
venv/

# PyCharm
.idea/

# Python cache files
__pycache__/
```

## Daemon management

```shell
vim /etc/systemd/system/telegram.service

[Unit]
Description=Notes
After=network.target

[Service]
User=root
WorkingDirectory=/root/telegramDB
ExecStart=python3 main.py -venv venv
Restart=always
Environment=ID=YOUR_TELEGRAM_ID
Environment=PASS=YOUR_DATABASE_PASS
Environment=TOKEN=YOUR_BOT_TOKEN

[Install]
WantedBy=multi-user.target 
```

## Solving the issue of ineffective firewall in Docker

UFW is a popular iptables front-end on Ubuntu, which makes it very convenient to manage firewall rules. However, when Docker is installed, UFW cannot manage the ports published by Docker. Here is a graceful solution to this kind of problem.

```shell
vim /etc/ufw/after.rules

# BEGIN UFW AND DOCKER
*filter
:ufw-user-forward - [0:0]
:DOCKER-USER - [0:0]
-A DOCKER-USER -j RETURN -s 10.0.0.0/8
-A DOCKER-USER -j RETURN -s 172.16.0.0/12
-A DOCKER-USER -j RETURN -s 192.168.0.0/16

-A DOCKER-USER -j ufw-user-forward

-A DOCKER-USER -j DROP -p tcp -m tcp --tcp-flags FIN,SYN,RST,ACK SYN -d 192.168.0.0/16
-A DOCKER-USER -j DROP -p tcp -m tcp --tcp-flags FIN,SYN,RST,ACK SYN -d 10.0.0.0/8
-A DOCKER-USER -j DROP -p tcp -m tcp --tcp-flags FIN,SYN,RST,ACK SYN -d 172.16.0.0/12
-A DOCKER-USER -j DROP -p udp -m udp --dport 0:32767 -d 192.168.0.0/16
-A DOCKER-USER -j DROP -p udp -m udp --dport 0:32767 -d 10.0.0.0/8
-A DOCKER-USER -j DROP -p udp -m udp --dport 0:32767 -d 172.16.0.0/12

-A DOCKER-USER -j RETURN
COMMIT
# END UFW AND DOCKER
```

```shell
systemctl restart ufw
ufw route allow proto tcp from any to any port 3306
ufw route delete allow proto tcp from any to any port 3306
```

```shell
docker cp tgdb.sql mysql:/root/
docker exec -t mysql bash -c "mysql -uroot -p123456 < /root/tgdb.sql"
```

```shell
# Clean all Docker container and images
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)

# Create Backup task sh
docker exec -it mysql bash -c "mysqldump -uroot -p123456 tgdb > tgbackup.sql"
docker cp mysql:tgbackup.sql /opt/backup

# Crontab
0 0 * * * /bin/sh /opt/backup.sh
```

## Reference

[Resolving UFW and Docker security issues without disabling iptables](https://chaifeng.com/to-fix-ufw-and-docker-security-flaw-without-disabling-iptables/)