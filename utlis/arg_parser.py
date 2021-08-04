from sys import argv

def getArg(flag, default = None):
    for i, v in enumerate(argv):
        if v == flag:
            if len(argv) < i + 2:
                break
            return argv[i+1]
    return default