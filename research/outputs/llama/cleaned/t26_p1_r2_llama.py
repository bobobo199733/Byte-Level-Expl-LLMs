from collections import Counter

def min_window_substring(s: str, t: str) -> str:
    """
    Returns the smallest substring of `s` containing all characters from `t`.
    
    :param s: The string to search for a substring in.
    :param t: The string with the characters that must be present in the substring.
    :return: The smallest substring of `s` containing all characters from `t`, or an empty string if no such substring exists.
    """
    if len(t) > len(s):
        return ""

    # Count the frequency of each character in t
    t_count = Counter(t)
    
    # Initialize the required number of unique characters in t
    required_chars = len(t_count)

    # Initialize the left and right pointers for the sliding window
    left = 0
    
    # Initialize the minimum window size and its position
    min_window_size = float('inf')
    min_window_pos = (float('inf'), float('inf))

    # Initialize the number of unique characters in the current window
    formed_chars = 0

    # Initialize the frequency of each character in the current window
    window_counts = {}

    for right, char in enumerate(s):
        # Add the current character to the window counts
        window_counts[char] = window_counts.get(char, 0) + 1

        # If the current character is in t and its count in the window is less than or equal to its count in t,
        # increment the number of formed characters
        if char in t_count and window_counts[char] == t_count[char]:
            formed_chars += 1

        # While the number of formed characters equals the required number of unique characters in t
        while left <= right and formed_chars == required_chars:
            # If the current window size is less than the minimum window size, update the minimum window size and its position
            if right - left + 1 < min_window_size:
                min_window_size = right - left + 1
                min_window_pos = (left, right)

            # Remove the character at the left pointer from the window counts
            window_counts[s[left]] -= 1

            # If the character at the left pointer is in t and its count in the window is less than its count in t,
            # decrement the number of formed characters
            if s[left] in t_count and window_counts[s[left]] < t_count[s[left]]:
                formed_chars -= 1

            # Move the left pointer to the right
            left += 1

    # Return the minimum window substring, or an empty string if no such substring exists
    return "" if min_window_size == float('inf') else s[min_window_pos[0]:min_window_pos[1] + 1]