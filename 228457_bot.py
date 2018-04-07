# Created by Davide Sordi in 07/04/2018 at 17.24
from telegram import ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def read_from_file(fileread):
    """
    Reading task list from a file
    :param fileread: file from where we read
    :return: a list of tasks
    """
    lista = list()
    txt = open(fileread, 'r')
    line = txt.readline().rstrip()  # rstrip elimina i \n o simili
    while line != "":  # la read ritorna una riga vuota in caso di EOF
        lista.append(line)
        line = txt.readline().rstrip()
    return lista


def save_on_file(file):
    """
    function for saving task list on a file
    :param file: file name to write
    """
    txt = open(file, 'w')
    for task in tasks:
        txt.write(task)
        txt.write("\n")  # stamp un a capo dopo ogni task
    txt.close()


def start(bot, received):
    """
    Start function for the telegram bot
    :param bot:
    :param received: received message (probably /start)
    """
    bot.sendChatAction(received.message.chat_id, ChatAction.TYPING)
    received.message.reply_text("Welcome to your Task List bot try /help")


def error_non_command_message(bot, received):
    """
    function for replying to non command messages
    :param bot:
    :param received: received message from user
    """
    bot.sendChatAction(received.message.chat_id, ChatAction.TYPING)
    answer = "Sorry, only command messages are eccepted. Try /help to know more..."
    received.message.reply_text(answer)


def unknown_command(bot, received):
    """
    Function for handling unknown commands
    :param bot:
    :param received:
    """
    bot.sendChatAction(received.message.chat_id, ChatAction.TYPING)
    answer = "Sorry this command is not accepted. Try /help to know more..."
    received.message.reply_text(answer)


def help_the_noob(bot, received):
    """
    Function to show possibles commands to the user
    :param bot:
    :param received:
    :return:
    """
    bot.sendChatAction(received.message.chat_id, ChatAction.TYPING)
    answer = "Here's a list of accepted commands:\n" \
             "/help I think you know what is\n" \
             "/showTasks will show you the tasks you have to do\n" \
             "newTask <task to add> insert a new task (remember /)\n" \
             "removeTask <task to remove> (you need the exact name of the task)\n" \
             "removeAllTasks <substring to search in a task to remove> "
    received.message.reply_text(answer)


def show_tasks(bot, received):
    """
    This function will reply to the user with the to-do list or another message if this list is empty
    :param bot:
    :param received:
    """
    bot.sendChatAction(received.message.chat_id, ChatAction.TYPING)
    if len(tasks) > 0:
        answer = tasks
    else:
        answer = "Nothing to do."
    received.message.reply_text(answer)


def insert_new_task(bot, received, args):
    """
    Function for insert a new task to the list and rewrite the list to a new file
    :param bot:
    :param received:
    :param args:
    :return:
    """
    bot.sendChatAction(received.message.chat_id, ChatAction.TYPING)
    if len(args) == 0:
        answer = "You need to specify a task!!!"
    else:
        tasks.append(" ".join(args))
        answer = "Task inserted successfully"
        save_on_file("new_task_list.txt")
    received.message.reply_text(answer)


def main():
    """
    Main function of the bot
    """
    # updater check if there are any updates in telegram chat
    updater = Updater(token='597817386:AAFsTFvxWdAV-824-CQfRBB0TiaLOcqAmqk')

    # read initial task list from a file

    # create a command handler for /start command
    disp = updater.dispatcher
    disp.add_handler(CommandHandler("start", start))

    # message handler for non command messages
    disp.add_handler(MessageHandler(Filters.text, error_non_command_message))

    # help handler for giving hint to noob user :)
    disp.add_handler(CommandHandler("help", help_the_noob))

    # show task command handler
    disp.add_handler(CommandHandler("showTasks", show_tasks))

    # insert new task command handler
    disp.add_handler(CommandHandler("newTask", insert_new_task, pass_args=True))

    #TODO remove all tasks function and handler

    # handler for unknown commands command is not iterable we use filterd messages
    disp.add_handler(MessageHandler(Filters.command, unknown_command))

    # start requesting information
    updater.start_polling()

    # will handle the stop of the bot
    updater.idle()


# trying for first declaring task list as global variable
tasks = read_from_file('task_list.txt')
# tasks = ""

if __name__ == '__main__':
    main()
