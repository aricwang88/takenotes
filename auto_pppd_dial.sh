#!/usr/bin/env sh


echo Prepare to connect to EPS.

while true
do
sleep 2
ret=`ip a | grep 10.64.64.64`
if [ -z $ret ]; then
	echo Not attach to EPS, try again!
	sleep 2
	pkill -9 pppd
	echo Try to dial again!
else
	echo Already connected to EPS.
	echo Add a route in table for LTE dongle.
	route add -net 10.0.0.0/8 ppp0

fi
sleep 10
done

