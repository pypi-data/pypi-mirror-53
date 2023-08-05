# __main__.py

"""This programme takes a bunch of binary numbers for user input
and converts this to a string and outputs it"""

# TODO - make this a proper callable and usable class

import ascii_from_base
import ascii_from_hex


class ConvertBase():
    def __init__(self, user_input, chunk_size, from_base):
        self.user_input = user_input
        self.chunk_size = chunk_size
        self.from_base = from_base

    @classmethod
    def convert_base(user_input, chunk_size, from_base):

        if from_base == 2:
            print(ascii_from_base.convert_to_string(self.user_input,
                                                    self.chunk_size,
                                                    self.from_base))
        elif from_base == 16:
            print(ascii_from_hex.convert_to_string(self.user_input))

"""
if __name__ == "__main__":
    main(user_input, chunk_size, from_base)
"""


"""
quit = False
while quit == False:
    user_in = str(input("enter numbers or 'quit': " ))
    chunko = int(input("enter chunk size: " ))
    base_in = int(input("from what base?:"))
    ConvertBase(user_in, chunko, base_in)
    if user_in == "quit":
        quit = True
"""


"""
py ConvertBase.py
"""
