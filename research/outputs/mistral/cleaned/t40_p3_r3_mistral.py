def autocomplete_system(words, prefix):
    matches = [word for word in words if word.startswith(prefix)]
    return sorted(matches)