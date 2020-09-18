import subprocess
import os

def unix(directory):
    os.chdir(directory)
    subprocess.run(['echo', 'download_scratch-gui'])
    subprocess.run(['wget', '--progress=dot:mega', 'https://github.com/LLK/scratch-gui/archive/develop.zip', '-O', 'gui.zip'])
    subprocess.run(['unzip', 'gui.zip'])
    subprocess.run(['rm', '-f', 'gui.zip'])
    subprocess.run(['mv', 'scratch-gui-develop', 'scratch-gui'])
    subprocess.run(['rm', '-f', 'scratch-gui-develop'])

    subprocess.run(['echo', 'download_scratch-vm'])
    subprocess.run(['wget', '--progress=dot:mega', 'https://github.com/LLK/scratch-vm/archive/develop.zip', '-O', 'vm.zip'])
    subprocess.run(['unzip', 'vm.zip'])
    subprocess.run(['rm', '-f', 'vm.zip'])
    subprocess.run(['mv', 'scratch-vm-develop', 'scratch-vm'])
    subprocess.run(['rm', '-f', 'scratch-vm-develop'])

    subprocess.run(['curl', '-sL', 'https://deb.nodesource.com/setup_10.x', '-o', 'nodesource_setup.sh'])
    subprocess.run(['sudo', 'bash', 'nodesource_setup.sh'])
    subprocess.run(['rm', 'nodesource_setup.sh'])
    subprocess.run(['sudo', 'apt', 'install', 'nodejs'])
    subprocess.run(['/usr/bin/npm', 'install', '-g', 'yarn'])

    os.chdir('scratch-vm')
    subprocess.run(['/usr/local/bin/yarn', 'install'])
    subprocess.run(['/usr/local/bin/yarn', 'link'])
    os.chdir('../scratch-gui')
    subprocess.run(['/usr/local/bin/yarn', 'install'])
    subprocess.run(['/usr/local/bin/yarn', 'link', 'scratch-vm'])
    os.chdir('..')

    subprocess.run(['echo', 'download_scratch-poppy'])
    subprocess.run(['wget', '--progress=dot:mega', 'https://github.com/poppy-project/scratch-poppy/archive/master.zip', '-O', 'scratch-poppy.zip'])
    subprocess.run(['unzip', 'scratch-poppy.zip'])
    subprocess.run(['rm', '-f', 'scratch-poppy.zip'])
    subprocess.run(['mv', 'scratch-poppy-master', 'scratch-poppy'])
    subprocess.run(['rm', '-f', 'scratch-poppy-master'])

    os.chdir('scratch-poppy')
    subprocess.run(['bash', 'install.sh'])

    subprocess.run(['/usr/bin/npm', 'install', '-g', 'wait-on'])