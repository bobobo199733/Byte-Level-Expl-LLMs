def text_justification(words, max_width):
    """
    Format text into fully justified lines.

    :param words: List of words to justify.
    :type words: list[str]
    :param max_width: Maximum width for each line.
    :type max_width: int
    :return: List of strings, each exactly max_width characters long.
    :rtype: list[str]
    """
    lines = []
    current_line = []
    current_width = 0
    for word in words:
        if current_width + len(word) + len(current_line) > max_width:
            lines.append(_justify_line(current_line, max_width))
            current_line = [word]
            current_width = len(word)
        else:
            current_line.append(word)
            current_width += len(word)
    if current_line:
        lines.append(_left_justify_line(current_line, max_width))
    return lines

def _left_justify_line(words, max_width):
    """
    Left-justify a list of words with padding.

    :param words: List of words to left-justify.
    :type words: list[str]
    :param max_width: Maximum width for the line.
    :type max_width: int
    :return: A string representing the justified line, exactly max_width characters long.
    :rtype: str
    """
    line = ' '.join(words) + ' ' * (max_width - len(' '.join(words)))
    return line

def _justify_line(words, max_width):
    """
    Justify a list of words with even spacing.

    :param words: List of words to justify.
    :type words: list[str]
    :param max_width: Maximum width for the line.
    :type max_width: int
    :return: A string representing the justified line, exactly max_width characters long.
    :rtype: str
    """
    total_chars = sum((len(word) for word in words))
    num_gaps = len(words) - 1
    gap_size = (max_width - total_chars) // num_gaps
    if (max_width - total_chars) % num_gaps != 0:
        extra_spaces = max_width - total_chars - num_gaps * gap_size
        for i in range(extra_spaces):
            words[i] += ' '
    line = ' '.join(words)
    return line