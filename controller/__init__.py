from .win_controller import WinController


import os
import logging


class WrongOS(Exception):
    pass


def get_controller():
    if os.name == "nt":
        logging.info("Create WinController")
        return WinController()
    raise WrongOS
