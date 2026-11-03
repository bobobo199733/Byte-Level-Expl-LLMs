def text_justification(words, max_width):
    """
    Formats text into fully justified lines.

    Args:
        words (list): A list of words to be justified.
        max_width (int): The maximum width of each line.

    Returns:
        list: A list of strings, each exactly max_width characters long.
    """
    result = []
    current_line = []
    current_width = 0
    for word in words:
        if current_width + len(word) + len(current_line) > max_width:
            justified_line = _justify_line(current_line, max_width)
            result.append(justified_line)
            current_line = [word]
            current_width = len(word)
        else:
            current_line.append(word)
            current_width += len(word)
    if current_line:
        justified_line = _left_justify(current_line, max_width)
        result.append(justified_line)
    return result

def _justify_line(words, max_width):
    """
    Justifies a single line by distributing spaces evenly.

    Args:
        words (list): A list of words on the current line.
        max_width (int): The maximum width of the line.

    Returns:
        str: The justified line as a string.
    """
    num_spaces = max_width - sum((len(word) for word in words))
    if len(words) == 1:
        return ' '.join(words) + ' ' * (num_spaces - 1)
    base_spaces = num_spaces // (len(words) - 1)
    extra_spaces = num_spaces % (len(words) - 1)
    justified_line = ''
    for i, word in enumerate(words):
        justified_line += word
        if i < len(words) - 1:
            justified_line += ' ' * base_spaces
            if extra_spaces > 0:
                justified_line += ' '
                extra_spaces -= 1
    return justified_line

def _left_justify(words, max_width):
    """
    Left-justifies a single line by adding spaces between words.

    Args:
        words (list): A list of words on the current line.
        max_width (int): The maximum width of the line.

    Returns:
        str: The left-justified line as a string.
    """
    justified_line = ' '.join(words)
    return justified_line + ' ' * (max_width - len(justified_line))