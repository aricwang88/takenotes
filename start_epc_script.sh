#!/bin/bash

EXE_RUN_PATH=`pwd`

if [ $1 = "start" ]; then
    echo 'Setup core network.'
    if [ $2 = 'all' ]; then
        echo '===> Start all nodes in EPC, HSS/SPGW/MME.'
        /usr/bin/xterm -fg Yellow -bg Black -cr DarkRed -e "pushd /home/ehhewng/openair-cn/SCRIPTS/; source ../oaienv; ./run_hss" &
	sleep 1
        /usr/bin/xterm -fg lightgreen -bg Blue -cr red  -e "pushd /home/ehhewng/openair-cn/SCRIPTS/; source ../oaienv; ./run_spgw" &
	sleep 1
        /usr/bin/xterm -fg LightYellow -bg Orange -cr red -e "pushd /home/ehhewng/openair-cn/SCRIPTS/; source ../oaienv; ./run_mme" &
	sleep 1
	/usr/bin/xterm -fg LightGreen -bg black -cr red -e "tailf /tmp/mme.log" &

    fi
    
    if [ $2 = 'hss' ]; then
	echo 'Start HSS nodes in EPC.'
    fi 

    if [ $2 = 'spgw' ]; then
	echo 'Start SPGW nodes in EPC.'
    fi

    if [ $2 = 'mme' ]; then
	echo 'Start MME nodes in EPC.'
    fi

fi

#/usr/bin/xterm -fg lightgreen -bg Blue -cr red -fn 9*15 -e "pushd /home/ehhewng/openair-cn/SCRIPTS/; source ../oaienv; ./run_spgw" &

if [ $1 = "stop" ]; then
    echo 'Setup core network.'
    if [ $2 = 'all' ]; then
        echo '===> Stop all nodes in EPC, HSS/SPGW/MME.'
    fi
    
    if [ $2 = 'hss' ]; then
	echo 'Stop HSS nodes in EPC.'
    fi 

    if [ $2 = 'spgw' ]; then
	echo 'Stop SPGW nodes in EPC.'
    fi

    if [ $2 = 'mme' ]; then
	echo 'Stop MME nodes in EPC.'
    fi

fi
