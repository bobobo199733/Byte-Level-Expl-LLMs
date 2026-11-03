def text_justification(words, max_width):
    """
    Given a list of words and a max line width,
    return a list of justified lines.

    :param words: List of words
    :type words: list[str]
    :param max_width: Maximum line width
    :type max_width: int
    :return: List of justified lines
    :rtype: list[str]
    """
    result = []
    current_line = []
    current_width = 0
    for word in words:
        if current_width + len(word) + len(current_line) > max_width:
            result.append(_justify_line(current_line, max_width))
            current_line = [word]
            current_width = len(word)
        else:
            current_line.append(word)
            current_width += len(word)
    if current_line:
        result.append(' '.join(current_line).ljust(max_width))
    return result

def _justify_line(words, max_width):
    """
    Justify a line of words.

    :param words: List of words on the line
    :type words: list[str]
    :param max_width: Maximum width of the line
    :type max_width: int
    :return: The justified line as a string
    :rtype: str
    """
    total_chars = sum((len(word) for word in words))
    num_spaces = max_width - total_chars
    if num_spaces == 0:
        return ' '.join(words)
    space_between_words = num_spaces // (len(words) - 1)
    extra_spaces = num_spaces % (len(words) - 1)
    result = ''
    for i, word in enumerate(words):
        result += word
        if i < len(words) - 1:
            result += ' ' * space_between_words
            if i < extra_spaces:
                result += ' '
    return result