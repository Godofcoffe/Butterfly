def color_text(c, txt):
    """
To edit the text color:
     c = 'color'
     txt = 'text'
    """
    if c == 'red':
        return '\033[31m{}\033[m'.format(txt)
    elif c == 'white':
        return '\033[97m{}\033[m'.format(txt)
    elif c == 'green':
        return '\033[32m{}\033[m'.format(txt)
    elif c == 'yellow':
        return '\033[33m{}\033[m'.format(txt)
    elif c == 'blue':
        return '\033[34m{}\033[m'.format(txt)
    elif c == 'cyan':
        return '\033[36m{}\033[m'.format(txt)
    elif c == 'grey':
        return '\033[37m{}\033[m'.format(txt)
    elif c == 'magenta':
        return '\033[35m{}\033[m'.format(txt)
