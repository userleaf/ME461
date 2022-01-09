#/usr/bin/python3
from optparse import OptionParser
from math import *
if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()
    if len(args) < 1:
        print('pass something')
    else:
        for current_arg in args:
            try:
                res = eval(current_arg)
                print(str(current_arg)+'='+str(res))
            except:
                print('it did not work')
else:
    pass
