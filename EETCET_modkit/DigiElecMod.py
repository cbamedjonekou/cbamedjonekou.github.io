import math as m
import numpy as np

def dec_to_diffBase(number, base= 2):
    """This function converts numbers from base 10 (decimal) to other number systems.
    [E.g.: base 2 (bin), base 16 (hex), base 8 (octal)]. By default it converts from dec to bin.
    It takes in one argument, number, which is expected to be base 10.
    It returns the number as a base 2 number."""
    binList = []
    if number == 0:
        binString = 0
        return str(binString)*4

    while number != 0:

        remainder = number % base

        if base == 16:
            if remainder == 10:
                remainder = 'a'
            elif remainder == 11:
                remainder = 'b'
            elif remainder == 12:
                remainder = 'c'
            elif remainder == 13:
                remainder = 'd'
            elif remainder == 14:
                remainder = 'e'
            elif remainder == 15:
                remainder = 'f'

        binList.append(remainder)
        number = number//base

        if number == 0:
            binList.reverse()
            binString = ''.join(str(i) for i in binList)
            return binString

def diffBase_to_dec(number, base= 2):
    """This function converts numbers from other number systems to base 10 (decimal).
    [E.g.: base 2 (bin), base 16 (hex), base 8 (octal)]. By default it converts from bin to dec.
    It takes in one argument, number, which is expected to be other number systems.
    It returns the number as a base 10 number."""
    number = list(str(number))
    number.reverse()
    decList = []
    for i in range(0,len(number)):

        if base == 16:
            if number[i] == 'a':
                number[i] = 10
            elif number[i] == 'b':
                number[i] = 11
            elif number[i] == 'c':
                number[i] = 12
            elif number[i] == 'd':
                number[i] = 13
            elif number[i] == 'e':
                number[i] = 14
            elif number[i] == 'f':
                number[i] = 15

        digit = int(number[i]) * m.pow(base, i)
        decList.append(digit)
    arr1 = np.array(decList)
    return int(np.sum(arr1))

def hex_to_bin(number, base= 16):
    """This function converts numbers from hex to base 2 (bin).
    It takes in one argument, number, which is expected to be hex.
    It returns the number as a base 2 number."""
    number = list(str(number))
    for i in range(0,len(number)):

        if base == 16:
            if number[i] == 'a':
                number[i] = 10
            elif number[i] == 'b':
                number[i] = 11
            elif number[i] == 'c':
                number[i] = 12
            elif number[i] == 'd':
                number[i] = 13
            elif number[i] == 'e':
                number[i] = 14
            elif number[i] == 'f':
                number[i] = 15

    number = list(map(int, number))
    bit = [dec_to_diffBase(hexDgt) for hexDgt in number]
    bit = [('0' * (4 - len(x)) + x) if len(x) < 4 else x for x in bit]
    output = ''
    for binary in bit:
        output = output + binary
    return int(output)

def bin_to_hex(number, base= 16):
    """This function converts numbers from bin to base 16 (hex).
    It takes in one argument, number, which is expected to be bin.
    It returns the number as a base 16 number."""
    toDec = diffBase_to_dec(number)
    toHex = dec_to_diffBase(toDec, base= 16)
    return toHex
