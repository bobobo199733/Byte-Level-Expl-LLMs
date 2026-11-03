def text_justification(words, max_width):

    def justify_line(line_words, width, last=False):
        if len(line_words) == 1 or last:
            return ' '.join(line_words).ljust(width)
        num_gaps = len(line_words) - 1
        spaces = (width - sum((len(word) for word in line_words))) // num_gaps
        extra_spaces = (width - sum((len(word) for word in line_words))) % num_gaps
        justified_line = ''
        for i, word in enumerate(line_words):
            justified_line += word + ' '
            if i < extra_spaces:
                justified_line += ' ' * (spaces + 1)
            else:
                justified_line += ' ' * spaces
        return justified_line.strip()
    result = []
    current_line = []
    current_width = 0
    for word in words:
        if len(current_line) == 0:
            current_width = len(word)
        else:
            current_width += len(word) + 1
        if current_width > max_width:
            result.append(justify_line(current_line, max_width))
            current_line = [word]
            current_width = len(word) + 1
        else:
            current_line.append(word)
    result.append(' '.join(current_line).ljust(max_width))
    return result