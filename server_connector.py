import requests
from wsgiref.simple_server import make_server
import falcon
import uuid
import json
import logging


class ServerConnector:

    def __init__(self, server_ip, local_port, controller):
        self.controller = controller
        self.server_ip = server_ip
        self.port = local_port

        self._set_mac()

    def prepare_data(self):
        data = {}
        data["mac"] = self.mac
        data["port"] = self.port
        return data

    def send_data(self, data=None):
        data = self.prepare_data()

        r = requests.post("http://" + self.server_ip +
                          "/pc_master/api/register/" + self.mac + "/", data)
        print(r)

    def _set_mac(self):
        # TODO fix this function
        self.mac = (':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                              for ele in range(0, 8 * 6, 8)][::-1]))
        logging.info(F"Set mac to {self.mac}")

    def wait_for_command(self):
        app = falcon.App()
        app.add_route('/', self)
        logging.info("Starting server")
        with make_server('', 21370, app) as httpd:
            httpd.serve_forever()

    def on_post(self, req, resp, **kwargs):
        '''
        Function used by Falcon
        '''
        result = req.media
        logging.info(F"POST DATA was received: {result}")
        command_list = result.get("command", [])
        if not isinstance(command_list, list):
            logging.error(
                F"Wrong command format. Should be list, "
                F"not {type(command_list)}")
            return
        logging.info(F"Command was received: {command_list}")
        if not command_list:
            logging.info("EXECUTED: nothing")
            return
        if command_list[0] == "refresh":
            logging.info("EXECUTED: refresh")
            resp.text = json.dumps(self.prepare_data())
        else:
            self.controller.execute_command(command_list)
