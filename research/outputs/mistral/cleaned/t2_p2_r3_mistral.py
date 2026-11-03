def is_balanced(s: str) -> bool:
    opening_brackets = '([{'
    closing_brackets = ')]}'
    bracket_map = dict(zip(opening_brackets, closing_brackets))
    stack = []
    for bracket in s:
        if bracket in opening_brackets:
            stack.append(bracket)
        elif bracket in closing_brackets:
            if not stack or bracket_map[stack.pop()] != bracket:
                return False
    return len(stack) == 0