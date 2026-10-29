import ast
import json

print(json.loads('{"course": 1, "seats": 2}'))
print(ast.literal_eval("[10, 20, 30]"))
try:
    ast.literal_eval("__import__('os').getcwd()")
except ValueError:
    print("ValueError: refused to run code")
