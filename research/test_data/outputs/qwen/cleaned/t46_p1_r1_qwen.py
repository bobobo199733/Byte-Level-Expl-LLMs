def text_justification(words, max_width):

    def justify_line(line_words, width, is_last=False):
        if len(line_words) == 1:
            return line_words[0] + ' ' * (width - len(line_words[0]))
        spaces_needed = width - sum((len(word) for word in line_words))
        gaps = len(line_words) - 1
        base_spaces = spaces_needed // gaps if gaps else 0
        extra_spaces = spaces_needed % gaps if gaps else 0
        justified_line = ''
        for i, word in enumerate(line_words):
            justified_line += word + ' ' * base_spaces
            if i < extra_spaces:
                justified_line += ' '
        return justified_line.rstrip() + ' ' * (width - len(justified_line))
    result = []
    current_line = []
    current_length = 0
    for word in words:
        if current_length + len(word) + len(current_line) > max_width:
            result.append(justify_line(current_line, max_width))
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += len(word)
    result.append(' '.join(current_line).ljust(max_width))
    return result