def text_justification(words, max_width):
    if not words:
        return []
    lines = [words[0]]
    current_line_len = len(words[0])
    for word in words[1:]:
        line_len = min(current_line_len + len(word) + 1, max_width)
        if line_len - len(word) > current_line_len:
            spaces_count = line_len - len(word) - current_line_len
            line = [word] + [' ' for _ in range(spaces_count)]
            lines.append(' '.join(line))
            current_line_len = line_len
        else:
            lines[-1] += ' ' + word
            current_line_len = line_len
    last_line = ' '.join(lines[-1:])
    if len(last_line) < max_width:
        last_line += ' ' * (max_width - len(last_line))
    lines.append(last_line)
    return lines