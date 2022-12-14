# TODO this file could be made more general, or even moved to individual task code


import os
import codecs

from psychopy import event, logging, visual, core


def read_text_from_file(file_name, insert=""):
    """
    Method that read message from text file, and optionally add some
    dynamically generated info.
    :param file_name: Name of file to read
    :param insert: dynamically generated info
    :return: message
    """
    if not isinstance(file_name, str):
        raise TypeError("file_name must be a string")
    msg = list()
    with codecs.open(file_name, encoding="utf-8", mode="r") as data_file:
        for line in data_file:
            if not line.startswith("#"):  # if not commented line
                msg.append(line)
    whole_message = "".join(msg)
    final_message = whole_message.replace("<--insert-->", insert)
    return final_message


def show_info(
    file_name,
    exp,
    insert="",
    alignText="center",
    pos=(0, 0),
    duration=None,
):
    """
    Clear way to show info message into screen.
    :param win:
    :param file_name:
    :param screen_width:
    :param text_size:
    :param text_color:
    :param insert: extra text for read_text_from_file
    :return:
    """

    screen_width = exp.screen_res["width"]

    hello_msg = read_text_from_file(os.path.join("messages", file_name), insert=insert)
    hello_msg = visual.TextStim(
        win=exp.win,
        antialias=True,
        font=exp.config["Text_font"],
        text=hello_msg,
        height=exp.config["Text_size"],
        wrapWidth=screen_width,
        color=exp.config["Text_color"],
        alignText=alignText,
        pos=pos,
    )
    hello_msg.draw()
    exp.win.flip()
    if duration is None:
        # wait for key press
        key = event.waitKeys(keyList=["f7", "return", "space"])
        if key == ["f7"]:
            exp.data_saver.save_beh()
            exp.data_saver.save_triggers()
            logging.critical("Experiment finished by user! {} pressed.".format(key))
            exit(1)
    else:
        # wait for duration
        core.wait(duration)
