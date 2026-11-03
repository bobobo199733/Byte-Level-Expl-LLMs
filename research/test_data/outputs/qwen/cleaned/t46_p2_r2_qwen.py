def text_justification(words, max_width):

    def justify_line(line_words, width):
        if len(line_words) == 1:
            return line_words[0] + ' ' * (width - len(line_words[0]))
        num_spaces = width - sum((len(word) for word in line_words))
        num_gaps = len(line_words) - 1
        base_spaces = num_spaces // num_gaps
        extra_spaces = num_spaces % num_gaps
        justified_line = ''
        for i, word in enumerate(line_words):
            justified_line += word + ' ' * (base_spaces + (i < extra_spaces))
        return justified_line.rstrip()
    result = []
    current_line = []
    current_length = 0
    for word in words:
        if len(word) + current_length > max_width:
            result.append(justify_line(current_line, max_width))
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += len(word) + 1
    result.append(' '.join(current_line).ljust(max_width))
    return result