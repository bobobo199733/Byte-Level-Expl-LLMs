def text_justification(words, max_width):

    def justify_line(line_words, line_length, is_last=False):
        if len(line_words) == 1 or is_last:
            return ' '.join(line_words).ljust(max_width)
        num_gaps = len(line_words) - 1
        spaces_per_gap = (max_width - line_length) // num_gaps
        extra_spaces = (max_width - line_length) % num_gaps
        justified_line = ''
        for i in range(num_gaps):
            justified_line += line_words[i] + ' ' * (spaces_per_gap + 1)
            if i < extra_spaces:
                justified_line += ' '
        justified_line += line_words[-1]
        return justified_line.ljust(max_width)
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
    result.append(' '.join(current_line).ljust(max_width))
    return result