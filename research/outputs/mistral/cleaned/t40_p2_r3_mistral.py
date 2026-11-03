def autocomplete_system(words, prefix):
    if not words or not prefix:
        return []
    results = [word for word in words if word.startswith(prefix)]
    return sorted(results)