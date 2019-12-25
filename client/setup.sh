#! /bin/bash
config="client_settings.properties"

function prop {
	[ -f "$config" ] && grep -P "^\s*[^#]?${1}=.*$" $config | cut -d'=' -f2
}

nohup ssh -tt -i $(prop "ssh_key") -D $(prop "client_tun_port") $(prop "ssh_server") > output.txt 2>&1 &
export ALL_PROXY=$(prop "client_proxy")
# sudo ssh -i cs305dnspro_cn.pem -D 192.168.77.2:8080 ubuntu@192.168.77.10
