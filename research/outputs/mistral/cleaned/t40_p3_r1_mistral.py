def autocomplete_system(words, prefix):
    matches = [word for word in words if word.startswith(prefix)]
    matches.sort()
    return matches