# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "geerlingguy/centos7"
    config.vm.network "private_network", ip: "192.168.10.10"
    config.vm.synced_folder ".", "/vagrant"
    config.vm.provider "virtualbox" do |vb|
        vb.name = "airflow"
        vb.memory = 2048
        vb.cpus = 2
    end
end
