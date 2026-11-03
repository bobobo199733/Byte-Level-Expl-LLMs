def text_justification(words, max_width):

    def justify_line(line_words, line_length, is_last_line=False):
        if len(line_words) == 1 or is_last_line:
            return ' '.join(line_words).ljust(max_width)
        num_gaps = len(line_words) - 1
        total_spaces = max_width - line_length
        if is_last_line:
            return ' '.join(line_words) + ' ' * (max_width - line_length)
        even_spaces, extra_spaces = divmod(total_spaces, num_gaps)
        justified_line = []
        for i in range(num_gaps):
            justified_line.append(line_words[i])
            justified_line.append(' ' * (even_spaces + 1) if i < extra_spaces else ' ' * even_spaces)
        justified_line.append(line_words[-1])
        return ''.join(justified_line)
    result = []
    current_line = []
    current_length = 0
    for word in words:
        if current_length + len(word) + len(current_line) > max_width:
            result.append(justify_line(current_line, current_length))
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += len(word)
    result.append(justify_line(current_line, current_length, is_last_line=True))
    return result