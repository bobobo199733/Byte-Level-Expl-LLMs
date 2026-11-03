def text_justification(words, max_width):
    """
    Justify the given list of words to fit within the specified maximum line width.
    
    Args:
        words (list): A list of words to be justified.
        max_width (int): The maximum allowed line width.
        
    Returns:
        list: A list of justified lines.
    """
    lines = []
    current_line = []
    total_chars = 0
    for word in words:
        if total_chars + len(current_line) + len(word) > max_width:
            lines.append(justify_line(current_line, max_width))
            current_line = [word]
            total_chars = len(word)
        else:
            current_line.append(word)
            total_chars += len(word)
    if current_line:
        lines.append(' '.join(current_line).ljust(max_width))
    return lines

def justify_line(words, max_width):
    """
    Justify a single line of words by spreading spaces evenly between them.
    
    Args:
        words (list): A list of words to be justified.
        max_width (int): The maximum allowed line width.
        
    Returns:
        str: The justified line as a string.
    """
    total_chars = sum((len(word) for word in words))
    num_spaces = max_width - total_chars
    space_between_words = ' ' if len(words) == 1 else num_spaces // (len(words) - 1)
    justified_line = ''
    for i, word in enumerate(words):
        justified_line += word
        if i < len(words) - 1:
            justified_line += space_between_words
    num_extra_spaces = (max_width - len(justified_line)) // (len(words) - 1)
    justified_line = ' ' * num_extra_spaces + justified_line
    return justified_line