def text_justification(words, max_width):
    lines = []
    current_line = []
    total_spaces = 0
    for word in words:
        if sum((len(w) for w in current_line)) + len(word) + total_spaces > max_width:
            lines.append(' '.join(current_line))
            current_line = [word]
            total_spaces = 0
        elif total_spaces == 0:
            current_line.append(word)
            total_spaces += len(word) + 1
        else:
            spaces_to_add = min(max_width - sum((len(w) for w in current_line)) - len(word), total_spaces)
            current_line[-1] += ' ' * spaces_to_add
            current_line.append(word)
            total_spaces -= spaces_to_add + 1
    lines.append(' '.join(current_line))
    last_line = lines[-1]
    num_words = len(last_line.split())
    if num_words < len(words) or (num_words == len(words) and max_width - len(last_line) > 1):
        lines[-1] += ' ' * (max_width - len(last_line))
    return lines