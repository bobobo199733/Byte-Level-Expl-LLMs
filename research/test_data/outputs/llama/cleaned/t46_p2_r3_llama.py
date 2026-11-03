def text_justification(words, max_width):
    """
    Formats text into fully justified lines.

    Args:
        words (list): List of words to be formatted.
        max_width (int): Maximum width for each line.

    Returns:
        list: A list of strings, each exactly max_width characters long.
    """
    result = []
    current_line = []
    current_length = 0
    for word in words:
        if current_length + len(word) + len(current_line) > max_width:
            result.append(justify_line(current_line, max_width))
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += len(word)
    if current_line:
        result.append(justify_last_line(current_line, max_width))
    return result

def justify_line(words, max_width):
    """
    Distributes spaces as evenly as possible between words on each line.

    Args:
        words (list): List of words on a single line.
        max_width (int): Maximum width for this line.

    Returns:
        str: A string representing the justified line.
    """
    total_length = sum((len(word) for word in words))
    spaces = max_width - total_length
    num_slots = len(words)
    if num_slots == 1:
        return words[0] + ' ' * (max_width - len(words[0]))
    base_spaces = spaces // (num_slots - 1)
    extra_spaces = spaces % (num_slots - 1)
    line = ''
    for i, word in enumerate(words):
        if line:
            line += ' '
        line += word
        line += ' ' * base_spaces
        if i < extra_spaces:
            line += ' '
    return line

def justify_last_line(words, max_width):
    """
    Formats the last line as left-justified: single space between words, padded with trailing spaces.

    Args:
        words (list): List of words on a single line.
        max_width (int): Maximum width for this line.

    Returns:
        str: A string representing the last line.
    """
    result = ' '.join(words)
    return result + ' ' * (max_width - len(result))