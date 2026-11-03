def text_justification(words, max_width):
    if not words:
        return []
    lines = [words[0]]
    remaining_words = words[1:]
    current_line_length = len(words[0])
    for word in remaining_words:
        if current_line_length + len(word) + len(words.split()[-1]) <= max_width:
            lines[-1] += ' ' + word
            current_line_length += len(word) + 1
        else:
            lines.append(word)
            current_line_length = len(word)
    last_line = ' '.join(remaining_words)
    last_line_padding = max_width - (len(last_line) + (len(remaining_words) - 1))
    if last_line_padding > 0:
        last_line += ' ' * last_line_padding
    formatted_lines = []
    for line in lines:
        formatted_lines.append(line.rjust(max_width, ' '))
    formatted_lines.append(last_line)
    return formatted_lines