def autocomplete_system(words, prefix):
    if not words or not prefix:
        return []
    suggestions = [word for word in words if word.startswith(prefix)]
    sorted_suggestions = sorted(suggestions)
    return sorted_suggestions