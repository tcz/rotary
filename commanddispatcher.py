from commands.romanticlights import RomanticLights
from commands.romanticmusic import RomanticMusic

class CommandDispatcher:
    def __init__(self, logger):
        self.commands = list()
        self.commands.append(RomanticLights(logger))
        self.commands.append(RomanticMusic(logger))

    def dispatch(self, command_text):
        for command in self.commands:
            command.respond_to(command_text)

