def text_justification(words, max_width):
    if not words:
        return []
    lines = []
    current_line = []
    spaces_remaining = max_width
    for word in words:
        word_length = len(word)
        spaces_to_add = min(spaces_remaining, len(current_line) - 1) * ' '
        if sum([word_length] + list(map(len, current_line))) + spaces_to_add <= max_width:
            current_line.append(word + spaces_to_add)
            spaces_remaining -= word_length + spaces_to_add
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            spaces_remaining -= word_length + 1
    lines.append(' '.join(current_line))
    if len(lines) > 1 and len(lines[-1]) < max_width:
        lines[-1] += ' ' * (max_width - len(lines[-1]))
    return lines