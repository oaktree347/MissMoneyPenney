$script = <<SCRIPT
apt-get install -y python-pip
pip install -U Legobot
SCRIPT

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.synced_folder ".", "/project"
  config.vm.provision "shell", inline: $script
end

