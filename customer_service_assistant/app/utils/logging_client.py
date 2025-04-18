# app/utils/logging_server.py

import zmq
from loguru import logger

from .config_loader import load_toml_config

config = load_toml_config("log_config.toml")["logging"]
port = config["logging_server_port_no"]

def run_logging_server():
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind(f"tcp://*:{port}")
    logger.info(f"Logging server running on port {port}")

    while True:
        msg = socket.recv_json()
        logger.log(msg["level"], f"{msg['source']}: {msg['message']}")
