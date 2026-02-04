#  Imports desnecessários, 'traceback' não é usado no código e Evitar múltiplos imports em uma linha (PEP 8)
import os, sys, traceback, logging, configparser

import xlsxwriter

#  'timedelta' e 'timezone' não são usados no código - remover
from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.blocking import BlockingScheduler

#  Flask é importado e inicializado o app mas ele não é de fato usado, pois é um robo e não um aplicativo web
from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from logging.handlers import RotatingFileHandler


def main(argv):

    greetings()

    print("Press Crtl+{0} to exit".format("Break" if os.name == "nt" else "C"))

    #  Flask não deveria ser usado aqui
    app = Flask(__name__)

    #  maxBytes=10000 (10KB) é muito pequeno para logs
    handler = RotatingFileHandler("bot.log", maxBytes=10000, backupCount=1)

    handler.setLevel(logging.INFO)

    app.logger.addHandler(handler)

    """
    Aqui estamos configurando a URI de conexão com o banco de dados estamos deixando a senha exposta no código fonte.
    O GitGauardian pode alertar sobre isso mas uma boa pratica é usar variaveis de ambiente, no .env, para armazenar informações sensíveis como senhas.
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql+psycopg2://postgres:123mudar@127.0.0.1:5432/bot_db"
    )

    db = SQLAlchemy(app)

    config = configparser.ConfigParser()

    # Falta validação se o arquivo existe
    config.read("/tmp/bot/settings/config.ini")

    #  Falta validação se o valor é válido (> 0)
    var1 = int(config.get("scheduler", "IntervalInMinutes"))

    app.logger.warning("Intervalo entre as execucoes do processo: {}".format(var1))

    scheduler = BlockingScheduler()

    #  task1(db) está sendo EXECUTADA agora, não agendada
    task1_instance = scheduler.add_job(
        task1(db), "interval", id="task1_job", minutes=var1
    )

    try:

        scheduler.start()

    except (KeyboardInterrupt, SystemExit):

        pass


def greetings():
    #  Falta docstring explicando o propósito da função

    print(" ##########################")

    print(" # - ACME - Tasks Robot - #")

    print(" # - v 1.0 - 2020-07-28 - #")

    print(" ##########################")


#  Falta tratamento de erros
def task1(db):

    #  Usar f-strings em vez de .format() (Python 3.6+)
    file_name = "data_export_{0}.xlsx".format(datetime.now().strftime("%Y%m%d%H%M%S"))

    file_path = os.path.join(os.path.curdir, file_name)

    workbook = xlsxwriter.Workbook(file_path)

    worksheet = workbook.add_worksheet()

    # Usar SQL puro ao invez de ORM pode gerar SQL Injection, ou seja, vulnerabilidade de segurança.
    orders = db.session.execute("SELECT * FROM users;")

    index = 1

    worksheet.write("A{0}".format(index), "Id")

    worksheet.write("B{0}".format(index), "Name")

    worksheet.write("C{0}".format(index), "Email")

    # Vunerabilidade de segurança exportando senha em texto
    worksheet.write("D{0}".format(index), "Password")

    worksheet.write("E{0}".format(index), "Role Id")

    worksheet.write("F{0}".format(index), "Created At")

    worksheet.write("G{0}".format(index), "Updated At")

    #  Itero sobre orders quando na verdade são usuários
    for order in orders:

        index = index + 1

        print("Id: {0}".format(order[0]))

        worksheet.write("A{0}".format(index), order[0])

        print("Name: {0}".format(order[1]))

        worksheet.write("B{0}".format(index), order[1])

        print("Email: {0}".format(order[2]))

        worksheet.write("C{0}".format(index), order[2])

        #     # Vunerabilidade de segurança exportando senha em texto
        print("Password: {0}".format(order[3]))

        worksheet.write("D{0}".format(index), order[3])

        print("Role Id: {0}".format(order[4]))

        worksheet.write("E{0}".format(index), order[4])

        print("Created At: {0}".format(order[5]))

        worksheet.write("F{0}".format(index), order[5])

        print("Updated At: {0}".format(order[6]))

        worksheet.write("G{0}".format(index), order[6])

    #  Falta fechar db.session
    workbook.close()

    #  Usar logger em vez de print
    print("job executed!")

    #  Falta retornar algo ou logar informações sobre o sucesso da operação
    #  Falta tratamento de erros - wrap tudo em try/except com logging


if __name__ == "__main__":

    main(sys.argv)
