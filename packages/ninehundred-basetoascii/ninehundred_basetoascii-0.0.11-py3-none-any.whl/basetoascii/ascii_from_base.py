import binascii

@staticmethod
def convert_to_string(user_input, chunk_size, from_base):
    """turns input into ascii"""
    string_output = ""
    for i in range(0, len(user_input), chunk_size):
            string_output += chr(int(user_input[i:i + chunk_size], from_base))
    #print(string_output)
    return string_output
