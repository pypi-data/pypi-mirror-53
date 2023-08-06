import sys
import argparse

def nerum(*args):
    parser = argparse.ArgumentParser()

    for arg in args:

        argument = dict()

        if '#' in arg:
            arg, argument['help'] = arg.split('#')

        if '?' in arg:
            argument['action'] = 'store_true'

        if '+' in arg:
            argument['nargs'] = '+'

        # leave only numbers, letters and '-'
        arg = ''.join(
            x for x in arg
            if x.isalpha()
            or x.isdigit()
            or x == '-'
        )

        parser.add_argument(arg, **argument)

    output = parser.parse_args().__dict__

    for e in output:
        try:
            if isinstance(output[e], list):
                for i in range(len(output[e])):
                    output[e][i] = int(output[e][i])
            output[e] = int(output[e])
        except:
            pass

    return argparse.Namespace(**output)

sys.modules[__name__] = nerum
