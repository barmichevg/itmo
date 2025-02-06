#!/bin/bash

# 1

mkdir ~/lab0
cd ~/lab0

touch carvanha4
mkdir -p hydreigon6/lotad
mkdir hydreigon6/crustle
mkdir hydreigon6/combusken
mkdir hydreigon6/kadabra

touch lampent5
mkdir -p phanpy1/machamp
touch phanpy1/remoraid
touch phanpy1/magby
touch phanpy1/walrein

touch turtwig4
mkdir -p ursaring2/budew
mkdir ursaring2/slowbro
touch ursaring2/hoppip
touch ursaring2/volcarona

echo -e 'Возможности Overland=1 Surface=10 Underwater=8 Jump3=0\nPower=1 Intelligence=4 Gilled=0' > carvanha4
echo -e 'satk=10 sdef=6\nspd=6' > lampent5
echo -e 'Тип покемона WATER NONE' > phanpy1/remoraid
echo -e 'Развитые способности\nVital Spirit' > phanpy1/magby
echo -e 'satk=10 sdef=9 spd=7' > phanpy1/walrein
echo -e 'Возможности\nOverland=4 Surface=2 Burrow=4 Jump=3 Power=1 Intelligence=3\nSprouter=0' > turtwig4
echo -e 'Способности Splash Synthesis Tail Whip Tackle\nPoisonpowder Stun Spore Sleep Powder Bullet Seed Leech Seed Mega Drain\nAcrobatics Rage Powder Cotton Spore U-Turn Worry Seed Giga Drain\nBounce Memento' > ursaring2/hoppip
echo -e 'Живет Cave Mountain' > ursaring2/volcarona

echo "====Step 1 done===="