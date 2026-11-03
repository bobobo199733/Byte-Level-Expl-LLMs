def text_justification(words, max_width):

    def justify_line(line_words, width, last_line=False):
        if len(line_words) == 1:
            return line_words[0] + ' ' * (width - len(line_words[0]))
        num_gaps = len(line_words) - 1
        extra_spaces = width - sum((len(word) for word in line_words))
        spaces_per_gap, remainder = divmod(extra_spaces, num_gaps)
        if last_line:
            return ' '.join([word + ' ' * (width - sum(map(len, line_words))) // len(line_words) for word in line_words])
        justified_line = []
        for i, word in enumerate(line_words):
            spaces = [spaces_per_gap] * num_gaps
            if remainder > 0:
                spaces[:remainder] = [spaces_per_gap + 1] * remainder
                remainder = 0
            justified_line.append(word)
            for _ in range(spaces[i]):
                justified_line.append(' ')
        return ''.join(justified_line)
    result = []
    line_words = []
    current_width = 0
    for word in words:
        if current_width + len(word) + len(line_words) <= max_width:
            line_words.append(word)
            current_width += len(word)
        else:
            result.append(justify_line(line_words, max_width))
            line_words = [word]
            current_width = len(word)
    if line_words:
        result.append(' '.join(line_words) + ' ' * (max_width - sum((len(w) for w in line_words)) - len(line_words) + 1))
    return result