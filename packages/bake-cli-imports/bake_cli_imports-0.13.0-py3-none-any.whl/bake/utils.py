import os


def scrub_hidden_tasks(names):

    hidden_char = "//"
    _names = []
    for name in names:
        if hidden_char not in str(name):
            _names.append(name)

    return _names


def walk_up(bottom):
    """mimic os.walk, but walk 'up' instead of down the directory tree.
    From: https://gist.github.com/zdavkeos/1098474
    """

    bottom = os.path.realpath(bottom)

    # get files in current dir
    try:
        names = os.listdir(bottom)
    except Exception:
        return

    dirs, nondirs = [], []
    for name in names:
        if os.path.isdir(os.path.join(bottom, name)):
            dirs.append(name)
        else:
            nondirs.append(name)

    yield bottom, dirs, nondirs

    new_path = os.path.realpath(os.path.join(bottom, ".."))

    # see if we are at the top
    if new_path == bottom:
        return

    for x in walk_up(new_path):
        yield x
