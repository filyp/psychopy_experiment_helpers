import time

from psychopy import logging


def create_eeg_port():
    try:
        import parallel

        port = parallel.Parallel()
        port.setData(0x00)
        return port
    except:
        raise Exception("Can't connect to EEG")


class TriggerHandler:
    def __init__(self, port_eeg, data_saver):
        self.port_eeg = port_eeg
        self.data_saver = data_saver
        self.trigger_no = 0

    def prepare_trigger(self, trigger_name):
        self.trigger_no += 1
        if self.trigger_no == 9:
            self.trigger_no = 1
        line = f"{self.trigger_no}:{trigger_name}"
        self.data_saver.triggers_list.append(line)

    def send_trigger(self):
        logging.data("TRIGGER: " + self.data_saver.triggers_list[-1])
        if self.port_eeg is not None:
            try:
                self.port_eeg.setData(self.trigger_no)
                time.sleep(0.005)
                self.port_eeg.setData(0x00)
                time.sleep(0.005)
            except Exception as ex:
                logging.error(ex)
                pass
