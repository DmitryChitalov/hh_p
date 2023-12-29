import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))

import multiprocessing as ml
from parser_app import main as pr
#from web_app import create_app

def create_app():
    from web_app.flask_parser.flask_parser import parser_blueprint
    from web_app.authorization.auth import auth_blueprint
    app.register_blueprint(parser_blueprint)
    app.register_blueprint(auth_blueprint)

    return app

if __name__ == "__main__":
    # Создать приложение Flask
    app = create_app()

    # Запустить парсер
    par_service = ml.Process(name="HH Parser", target=pr.main)
    par_service.start()


    # Запустить Flask приложение
    app.run(debug=True
            )
