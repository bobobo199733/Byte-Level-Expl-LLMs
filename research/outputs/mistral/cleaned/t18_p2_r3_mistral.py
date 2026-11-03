def edit_distance(word1, word2):
    if not word1 and (not word2):
        return 0
    matrix = []
    len1 = len(word1) + 1
    len2 = len(word2) + 1
    for i in range(len1):
        matrix.append([i] + [None] * len2)
    for j in range(len2):
        row = [None] * (len1 + 1)
        row[0] = j
        matrix[-1] = row
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if word1[i - 1] == word2[j - 1]:
                cost = 0
            else:
                cost = 1
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + cost)
    return matrix[-1][-1]