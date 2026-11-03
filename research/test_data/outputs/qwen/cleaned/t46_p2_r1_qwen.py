def text_justification(words, max_width):
    result = []
    line = []
    current_length = 0

    def add_line():
        nonlocal current_length
        if len(line) == 1:
            result.append(' '.join(line).ljust(max_width))
        else:
            total_spaces = max_width - current_length + len(line)
            num_gaps = len(line) - 1
            extra_spaces = total_spaces // num_gaps if num_gaps > 0 else 0
            extra_spaces_needed = total_spaces % num_gaps if num_gaps > 0 else 0
            justified_line = ''
            for i in range(len(line)):
                justified_line += line[i]
                if i < len(line) - 1:
                    num_spaces = extra_spaces + (i < extra_spaces_needed)
                    justified_line += ' ' * num_spaces
            result.append(justified_line.ljust(max_width))
        line.clear()
        current_length = 0
    for word in words:
        if current_length + len(word) + len(line) <= max_width:
            line.append(word)
            current_length += len(word)
        else:
            add_line()
            line = [word]
            current_length = len(word)
    add_line()
    return result