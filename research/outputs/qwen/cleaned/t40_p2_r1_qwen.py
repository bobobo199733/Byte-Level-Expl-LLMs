def autocomplete_system(words, prefix):
    suggestions = []
    if not words or not prefix:
        return suggestions
    for word in words:
        if word.startswith(prefix):
            suggestions.append(word)
    suggestions.sort()
    return suggestions