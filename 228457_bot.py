# Created by Davide Sordi in 07/04/2018 at 17.24

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def read_from_file(fileRead):
    """
    Reading task list from a file
    :param fileRead: file from where we read
    :return: a list of tasks
    """
    lista = list()
    txt = open(fileRead, 'r')
    line = txt.readline().rstrip()  # rstrip elimina i \n o simili
    while line != "":  # la read ritorna una riga vuota in caso di EOF
        lista.append(line)
        line = txt.readline().rstrip()
    return lista


def save_on_file(tasks, file):
    """
    function for saving task list on a file
    :param tasks: list of tasks to save
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
    received.message.reply_text("Welcome to your Task List bot try /help")


def error_non_command_message(bot, received):
    """
    function for replying to non command messages
    :param received: received message from user
    """
    answer = "Sorry, only command messages are eccepted. Try /help to know more..."
    received.message.reply_text(answer)


def unknown_command(bot, received):
    """
    Function for handling unknown commands
    :param bot:
    :param received:
    """
    answer = "Sorry this command is not accepted. Try /help to know more..."
    received.message.reply_text(answer)


def help_the_noob(bot, received):
    """
    Function to show possibles commands to the user
    :param bot:
    :param received:
    :return:
    """
    answer = "Here's a list of accepted commands:\n" \
             "/help I think you know what is\n" \
             "/showTasks will show you the tasks you have to do\n" \
             "newTask <task to add> insert a new task (remember /)\n" \
             "removeTask <task to remove> (you need the exact name of the task)\n" \
             "removeAllTasks <substring to search in a task to remove> "
    received.message.reply_text(answer)


def main():
    """
    Main function of the bot
    """
    # updater check if there are any updates in telegram chat
    updater = Updater(token='597817386:AAFsTFvxWdAV-824-CQfRBB0TiaLOcqAmqk')

    # read initial task list from a file
    tasks = read_from_file('task_list.txt')

    # create a command handler for /start command
    disp = updater.dispatcher
    disp.add_handler(CommandHandler("start", start))

    # message handler for non command messages
    disp.add_handler(MessageHandler(Filters.text, error_non_command_message))

    # help handler for giving hint to noob user :)
    disp.add_handler(CommandHandler("help", help_the_noob))

    # handler for unknown commands command is not iterable we use filterd messages
    disp.add_handler(MessageHandler(Filters.command, unknown_command))

    # start requesting information
    updater.start_polling()

    # will handle the stop of the bot
    updater.idle()


if __name__ == '__main__':
    main()
