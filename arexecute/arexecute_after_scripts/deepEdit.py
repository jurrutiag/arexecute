import time
from shutil import copyfile
import sys

def checkArgument(arg):
    return "-" + arg in sys.argv


def getArgument(arg):
    return sys.argv[sys.argv.index("-" + arg) + 1]

if checkArgument("i"):
    i = getArgument("i")

fName = "P" + str(i) + ".dat"
src = "C:/Users/Juan Urrutia/Documents/DeepEdit/nod/JavaLF.dat"
dst = "D:/Docs universidad/7mo Semestre/Sistemas de energía y equipos eléctricos/Tarea1/Tarea 1/Flujos/Flujos Pdelta Qdelta/" + fName

time.sleep(3)
copyfile(src, dst)