# nottelib.py
# library for commonly used functions that do not need to be their own Cog/Inside each function
# P.S. you should have done this ages ago

# okay this one is why i made the file so here we go
# checks if the user is in a

import asyncio
import datetime
import pickle  # used for VDB/Disk

from cns import *


async def sanitize(self, ctx, bot):
    print("Hello it is me, sanitize")

    pass


def nprint(self, ctx, var):
    print("Hello it is me, nprint, I am printing:\n")
    print(var)

    pass


def spw(self, data, filename):

    fn = './pk/'
    fn = fn+str(filename)
    dbfile = open(fn, 'wb')
    pickle.dump(data, dbfile)
    dbfile.close()


def spa(self, data, filename):

    fn = './pk/'
    fn = fn+str(filename)
    dbfile = open(fn, 'ab')
    pickle.dump(data, dbfile)
    dbfile.close()


def spl(self, filename):

    fn = './pk/'
    fn = fn+str(filename)
    print("Opening Pickle: ", filename)
    with open(fn, 'rb') as f:
        result = pickle.load(f)
    f.close()
    # return objs
    if result:
        return result


def namez(self, classname):
    testcommand = 3
    t = str(testcommand)
    print(t)
