import speech_recognition as sr
from ctypes import *
from contextlib import contextmanager

# This starting chunk of code is only used to avoid the annoying ALSA errors to be printed,
# they are not related to the project. The code related to the project is the Listener class.
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)


def py_error_handler(filename, line, function, err, fmt):
    pass


c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)


@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)

# print(sr.Microphone.list_microphone_names())
# print(sr.Microphone.list_working_microphones())


class Listener:
    """Even if not used as a class but only via static method call,
    I prefer to maintain the class for code coherence."""
    def __int__(self):
        # self.recognizer = sr.Recognizer()

        # self.mic = sr.Microphone()
        # print(self.mic)
        pass

    @staticmethod
    def listen():
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 50

        with noalsaerr(), sr.Microphone() as source:
            print("Tell me what you want!")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source)

        phrase_list = recognizer.recognize_google(audio, show_all=True)

        # print(phrase_list)

        # Here a brief way to rank the possible phrases listened by the recognizer,
        # trying to rank first the one with more words that are relevant to my task.
        chosen_phrase = ""
        max_points = 0

        if phrase_list:
            for phrase in phrase_list["alternative"]:
                keywords = [word for word in phrase["transcript"].split() if word in ["gin", "vermut", "lemon", "campari", "Baxter", "Campari", "Negroni", "negroni", "martini", "Martini"]]
                points = len(keywords)
                if points > max_points:
                    max_points = points
                    chosen_phrase = phrase["transcript"]

        # print(type(phrase))
        # print(chosen_phrase)

        return chosen_phrase


"""
# this is for debug purposes
if __name__ == "__main__":
    Ears = Listener()
    phrase = Ears.listen()
    print(phrase)
"""