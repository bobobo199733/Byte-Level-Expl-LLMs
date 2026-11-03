def text_justification(words, max_width):
    """
    Takes a list of words and a maximum line width, 
    and returns a list of fully justified strings.

    :param words: List of words to be justified.
    :type words: list
    :param max_width: Maximum allowed width for each line.
    :type max_width: int
    :return: A list of justified lines as strings.
    :rtype: list
    """
    result = []
    current_line = []
    current_length = 0
    for word in words:
        if current_length + len(word) + len(current_line) > max_width:
            justification_spaces = ' '.join([' ' * (max_width - len(''.join(current_line))) // len(current_line)] + [' '] * (max_width - len(''.join(current_line)) % len(current_line)))
            if len(current_line) == 1:
                justification_spaces = ' ' * (max_width - len(''.join(current_line)))
            result.append(justification_spaces + ''.join(current_line))
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += len(word)
    justification_spaces = ' '.join([' ' * (max_width - len(''.join(current_line))) // len(current_line)] + [' '] * (max_width - len(''.join(current_line)) % len(current_line)))
    if len(current_line) == 1:
        justification_spaces = ' ' * (max_width - len(''.join(current_line)))
    result.append(justification_spaces + ''.join(current_line))
    return result