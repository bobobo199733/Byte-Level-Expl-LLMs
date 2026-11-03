def text_justification(words, max_width):
    """
    Justify a list of words within a maximum width.

    :param words: List of words to justify
    :type words: list[str]
    :param max_width: Maximum line width
    :type max_width: int
    :return: List of justified strings
    :rtype: list[str]
    """
    result = []
    current_line = []
    current_width = 0
    for word in words:
        if current_width + len(word) + len(current_line) > max_width:
            if len(current_line) > 1:
                gap_size = (max_width - current_width) // (len(current_line) - 1)
                extra_spaces = (max_width - current_width) % (len(current_line) - 1)
                justified_line = ''
                for i in range(len(current_line)):
                    justified_line += current_line[i]
                    if i < len(current_line) - 1:
                        justified_line += ' ' * gap_size
                        if extra_spaces > 0:
                            justified_line += ' '
                            extra_spaces -= 1
            else:
                justified_line = ' '.join(current_line).ljust(max_width)
            result.append(justified_line)
            current_line = []
            current_width = 0
        current_line.append(word)
        current_width += len(word)
    if current_line:
        justified_line = ' '.join(current_line).ljust(max_width)
        result.append(justified_line)
    return result