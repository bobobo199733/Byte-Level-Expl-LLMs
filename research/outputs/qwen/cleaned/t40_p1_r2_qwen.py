def autocomplete_system(words, prefix):
    if not words or not prefix:
        return []
    prefix_map = {}
    for word in words:
        current_node = prefix_map
        for char in word:
            if char not in current_node:
                current_node[char] = {}
            current_node = current_node[char]
        current_node['#'] = '#'

    def dfs(node, path):
        result = []
        if '#' in node:
            result.append(path)
        for char in node:
            if char != '#':
                result.extend(dfs(node[char], path + char))
        return result
    current_node = prefix_map
    for char in prefix:
        if char not in current_node:
            return []
        else:
            current_node = current_node[char]
    suggestions = dfs(current_node, prefix)
    return sorted(suggestions)