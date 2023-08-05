
@staticmethod
def convert_to_string(user_input):
    return binascii.unhexlify(user_input).decode(encoding="utf-8")
