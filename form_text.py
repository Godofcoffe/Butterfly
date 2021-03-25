def style_text(s, txt):
    """
To edit the text font:
     s = 'underline, negative or bold'
     txt = 'text'
    """
    if s == 'bold':
        return '\033[1m{}\033[m'.format(txt)
    elif s == 'underline':
        return '\033[4m{}\033[m'.format(txt)
    elif s == 'negative':
        return '\033[7m{}\033[m'.format(txt)


def color_text(c, txt):
    """
To edit the text color:
     c = 'color'
     txt = 'text'
    """
    if c == 'red':
        return '\033[31m{}\033[m'.format(txt)
    elif c == 'white':
        return '\033[30m{}\033[m'.format(txt)
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


def back_text(c, txt):
    """
To edit the text background:
         c = 'color'
         txt = 'text'
    """
    if c == 'red':
        return '\033[41m{}\033[m'.format(txt)
    elif c == 'white':
        return '\033[40m{}\033[m'.format(txt)
    elif c == 'green':
        return '\033[42m{}\033[m'.format(txt)
    elif c == 'yellow':
        return '\033[43m{}\033[m'.format(txt)
    elif c == 'blue':
        return '\033[44m{}\033[m'.format(txt)
    elif c == 'cyan':
        return '\033[46m{}\033[m'.format(txt)
    elif c == 'grey':
        return '\033[47m{}\033[m'.format(txt)
