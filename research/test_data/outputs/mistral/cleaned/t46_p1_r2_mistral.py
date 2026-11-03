def text_justification(words, max_width):
    if not words:
        return []
    line = []
    lines = []
    for word in words:
        if not line or (len(line) > 0 and len(line[-1]) + len(word) + 1 <= max_width):
            line.append(word + ' ')
        else:
            lines.append(''.join(line))
            line = [word + ' ']
    lines.append(' '.join(line))
    while len(' '.join(lines[-1].split())) < max_width:
        lines[-1] += ' '
    return lines