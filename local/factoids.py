import logging
import json
import requests
import random
from Legobot.Lego import Lego

logger = logging.getLogger(__name__)

class Factoids(Lego):
    """Class to hold all factoids
    Args: Lego
    """
    def listening_for(self, message):
        """Checks if the message contains a command that we need to execute
        Args:
            self:
            message: The complete line/message that comes from an IRC channel

        Returns:
            Bool: Returns true if the first word in the message is a command for this class
        """
        cmds = ['!ugt', '!info', '!users', '!gray']
        return message['text'].split()[0] in cmds

    def handle(self, message):
        """Execute the needed command
        Args:
            self:
            message: The complete line/message that comes from an IRC channel

        Returns:
            string: Returns the suitable factoid
        """
        opts = None
        logger.info(message)
        try:
            target = message['metadata']['source_channel']
            opts = {'target':target}
        except IndexError:
            logger.error('Could not identify message source in message: %s' % str(message))
        command = message['text'].split()[0]
        if command == '!ugt':
            txt = 'Universal Greeting Time. http://www.total-knowledge.com/~ilya/mips/ugt.html'
        elif command == '!info':
            txt = "You are on the 0x00sec IRC network in channel {} |  Forums: https://0x00sec.org/ " \
                  "| IRC: irc.0x00sec.org 6697+ | Git server: https://git.0x00sec.org " \
                  "| Source for this bot: https://github.com/bbriggs/MissMoneyPenney".format(message['metadata']['source_channel'])
        elif command == "!users":
            users = json.loads(requests.get("https://0x00sec.org/about.json").text)
            count = users['about']['stats']['user_count']
            txt = "There are currently {} registered users on 0x00sec.".format(count)
        elif command == "!gray":
            responses = ["Well I'm a paint my picture, Paint myself in blue, red, black and gray",
                         "All of the beautiful colors are very, very meaningful",
                         "Yeah, well you know, gray is my favorite color",
                         "I felt so symbolic yesterday",
                         "If I knew Picasso, I would buy myself a gray guitar and play",
                         "Sha la, la, la, la, la, la, la",
                         "Cut up, Maria. Show me some of them Spanish dances", 
                         "Pass me a bottle, Mr. Jones",
                         "Mr. Jones and me tell each other fairy tales",
                         "https://www.youtube.com/watch?v=-oqAU5VxFWs"]
            txt = random.choice(responses)
        self.reply(message, txt, opts)

    def get_name(self):
        """Returns the name of this class
        Args:
            self:

        Returns:
            string: The name of this class
        """
        return 'factoids'

    def get_help(self):
        """Prints a useful help message into the channel

        Args:
            self:

        Returns:
            String: A help message that explains this class
        """
        help_text = "collection of nice factoids (static reponses). " \
                "!ugt, !info, !users"
        return help_text
