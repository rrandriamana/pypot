import subprocess

def unix():
    subprocess.Popen(['echo -e "\e[33m setup_puppet_master: download_scratch-gui \e[0m"'])
    subprocess.Popen(['wget --progress=dot:mega "https://github.com/LLK/scratch-gui/archive/develop.zip" -O gui.zip'])
    subprocess.Popen(['unzip gui.zip'])
    subprocess.Popen(['rm -f gui.zip'])
    subprocess.Popen(['mv "scratch-gui-develop" scratch-gui'])

    subprocess.Popen(['echo -e "\e[33m setup_puppet_master: download_scratch-vm \e[0m"'])
    subprocess.Popen(['wget --progress=dot:mega "https://github.com/LLK/scratch-vm/archive/develop.zip" -O vm.zip'])
    subprocess.Popen(['unzip vm.zip'])
    subprocess.Popen(['rm -f vm.zip'])
    subprocess.Popen(['mv "scratch-vm-develop" scratch-vm'])

    subprocess.Popen(['curl -sL https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh -o install_nvm.sh'])
    subprocess.Popen(['bash install_nvm.sh'])
    subprocess.Popen(['source ~/.profile'])
    subprocess.Popen(['rm install_nvm.sh'])
    subprocess.Popen(['nvm install 10.21.0'])
    subprocess.Popen(['nvm use 10.21.0'])
    subprocess.Popen(['npm install -g yarn'])

    subprocess.Popen(['cd scratch-vm'])
    subprocess.Popen(['yarn install'])
    subprocess.Popen(['yarn link'])
    subprocess.Popen(['cd ../scratch-gui'])
    subprocess.Popen(['yarn install'])
    subprocess.Popen(['yarn link scratch-vm'])
    subprocess.Popen(['cd ../..'])

    subprocess.Popen(['echo -e "\e[33m setup_puppet_master: download_scratch-poppy \e[0m"'])
    subprocess.Popen(['wget --progress=dot:mega "https://github.com/poppy-project/scratch-poppy/archive/master.zip" -O scratch-poppy.zip'])
    subprocess.Popen(['unzip scratch-poppy.zip'])
    subprocess.Popen(['rm -f scratch-poppy.zip'])
    subprocess.Popen(['mv "scratch-poppy-master" scratch-poppy'])

    subprocess.Popen(['cd scratch-poppy'])
    subprocess.Popen(['bash install.sh'])