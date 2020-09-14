#!/bin/bash

echo -e "\e[33m setup_puppet_master: download_scratch-gui \e[0m"
wget --progress=dot:mega "https://github.com/LLK/scratch-gui/archive/develop.zip" -O gui.zip
unzip gui.zip
rm -f gui.zip
mv "scratch-gui-develop" scratch-gui

echo -e "\e[33m setup_puppet_master: download_scratch-vm \e[0m"
wget --progress=dot:mega "https://github.com/LLK/scratch-vm/archive/develop.zip" -O vm.zip
unzip vm.zip
rm -f vm.zip
mv "scratch-vm-develop" scratch-vm

curl -sL https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh -o install_nvm.sh
bash install_nvm.sh
source ~/.profile
rm install_nvm.sh
nvm install 10.21.0
nvm use 10.21.0
npm install -g yarn

cd scratch-vm
yarn install
yarn link
cd ../scratch-gui
yarn install
yarn link scratch-vm
cd ../..

echo -e "\e[33m setup_puppet_master: download_scratch-poppy \e[0m"
wget --progress=dot:mega "https://github.com/poppy-project/scratch-poppy/archive/master.zip" -O scratch-poppy.zip
unzip scratch-poppy.zip
rm -f scratch-poppy.zip
mv "scratch-poppy-master" scratch-poppy

cd scratch-poppy
bash install.sh