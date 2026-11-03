import ast
import operator

def safe_eval(expr: str) -> int:
    expr = expr.replace(' ', '')
    operators = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.floordiv}
    try:
        node = ast.parse(expr, mode='eval')
        safe_node = ast.Expression(node.body)

        def eval_expr(node):
            if isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.BinOp):
                left_val = eval_expr(node.left)
                right_val = eval_expr(node.right)
                return operators[type(node.op).__name__](left_val, right_val)
            elif isinstance(node, ast.UnaryOp):
                operand = eval_expr(node.operand)
                if type(node.op) == ast.USub:
                    return -operand
                else:
                    raise ValueError('Unsupported unary operator')
            else:
                raise ValueError('Unsupported node type')
        result = eval_expr(safe_node.body)
        return int(result)
    except (SyntaxError, ValueError):
        raise ValueError('Invalid expression')