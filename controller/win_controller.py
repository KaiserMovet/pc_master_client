from .controller import Controller

import logging


class WinController(Controller):
    def __init__(self):
        pass

    def command_off(self):
        logging.info("Shutting down client")

    def command_volume(self, volume_level):
        volume_level = int(volume_level)
        logging.info(F"Setting Volume to {volume_level}")

    def execute_command(self, command_list):
        if command_list[0] == 'off':
            self.command_off()
        elif command_list[0] == 'volume':
            self.command_volume(command_list[1])
        else:
            logging.warning(F"Unknown command: {command_list}")

    pass
