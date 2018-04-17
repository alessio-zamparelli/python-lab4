from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ChatAction
import time
from sys import exit
from os import _exit
import configparser
tasks_list = list()
pathToFile = "/home/ale-dell/Python project/python-lab2/task_list.txt"

"""

/showTasks
/newTask	<task	to	add>
/removeTask	<task	to	remove>
/removeAllTasks	<substring	to	use	to	remove	all	the	tasks	that	contain	it>


"""


def load_list(path):
    with open(path) as f:
        lines = f.readlines()
        for line in lines:
            tasks_list.append(line.strip())


def save_list(bot, update):
    f = open(pathToFile, 'w')
    for item in tasks_list:
        f.write("%s\n" % item)
    update.message.reply_text("list saved")


"""
def readInput(bot, update):
    readed = update.message.text
    print("f readInput" + readed)
    return update.message.text
"""


def showTasks(bot, update):
    if len(tasks_list) == 0:
        update.message.reply_text("no tasks memorized yet")
        return
    tasks_list.sort()
    for element in tasks_list:
        update.message.reply_text(element)




def newTask(bot, update, args):
    msg = ' '.join(args)
    #print(msg + " replied text!!")
    if(msg != ""):
        tasks_list.append(msg)
        #showTasks(bot, update)
        update.message.reply_text("added " + msg + " to the tasks list")
    else:
        update.message.reply_text("error")




def removeTask(bot, update, args):
    msg = ' '.join(args)
    try:
        tasks_list.remove(msg)
        update.message.reply_text(msg + " removed")
    except ValueError:
        update.message.reply_text("element not found!")


def removeAllTasks(bot, update):
    tasks_list.clear()
    update.message.reply_text("Deleted ALL tasks")


def start(bot, update):
    # handle start on bot
    update.message.reply_text("connected")
    update.message.reply_text(
        "list of commands:\n/show_tasks\tshow all saved tasks\n/new_tasks\tadd a new task\n/remove_task\n/remove_all_tasks\tremove all tasks\nsave_tasks\tsave current list")


def testPrint():
    if len(tasks_list) == 0:
        print("no tasks memorized yet")
        return
    tasks_list.sort()
    print(*tasks_list, sep='\n')

def cancel(bot, update):
    update.message.reply_text("adieu!")
    save_list(bot, update)
    _exit(0)


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['telegram']['token']
    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("show_tasks", showTasks))
    dispatcher.add_handler(CommandHandler("new_task", newTask, pass_args="true"))
    dispatcher.add_handler(CommandHandler("remove_task", removeTask, pass_args="true"))
    dispatcher.add_handler(CommandHandler("remove_all_tasks", removeAllTasks))
    dispatcher.add_handler(CommandHandler("save_tasks", save_list))
    dispatcher.add_handler(CommandHandler("cancel", cancel))


    #dispatcher.add_handler(MessageHandler(Filters.text, readInput))

    load_list(pathToFile)

    # testPrint()

    updater.start_polling()
    updater.idle()

    # save_list(pathToFile)


if __name__ == "__main__":
    main()
