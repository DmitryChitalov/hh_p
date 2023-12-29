import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))

import multiprocessing as ml
from parser_app import main as pr
from hh_parser.web_app import create_app

if __name__ == "__main__":
    # Создать приложение Flask
    app = create_app()

    # Запустить парсер
    par_service = ml.Process(name="HH Parser", target=pr.main)
    par_service.start()


    # Запустить Flask приложение
    app.run()
