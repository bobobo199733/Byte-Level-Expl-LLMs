def text_justification(words, max_width):
    """
    Justify a list of words into lines.

    Args:
        words (list): List of words.
        max_width (int): Maximum width of each line.

    Returns:
        list: A list of justified lines.
    """
    result = []
    current_line = []
    total_length = 0
    for word in words:
        if total_length + len(current_line) + len(word) > max_width:
            result.append(justify_line(current_line, max_width))
            current_line = [word]
            total_length = len(word)
        else:
            current_line.append(word)
            total_length += len(word)
    if current_line:
        result.append(' '.join(current_line).ljust(max_width))
    return result

def justify_line(words, max_width):
    """
    Justify a line of words.

    Args:
        words (list): List of words.
        max_width (int): Maximum width of the line.

    Returns:
        str: A justified string.
    """
    total_length = sum((len(word) for word in words))
    num_spaces = max_width - total_length
    spaces_between_words = len(words) - 1
    if spaces_between_words == 0:
        return words[0] + ' ' * num_spaces
    space_per_word = num_spaces // spaces_between_words
    remaining_spaces = num_spaces % spaces_between_words
    justified_string = ''
    for i in range(len(words)):
        justified_string += words[i]
        if i < len(words) - 1:
            justified_string += ' ' * (space_per_word + (1 if i < remaining_spaces else 0))
    return justified_string