import os
import string


def resource_path(relative_path: string):
    PATH = os.path.dirname(os.path.dirname(__file__))

    return PATH + relative_path