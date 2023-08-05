#!/usr/bin/python
import setuptools
import pkg_resources
import os
from subprocess import call
import shutil
from setuptools.command.install import install

def setup_system_service():
    autostart_dir = "/home/melopero-autostart/"
    scripts_dir = os.path.join(autostart_dir, "scripts/")
    uninstall_dir = os.path.join(autostart_dir, "uninstall/")
    
    bash_script_name = "StartScripts.sh"
    uninstall_script_name = "uninstall.sh"
    instructions_name = "instructions.txt"
    
    systemd_dir = "/etc/systemd/system/"
    service_unit_name = "melopero-autostart.service"
    
    package_name = "melopero-autostart"
    
    #create autostart dirs
    if not os.path.exists(autostart_dir):
        os.mkdir(autostart_dir)
    
    if not os.path.exists(scripts_dir):
        os.mkdir(scripts_dir)
        
    if not os.path.exists(uninstall_dir):
        os.mkdir(uninstall_dir)
        
    #copy bash script in autostart dir
    bash_script_path = os.path.abspath(pkg_resources.resource_filename(package_name, bash_script_name))
    final_bash_script_path = os.path.join(autostart_dir, os.path.basename(bash_script_path))
    shutil.copyfile(bash_script_path, final_bash_script_path) 
    os.chmod(final_bash_script_path, 0o554)
    
    #copy uninstall script in uninstall dir and instructions
    uninstall_script_path = os.path.abspath(pkg_resources.resource_filename(package_name, uninstall_script_name))
    final_uninstall_script_path = os.path.join(uninstall_dir, os.path.basename(uninstall_script_path))
    shutil.copyfile(uninstall_script_path, final_uninstall_script_path)
    os.chmod(final_uninstall_script_path, 0o554)
    
    instructions_path = os.path.abspath(pkg_resources.resource_filename(package_name, instructions_name))
    final_instructions_path = os.path.join(uninstall_dir, os.path.basename(instructions_path))
    shutil.copyfile(instructions_path, final_instructions_path)
    os.chmod(final_instructions_path, 0o444)

    #copy system service unit
    service_unit_path = os.path.abspath(pkg_resources.resource_filename(package_name, service_unit_name))
    shutil.copyfile(service_unit_path, os.path.join(systemd_dir, service_unit_name))
    os.chmod(os.path.join(systemd_dir, service_unit_name), 0o664)
    shutil.chown(os.path.join(systemd_dir, service_unit_name), "root", "root")
    
    #enable service
    # =============================================================================
    # sudo systemctl daemon-reload
    # sudo systemctl enable sample.service
    # =============================================================================
    status = call(["systemctl", "daemon-reload"])
    if status == 0: 
        status = call(["systemctl", "enable", service_unit_name])
    
    if status != 0:
        print("""WARNING! Service could not be activated. Please enable the service
              by typing the following commands:\n sudo systemctl enable {} \n 
              sudo systemctl daemon-reload""".format(service_unit_name))

class InstallCommand(install):
    def initialize_options(self):
        install.initialize_options(self)

    def finalize_options(self):
        #print('The custom option for install is ', self.custom_option)
        install.finalize_options(self)

    def run(self):
        setup_system_service()
        install.run(self)  # OR: install.do_egg_install(self)
    

setuptools.setup(
    name="melopero_autostart",
    version="0.0.3",
    description="Melopero Autostart, easily run python scripts at startup",
    #url="https://github.com/melopero/Melopero_AMG8833/tree/master/module",
    author="Melopero",
    author_email="info@melopero.com",
    license="MIT",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    cmdclass={
        'install': InstallCommand,
    },
)