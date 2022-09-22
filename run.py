# -*- coding: utf-8 -*-
# how to run:
# venv/bin/python main.py config/some_task.yaml

import os
import sys
import json
import shutil
import hashlib

import yaml
from psychopy import logging

# ERROR, WARNING, DATA, EXP, INFO and DEBUG
# logging.console.setLevel(logging.EXP)
logging.console.setLevel(logging.DATA)

from psychopy_experiment_helpers.experiment_info import get_participant_info

from psychopy_experiment_helpers.save_data import DataSaver
from psychopy_experiment_helpers.screen import create_win
from psychopy_experiment_helpers.experiment_info import display_eeg_info

__author__ = ["ociepkam", "filyp"]


def load_config(config_path):
    try:
        with open(config_path, encoding="utf8") as yaml_file:
            config = yaml.safe_load(yaml_file)
    except:
        raise Exception("Can't load config file")

    # compute hash of config file to know for sure which config version was used
    unique_config_string = json.dumps(config, sort_keys=True, ensure_ascii=True)
    short_hash = hashlib.sha1(unique_config_string.encode("utf-8")).hexdigest()[:6]

    return config, short_hash


def run(procedure):
    # Load config
    config_path = sys.argv[1]
    config, config_hash = load_config(config_path)
    experiment_name = os.path.split(config_path)[-1]
    experiment_name = experiment_name.split(".")[0]
    experiment_name = experiment_name + "_" + config_hash

    if config.get("Actiview_reminder", False):
        display_eeg_info()
    participant_info, experiment_version = get_participant_info(
        config.get("Ask_for_experiment_version", False)
    )
    config["Experiment_version"] = experiment_version

    data_saver = DataSaver(participant_info, experiment_name, beh=[], triggers_list=[])
    # copy config file to results folder
    os.makedirs(data_saver.directory, exist_ok=True)
    shutil.copy2(config_path, data_saver.directory)
    logging.data(f"Experiment name: {experiment_name}")

    # screen
    screen_number = config.get("Screen_number", -1)
    win, screen_res = create_win(screen_color=config["Screen_color"], screen_number=screen_number)

    # Experiment
    procedure(
        win=win,
        screen_res=screen_res,
        config=config,
        data_saver=data_saver,
    )

    # Save data
    data_saver.save_beh()
    data_saver.save_triggers()
