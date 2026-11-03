def text_justification(words, max_width):
    lines = []
    current_line = []
    total_length = 0
    for word in words:
        if total_length + len(word) + len(current_line) > max_width:
            lines.append(' '.join(current_line))
            current_line = [word]
            total_length = len(word)
        else:
            current_line.append(word) if total_length > 0 else current_line.insert(0, word)
            total_length += len(word) + 1
    lines.append(' '.join(current_line))
    return lines