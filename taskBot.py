from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
from telegram import (ChatAction, ReplyKeyboardMarkup, ReplyKeyboardRemove)
from os import _exit
import sqlite3
import os
import configparser

import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR)

pathToFile = "/home/ale-dell/Python project/python-lab2/task_list.txt"
pathToDb = 'task_list.db'

con = None


def start(bot, update):
    global con
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    try:
        con = sqlite3.connect(pathToDb)
        # print("db correttamente aperto")
        # update.message.reply_text("your user id is: " + str(update.message.from_user.id))
        cur = con.cursor()
        cur.execute(
            "create table if not exists '%d' (id_task integer primary key, todo varchar[255] not null)" % update.message.from_user.id)
        con.commit()
        cur.close()
    except sqlite3.DataError as DataErr:
        print("errore di creazione table " + DataErr.args[0])
    except sqlite3.DatabaseError as DBerror:
        print("errore nell'apertura del db " + DBerror.args[0])
        sys.exit(1)

    update.message.reply_text("""
    List of commands:
    /start - Start the bot
    /showTasks - Show stored tasks
    /newTask - Add new task
    /removeTask - Remove a single task
    /removeAllTasks - Remove all the existing tasks from the DB that contain a provided
    /quit - Exit the bot and save
    """)


def showTasks(bot, update):
    global con
    cur = con.cursor()
    cur.execute("select todo from '%s' order by todo" % update.message.from_user.id)
    rows = cur.fetchall()
    cur.close()
    if len(rows) == 0:
        update.message.reply_text("no tasks memorized yet")
        return
    for line in rows:
        print(line[0])
        update.message.reply_text(line[0])


def newTask(bot, update, args):
    msg = ' '.join(args)
    if (msg != ""):

        global con
        cur = con.cursor()
        cur.execute(
            "insert into '%d' (todo) values ('%s')" % (update.message.from_user.id, msg))
        con.commit()
        cur.close()

        # showTasks(bot, update)
        update.message.reply_text("added " + msg + " to the tasks list")
    else:
        update.message.reply_text("empty task...")


def removeTask(bot, update, args):
    msg = ' '.join(args)
    try:
        global con
        cur = con.cursor()
        cur.execute("delete from '%s' where todo = '%s'" % (update.message.from_user.id, args[0]))
        con.commit()
        cur.close()
        update.message.reply_text(msg + " removed")
    except ValueError:
        update.message.reply_text("element not found!")


def substringStatement(string, userID):
    statement = "delete * from " + userID + "where"
    words = string.split(" ")
    for word in words:
        statement += " todo like " + word
        if word != words[-1]:
            statement += "and"
    print("da eliminare\n" + statement)


def removeAllTasks(bot, update):
    global con
    cur = con.cursor()
    # use the substingStatement function
    # cur.execute("delete from '%s' " % update.message.from_user.id)
    update.message.reply_text("Deleted ALL tasks")


def closeBot(bot, update):
    global con
    con.close()
    update.message.reply_text("adieu!")
    _exit(0)


def clean_db(bot, update):
    global pathToDb
    os.remove(pathToDb)
    with open(pathToDb, 'w'):
        os.utime(pathToDb, None)


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['telegram']['token']
    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("showTasks", showTasks))
    dispatcher.add_handler(CommandHandler("newTask", newTask, pass_args="true"))
    dispatcher.add_handler(CommandHandler("removeTask", removeTask, pass_args="true"))
    dispatcher.add_handler(CommandHandler("removeAllTasks", removeAllTasks))
    dispatcher.add_handler(CommandHandler("quit", closeBot))
    dispatcher.add_handler(CommandHandler("clean_db", clean_db))

    # piu brevi

    dispatcher.add_handler(CommandHandler("add", newTask, pass_args="true"))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
