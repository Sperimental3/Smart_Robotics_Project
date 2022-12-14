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
    def __int__(self):
        #self.recognizer = sr.Recognizer()

        #self.mic = sr.Microphone()
        #print(self.mic)
        pass

    @staticmethod
    def listen():
        recognizer = sr.Recognizer()

        with noalsaerr(), sr.Microphone() as source:
            print("Tell me what you want!")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source)

        phrase = recognizer.recognize_google(audio)
        print(phrase)
        # print(type(phrase))

        return phrase
