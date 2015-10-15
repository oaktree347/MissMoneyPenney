#Legobot
=======
##Authors
Bren Briggs and Kevin McCabe developed Legobot in late 2013. This is an application built on that work. 

##Introduction
Legobot (and the Tipbot built with it) is just a simple python IRC bot made to allow people to easily write their own functions. 
Functions takea  .msg object as input and if they want to respond to the channel, pass a string as output. Legobot handles the rest. 

An example .py file exists for how to create a simple IRC Bot.

See the [Legobot repo](https://github.com/bbriggs/Legobot) for more detailed, but still very awful, documentation on the API. 

##Usage
This bot was made to be run either independently or with [Docker](https://www.docker.com/). If you're reading this repo, it means you found the dockerized version. Congratulations!
To run this bot, supply a config file (example below and provided in repo) by mounting a config file into `/tipbot/config.fecn`

Note about one function: In the current form, tips are not persistent across bot restarts. They're internet points anyway. What did you plan to spend them on?

###Running the bot and adding your own config
`docker run -d -it -v /your/config/file:/tipbot/config.fecn bbriggs/sithmail-tipbot` should take care of most needs. 

The config file is pretty self explanatory and built to allow new parameters to be added, if you understand Legobot well enough. 
Just build a config file pointing to the IRC server and channel of your preferenceThe minimum config file looks like this:
```
<str>HOST=irc.sithmail.com
<str>HOSTPW= 
<int>PORT=6697
<str>NICK = TheDoctor
<str>ROOM = #social
<str>ROOMPW = 
<int>SNARKHOLDDOWN = 15
<bool>ISSSL = True
```
Inline comments in the config file are not supported at this time. Currently only permits one channel at a time. 