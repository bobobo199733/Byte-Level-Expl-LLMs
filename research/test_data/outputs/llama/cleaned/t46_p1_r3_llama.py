def text_justification(words, max_width):
    """
    Fully justifies a list of words within a maximum width.

    Args:
        words (list): A list of words to justify.
        max_width (int): The maximum line width.

    Returns:
        list: A list of fully justified strings, each exactly max_width characters wide.
    """
    result = []
    current_line = []
    for word in words:
        if len(current_line) + len(word) + 1 <= max_width:
            current_line.append(word)
        else:
            result.append(justify_line(current_line, max_width))
            current_line = [word]
    if current_line:
        last_line = ' '.join(current_line) + ' ' * (max_width - len(' '.join(current_line)))
        result.append(last_line)
    return result

def justify_line(words, max_width):
    """
    Fully justifies a list of words within a maximum width.

    Args:
        words (list): A list of words to justify.
        max_width (int): The maximum line width.

    Returns:
        str: A fully justified string, exactly max_width characters wide.
    """
    word_count = len(words)
    total_spaces = max_width - sum((len(word) for word in words))
    if word_count == 1:
        return words[0] + ' ' * total_spaces
    base_spaces = total_spaces // (word_count - 1)
    extra_spaces = total_spaces % (word_count - 1)
    justified_line = ''
    for i, word in enumerate(words):
        justified_line += word + (' ' * base_spaces + ' ') * (i < extra_spaces)
    return justified_line