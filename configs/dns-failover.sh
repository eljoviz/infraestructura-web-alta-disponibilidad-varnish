#!/bin/bash
CONF="/etc/failover/failover.conf"
LOG="/var/log/dns-failover.log"
[ -f "$CONF" ] && source "$CONF"

STATE="NORMAL"
FAILS=0

echo "$(date): [INICIO] Watchdog de Failover iniciado. Vigilando $FRONTEND_INTERNAL_IP..." >> "$LOG"

while true; do
    if curl -s -m 2 -I "http://$FRONTEND_INTERNAL_IP:80/" > /dev/null 2>&1; then
        if [ "$STATE" = "FAILOVER" ]; then
            echo "$(date): [RECUPERADO] Frontend Varnish vuelve a responder. Restaurando estado normal..." >> "$LOG"
            STATE="NORMAL"
            FAILS=0
            if [ "$NOIP_USER" != "usuario_aqui" ]; then
                curl -s -u "$NOIP_USER:$NOIP_PASS" "https://dynupdate.no-ip.com/nic/update?hostname=$HOSTNAME&myip=$FRONTEND_PUBLIC_IP" >> "$LOG" 2>&1
            fi
            # Restaurar reglas restrictivas en nftables
            nft -f /etc/nftables.conf
        else
            FAILS=0
        fi
    else
        FAILS=$((FAILS + 1))
        if [ $FAILS -ge $MAX_FAILS ] && [ "$STATE" = "NORMAL" ]; then
            echo "$(date): [ALERTA] Frontend Varnish CAÍDO tras $FAILS intentos fallidos. Activando FAILOVER..." >> "$LOG"
            STATE="FAILOVER"
            # 1. Abrir puertos web en Apache para tráfico público
            nft add rule inet filter input tcp dport { 80, 443 } accept
            # 2. Actualizar DNS en No-IP hacia esta máquina
            if [ "$NOIP_USER" != "usuario_aqui" ]; then
                curl -s -u "$NOIP_USER:$NOIP_PASS" "https://dynupdate.no-ip.com/nic/update?hostname=$HOSTNAME&myip=$BACKEND_PUBLIC_IP" >> "$LOG" 2>&1
            fi
            echo "$(date): [FAILOVER ACTIVO] Dominio $HOSTNAME apuntado a $BACKEND_PUBLIC_IP." >> "$LOG"
        fi
    fi
    sleep $CHECK_INTERVAL
done
