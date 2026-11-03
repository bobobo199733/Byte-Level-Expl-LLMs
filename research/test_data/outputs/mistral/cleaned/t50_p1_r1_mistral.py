def find_all_anagrams(s, p):
    results = []
    table = {}
    for char in p:
        if char not in table:
            table[char] = 0
        table[char] += 1
    window_size = len(p)
    for i in range(len(s) - window_size + 1):
        substring = s[i:i + window_size]
        count_table = {}
        for char in substring:
            if char not in count_table:
                count_table[char] = 0
            count_table[char] += 1
        if count_table == table:
            results.append(i)
    return sorted(results)