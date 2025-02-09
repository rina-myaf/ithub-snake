import logging
import bootstrap
from config import get_config


def serve():
    config = get_config()
    app = bootstrap.configure_app()

    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    print(f"\Running on http://{config['host']}:{config['port']}")
    app.run(host=config["host"], port=config["port"], debug=True)


if __name__ == "__main__":
    serve()
