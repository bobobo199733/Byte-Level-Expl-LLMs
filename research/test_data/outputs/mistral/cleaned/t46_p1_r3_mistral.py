def text_justification(words, max_width):
    if not words:
        return []
    line = []
    result = []
    for word in words:
        if line and len(line[-1]) + len(word) + 1 > max_width:
            result.append(' '.join(line))
            line = [word]
        elif line:
            spaces_needed = max_width - len(line[-1]) - len(word)
            line[-1] += ' ' * min(spaces_needed, len(word))
            line.append(word)
        else:
            line.append(word)
    if line:
        spaces_needed = max_width - sum((len(word) for word in line))
        result.append(' '.join(line + [' '] * spaces_needed))
    return result