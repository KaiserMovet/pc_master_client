from server_connector import ServerConnector
from controller import get_controller
import logs
import threading
import time
import yaml
import logging


def get_vars():
    vars = None
    with open("data.yml", "r") as f:
        vars = yaml.load(f.read(), Loader=yaml.SafeLoader)
    return vars


def register(server):
    registered = False
    while not registered:
        try:
            server.send_data()
        except Exception as e:
            logging.warning("Cannot register client")
            logging.warning(e)
            time.sleep(1 * 60)
        else:
            logging.info("Client registered successfully")
            registered = True


def main():
    logs.init()
    logging.info("Starting program")

    vars = get_vars()
    server_ip = vars["server_url"]
    local_port = vars["local_port"]
    controller = get_controller()
    server = ServerConnector(server_ip, local_port, controller)
    th = threading.Thread(target=register, args=(server,))
    th.daemon = True
    th.start()
    server.wait_for_command()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.critical(e)
