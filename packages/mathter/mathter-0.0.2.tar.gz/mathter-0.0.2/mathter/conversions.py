import math


def BinMaxValueGet(bits):
    return (2 ** bits) - 1

def TwosCompToDec(twosComp, bits):
    return (twosComp - (2 ** bits if twosComp >> (bits - 1) else 0))
