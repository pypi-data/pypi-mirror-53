def clapify(input_string, padding_spaces=1):
    assert isinstance(input_string, str), "Invalid input. input must be a string"
    result = "{pad}👏{pad}".format(pad=" " * padding_spaces).join(input_string.split())
    return result