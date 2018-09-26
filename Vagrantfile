# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "tests/test.yml"
    ansible.extra_vars  = "tests/vagrant.inventory.yml"
    ansible.galaxy_role_file = "requirements.yml"
  end

  config.vm.provider "virtualbox" do |v|
    v.memory = 8192
    v.cpus = 2
  end

  config.vm.network "forwarded_port", guest: 8080, host: 8888
  config.vm.box = "ubuntu/xenial64"
end
