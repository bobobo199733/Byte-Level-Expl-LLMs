class TrieNode:

    def __init__(self):
        self.children = {}
        self.is_word = False

def autocomplete_system(words, prefix):
    root = TrieNode()
    for word in words:
        node = root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True
    suggestions = []

    def dfs(node, prefix):
        if node.is_word:
            suggestions.append(prefix + node.key)
        for char, child in node.children.items():
            dfs(child, prefix + char)
    dfs(root, prefix)
    return sorted(suggestions)