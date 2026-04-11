#!/bin/bash
echo -e "\e[1;32m[🔥] Installing L4SH-OSINT Pro v2.0...\e[0m"
pkg update -y
pkg install python git -y
pip install -r requirements.txt
chmod +x main.py
echo -e "\e[1;32m[✅] Installation complete!\e[0m"
echo -e "\e[1;34mUsage:\e[0m python main.py l4shbin"
