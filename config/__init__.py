import toml
import os

server_config = os.environ.get("SERVER_CONFIG")

if server_config is None:
    raise Exception("SERVER_CONFIG not specified")

config = toml.load("{}/{}/config.toml".format(os.path.dirname(__file__), server_config))
# print(config)
