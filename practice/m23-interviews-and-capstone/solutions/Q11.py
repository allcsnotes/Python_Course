# Q11 - Compiled or interpreted?
import dis

source = "total = price * 2 + tax"
code = compile(source, "<demo>", "exec")      # step 1: source text -> bytecode
print(type(code).__name__, code.co_names)
dis.dis(code)                                 # step 2 happens in the virtual machine
exec(code, {"price": 100, "tax": 18})         # the VM runs the bytecode
