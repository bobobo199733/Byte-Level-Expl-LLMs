def autocomplete_system(words, prefix):
    if not words or not prefix:
        return []
    suggestions = [word for word in words if word.startswith(prefix)]
    suggestions.sort()
    return suggestions