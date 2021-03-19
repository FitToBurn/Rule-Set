#!/bin/bash
green(){
    echo -e "\033[32m\033[01m$1\033[0m"
}
red(){
    echo -e "\033[31m\033[01m$1\033[0m"
}
yellow(){
    echo -e "\033[33m\033[01m$1\033[0m"
}

initialize(){
    systemctl stop firewalld
    systemctl disable firewalld
    CHECK=$(grep SELINUX= /etc/selinux/config | grep -v "#")
    if [ "$CHECK" == "SELINUX=enforcing" ]; then
        sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
        setenforce 0
    fi
    if [ "$CHECK" == "SELINUX=permissive" ]; then
        sed -i 's/SELINUX=permissive/SELINUX=disabled/g' /etc/selinux/config
        setenforce 0
    fi
    yum -y install bind-utils wget unzip zip curl tar
}

cert(){
    green "=============================="
    yellow "Enter the current domain of you VPS:"
    green "=============================="
    read your_domain
    real_addr=`ping ${your_domain} -c 1 | sed '1{s/[^(]*(//;s/).*//;q}'`
    local_addr=`curl ipv4.icanhazip.com`
    if [ $real_addr == $local_addr ] ; then
        green "=========================================="
        rpm -Uvh http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm
            yum install -y nginx
        systemctl enable nginx.service
        #设置伪装站
        rm -rf /usr/share/nginx/html/*
        cd /usr/share/nginx/html/
        wget https://github.com/atrandys/v2ray-ws-tls/raw/master/web.zip
            unzip web.zip
        systemctl restart nginx.service
        #申请https证书
        mkdir /usr/src/cert
        curl https://get.acme.sh | sh
        ~/.acme.sh/acme.sh  --issue  -d $your_domain  --webroot /usr/share/nginx/html/
            ~/.acme.sh/acme.sh  --installcert  -d  $your_domain   \
            --key-file   /usr/src/cert/private.key \
            --fullchain-file /usr/src/cert/fullchain.cer \
            --reloadcmd  "systemctl force-reload  nginx.service"
        if test -s /usr/src/cert/fullchain.cer; then
            green "======="
            green "安装成功"
            green "======="
        else
            red "================================"
            red "https证书没有申请成果，本次安装失败"
            red "================================"
        fi
	
    else
        red "================================"
        red "域名解析地址与本VPS IP地址不一致"
        red "本次安装失败，请确保域名解析正常"
        red "================================"
    fi
}

install_docker(){
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl start docker
    systemctl enable docker
    systemctl enable containerd
    docker pull portainer/portainer:latest
    docker volume create portainer_data
    docker run -d -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer
    docker pull v2fly/v2fly-core
    docker volume create v2fly_config
    trojan_passwd=$(cat /dev/urandom | head -1 | md5sum | head -c 8)
	cat > /var/lib/docker/volumes/v2fly_config/config.json <<-EOF
{
  "log": {
    "loglevel": "warning"
  },
  "inbounds": [
    {
      "listen": "0.0.0.0",
      "port": 443, 
      "protocol": "trojan",
      "settings": {
        "clients":[{"password": "$trojan_passwd"}],
        "fallbacks": [{"dest": 9000}]
      },
      "streamSettings": {
        "network": "tcp",
        "security": "tls",
        "tlsSettings": {
          "alpn": ["http/1.1"],
          "certificates": [{
            "certificateFile": "/cert/fullchain.cer",
            "keyFile": "/cert/privkey.key"
          }]
        }
      }
    }
  ],
  "outbounds": [{ 
    "protocol": "freedom"
  }]
}
EOF
    docker run -d --network=host --name=v2fly --restart=always -v /var/lib/docker/volumes/v2fly_config/config.json:/etc/v2ray/config.json -v /usr/src/cert:/cert v2fly/v2fly-core

}



start_menu(){
    initialize
    clear
    green " ===================================="
    green " ===================================="
    echo
    green " 1. 安装/更新证书"
    red " 2. 卸载trojan"
    yellow " 0. 退出脚本"
    echo
    read -p "Enter a number:" num
    case "$num" in
    1)
    cert
    install_docker
    ;;
    2)
    ;;
    0)
    exit 1
    ;;
    *)
    clear
    red "Please enter a correct number"
    sleep 1s
    start_menu
    ;;
    esac
}

start_menu