#!/bin/bash
# ============================================================
# Name: PG_SICP_PRCSE_Group4_C1_Ex5.sh
# Description: Process the contents of /etc/shadow and outputs the users whose passwords are about to expire
# Author: Group 4
# Created On: 2024-11-15
# Last Modified: 2024-11-15
# Usage: ./PG_SICP_PRCSE_Group4_C1_Ex5.sh 
# ============================================================

#Para teste:
# Criar um novo usuário temporario e definir a expiração da password para amanha 
#sudo useradd -e $(date -d "tomorrow" +%Y-%m-%d) user_test
#sudo passwd user_test #temos de inserir manualmente uma password para o user_test
#sudo chage -d $(date +%Y-%m-%d) -M 1 user_test


# Adicionar a data e hora atuais ao log para facilitar a consulta 
echo "Log Date: $(date '+%Y-%m-%d %H:%M:%S')" 
 
current_date_sec=$(date +%s) #Para se comparar a data atual com a as datas de /etc/shadow, é necessario obter, primeiramente, os dias desde Jan 1, 1970 em segundos
current_date_days=$((current_date_sec / 86400 )) #Converter a data atual de segundos para dias atraves da divisao pelo numero de segundos num dia 60*60*24=86400

while IFS=: read -r username password last_ch min_days max_days days2dis days_dis; do 
    
    #echo  "username: $username"

    exp_days=$((last_ch + max_days))

    #echo "exp days: $exp_days"
    #echo "current_date_days: $current_date_days"

    if (( exp_days >= current_date_days && exp_days <= current_date_days + 3 )); then
        echo "The password of user $username is about to expire in $((exp_days - current_date_days))"
    fi

done < /etc/shadow



#Para executar, automatizando com o crontab:
#chmod u+x PG_SICP_PRCSE_Group4_C1_Ex5.sh
#sudo ./PG_SICP_PRCSE_Group4_C1_Ex5.sh
#sudo crontab -e
#55 23 * * * /path/to/PG_SICP_PRCSE_Group4_C1_Ex5.sh >> /path/to/password_notices.log