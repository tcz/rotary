import logging
import sys
import os
import time
import linphone
import uuid
import speech_recognition as sr
import tempfile
from commanddispatcher import CommandDispatcher

class Server:
    def __init__(self):
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        self.logger = logging.getLogger('rotary')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(stream_handler)

        self.current_record_file = None

        self.command_dispatcher = CommandDispatcher(self.logger)

    def global_state_changed(self, core, state, message):
        self.logger.warning("global_state_changed: " + str(state) + ", " + message)
        if state == linphone.GlobalState.GlobalOn:
            self.logger.info("core version: " + str(core.version))

    def registration_state_changed(self, core, proxy_cfg, state, message):
        self.logger.info("registration_state_changed: " + str(state) + ", " + message)

    def call_state_changed(self, core, call, state, message):
        self.logger.info("call_state_changed: " + str(state) + ", " + message)

        if state == 1: # Incoming call
            params = call.current_params.copy()
            params.record_file = self.new_recording_file()
            self.core.accept_call_with_params(call, params)
            call.start_recording()
            self.logger.info("Incoming call accepted: " + str(state) + ", " + message)

        if state == 13: # Call ended
            self.logger.info("Call ended")
            self.logger.info("Analyzing audio file " + self.current_record_file)

            r = sr.Recognizer()
            input = sr.AudioFile(self.current_record_file)

            with input as source:
                audio = r.record(source, offset=1.1, duration=3)

                try:
                    recognizedPhrase = r.recognize_google(audio)
                except sr.UnknownValueError:
                    self.logger.warning("Unable to recognize")
                    return
                except sr.RequestError as e:
                    self.logger.error("Unable to reach recognition service {0}".format(e))
                    return

                self.logger.info("Recognized: " + recognizedPhrase)

                self.command_dispatcher.dispatch(recognizedPhrase)

    def new_recording_file(self):
        self.clean_recording_file()
        self.current_record_file = tempfile.gettempdir() + '/call' + str(uuid.uuid4()) + '.wav'
        return self.current_record_file

    def clean_recording_file(self):
        if self.current_record_file is not None and os.path.isfile(self.current_record_file):
            os.remove(self.current_record_file)

    def run(self):

        linphone.set_log_handler(self.log_handler)

        callbacks = {
            'global_state_changed': self.global_state_changed,
            'registration_state_changed': self.registration_state_changed,
            'call_state_changed': self.call_state_changed
        }

        # Create a linphone core and iterate every 20 ms
        self.core = linphone.Core.new(callbacks, None, None)
        self.core.use_files = True
        self.core.play_file = os.path.dirname(os.path.realpath(__file__)) + '/how-can-i-help-you.wav'
        self.new_recording_file()

        while True:
            self.core.iterate()
            time.sleep(0.02)

    def log_handler(self, level, msg):
        method = getattr(self.logger, level)
        method(msg)

def main():
    d = Server()
    d.run()

    return 0

if __name__ == "__main__":
    sys.exit(main())