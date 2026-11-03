def text_justification(words, max_width):

    def get_lines(line, spaces_left, lines):
        if not line:
            return lines + [spaces_left * ' ']
        space_needed = max_width - sum((len(word) for word in line))
        if space_needed < len(spaces_left):
            spaces_left = spaces_left[space_needed:]
            lines.append(' '.join(line))
            return get_lines(spaces_left, spaces_left, lines)
        extra_spaces = space_needed - len(spaces_left)
        spaces_left += extra_spaces * ' '
        line[0] += spaces_left.pop(0)
        lines.append(' '.join(line))
        return get_lines(spaces_left, spaces_left, lines)
    if not words:
        return []
    words.sort(key=len, reverse=True)
    lines = [' '.join(words[:i]) for i in range(1, len(words))]
    remaining_words = words[len(words) - 1:]
    spaces = [0] + [' ' * (max_width - len(word)) for word in lines]
    lines += get_lines(''.join(remaining_words), spaces[-1], [])
    return lines