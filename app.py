import signal
import sys
import logging
from enum import Enum

from src.server import create_app
import src.logger

app = create_app('src.config.DevelopmentConfig')

class ExitStatus(Enum):
    Failure = 1
    Success = 0

def handler(signum, frame):
    logging.info('App exited with success')
    sys.exit(ExitStatus.Success)

if __name__ == "__main__":
    try:
        EXIT_SIGNALS: "list[signal.Signals]" = [signal.SIGINT,signal.SIGTERM]
        for sig in EXIT_SIGNALS:
            try:
                signal.signal(sig,handler)
            except Exception as error:
                logging.error(f"App exited with error: {repr(error)}")  
                sys.exit(ExitStatus.Failure)
        app.run(host = "0.0.0.0",load_dotenv=True)

    except Exception as error:
        logging.error(f"App exited with error: {repr(error)}")
        sys.exit(ExitStatus.Failure)
