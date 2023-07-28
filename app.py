import config
import server
from logger import logger


app = server.create_app()


if __name__ == "__main__":
    logger.info("App running on localhost:5001")
    app.run('localhost', 5001, True, use_reloader=False)