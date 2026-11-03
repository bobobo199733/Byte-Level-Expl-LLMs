def edit_distance(word1, word2):
    len1 = len(word1) + 1
    len2 = len(word2) + 1
    matrix = [[0 for _ in range(len2)] for _ in range(len1)]
    for i in range(len1):
        for j in range(len2):
            if i == 0:
                matrix[i][j] = j
            elif j == 0:
                matrix[i][j] = i
            else:
                cost = 0
                if word1[i - 1] != word2[j - 1]:
                    cost += 1
                matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + cost)
    return matrix[len1 - 1][len2 - 1]