# Nullbot

## Installation

We provide a basic config file, it is located at config.example.ini. Please rename it to config.ini

### Local

*Note that python packages for this are 'pinned' in requirements.txt*

`pip3 install -r ./requirements.txt`

### venv

```bash
virtualenv --python=/usr/bin/python3 venv
source venv/bin/activate
pip3 install -r ./requirements.txt
```

## Running

If you decide to do this in Docker, local installation is not necessary.

### With Docker

`./run.sh SomeLocalContainerName` will start a local python:3 container, mount the repo into /usr/src/legobot, install deps, and then run the chatbot.py script.

### Without Docker

If you don't use virtualenv you can directly start the bot:

```bash
python3 chatbot.py
```

In case of virtualenv you first have to activate it:

```bash
source venv/bin/activate
python3 chatbot.py
```

### virtualenv and systemd

We can create a systemd service file in the namespace of our linux user, which doesn't require any root priviledges. This allows us to easily utilize systemd features.
Create the directory:

```bash
mkdir -p ~/.config/systemd/user
```

After that, create a nullbot.service file in it with the following content (it assumes that you cloned this repository into your home directory, please replace $USER with your actual username):

```ini
[Unit]
Description=0x00sec IRC Bot
After=network.target

[Service]
WorkingDirectory=/home/$USER/nullbot
ExecStart=/home/$USER/nullbot/venv/bin/python3 /home/$USER/nullbot/chatbot.py
PrivateTmp=true

[Install]
WantedBy=default.target
```

You can now start/stop/restart/status the bot with:

```
systemctl --user start nullbot
systemctl --user status nullbot
systemctl --user restart nullbot
systemctl --user restart nullbot
```

If you want the service to start at boot and run when logged out:

```
sudo loginctl enable-linger $USER
```

You can run it persistently with:

```bash
systemctl --user enable nullbot
```

### Setting configuration

Use the config.ini to provide settings to the chatbot.py script

### Developing Plugins

See [this link](https://github.com/bbriggs/Legobot/blob/develop/docs/writing-a-lego.md)
