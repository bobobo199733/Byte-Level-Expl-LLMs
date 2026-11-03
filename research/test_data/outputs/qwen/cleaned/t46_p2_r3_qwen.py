def text_justification(words, max_width):

    def justify_line(line_words, line_length, is_last_line=False):
        if len(line_words) == 1 or is_last_line:
            return ' '.join(line_words).ljust(max_width)
        num_gaps = len(line_words) - 1
        spaces_needed = max_width - line_length
        base_spaces, extra_spaces = divmod(spaces_needed, num_gaps)
        justified_line = []
        for i in range(len(line_words)):
            word = line_words[i]
            if i < extra_spaces:
                justified_line.append(word + ' ' * (base_spaces + 1))
            else:
                justified_line.append(word + ' ' * base_spaces)
        return ''.join(justified_line).rstrip().ljust(max_width)
    result = []
    current_line_words, line_length = ([], 0)
    for word in words:
        if line_length + len(word) + len(current_line_words) <= max_width:
            current_line_words.append(word)
            line_length += len(word)
        else:
            result.append(justify_line(current_line_words, line_length))
            current_line_words = [word]
            line_length = len(word)
    if current_line_words:
        result.append(justify_line(current_line_words, line_length, is_last_line=True))
    return result