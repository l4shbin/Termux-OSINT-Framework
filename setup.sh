#!/bin/bash
pkg update && pkg upgrade -y
pkg install python -y
pip install requests
echo "alias l4sh-osint='python $(pwd)/src/main.py'" >> ~/.bashrc
echo -e "\033[1;32mSetup Done! Please restart Termux or type 'source ~/.bashrc'\033[0m"
echo -e "\033[1;32mThen type 'l4sh-osint' to start.\033[0m"
