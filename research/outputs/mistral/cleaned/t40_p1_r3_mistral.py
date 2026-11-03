def autocomplete_system(words, prefix):
    if not words or not prefix:
        return []

    def get_matches(word):
        return word.startswith(prefix)
    matches = [word for word in words if any((c1 == c2 for c1, c2 in zip(word[len(prefix):], prefix)))]
    sorted_matches = sorted(matches, key=lambda word: sum([abs(ord(w) - ord(p)) for w, p in zip(word, prefix)]))
    return sorted_matches