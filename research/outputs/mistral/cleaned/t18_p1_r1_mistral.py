def edit_distance(word1, word2):
    len1 = len(word1) + 1
    len2 = len(word2) + 1
    matrix = [[0] * len2 for _ in range(len1)]
    for i in range(len1):
        matrix[i][0] = i
    for j in range(len2):
        matrix[0][j] = j
    for i in range(1, len1):
        for j in range(1, len2):
            if word1[i - 1] == word2[j - 1]:
                cost = 0
            else:
                cost = 1
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + cost)
    return matrix[-1][-1]