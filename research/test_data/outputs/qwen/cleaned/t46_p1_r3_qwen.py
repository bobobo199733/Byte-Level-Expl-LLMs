def text_justification(words, max_width):

    def justify_line(line_words, length, is_last=False):
        if len(line_words) == 1:
            return ' '.join(line_words).ljust(max_width)
        num_gaps = len(line_words) - 1
        spaces_per_gap = (max_width - length) // num_gaps
        extra_spaces = (max_width - length) % num_gaps
        justified_line = []
        for i, word in enumerate(line_words):
            gap = ' ' * spaces_per_gap if i < extra_spaces else ' ' * (spaces_per_gap + 1)
            justified_line.append(word + gap)
        return ''.join(justified_line).lstrip()
    result = []
    current_line = []
    total_length = 0
    for word in words:
        if total_length + len(word) + len(current_line) > max_width:
            result.append(justify_line(current_line, total_length))
            current_line = [word]
            total_length = len(word)
        else:
            current_line.append(word)
            total_length += len(word)
    result.append(' '.join(current_line).ljust(max_width))
    return result