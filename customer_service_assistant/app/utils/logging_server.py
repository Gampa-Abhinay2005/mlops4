# app/utils/logging_client.py

import zmq
from loguru import logger
from .config_loader import load_toml_config

config = load_toml_config("log_config.toml")["logging"]

LOG_SERVER_PORT = config["logging_server_port_no"]
LOG_LEVEL = config["min_log_level"]
LOG_ROTATION = config["log_rotation"]
LOG_COMPRESSION = config["log_compression"]
LOG_FILE_NAME = config["log_file_name"]

context = zmq.Context()
log_socket = context.socket(zmq.PUSH)
log_socket.connect(f"tcp://localhost:{LOG_SERVER_PORT}")

def setup_logger(service_name: str):
    logger.remove()
    logger.add(LOG_FILE_NAME, rotation=LOG_ROTATION, compression=LOG_COMPRESSION, level=LOG_LEVEL)

    def send_to_server(msg):
        log_record = {
            "source": service_name,
            "level": msg.record["level"].name,
            "message": msg.record["message"],
        }
        log_socket.send_json(log_record)

    logger.add(send_to_server, level=LOG_LEVEL)
    return logger
