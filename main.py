import logging

from app.controllers.rethome import server
import settings


logging.basicConfig(filename=settings.LOG_FILE, level=logging.INFO)
logger = logging.getLogger(__name__)


#コントローラのサーバーをメインパイで起動
if __name__ == '__main__':
    logger.info("running server")
    server.start(debug=settings.DEBUG)

