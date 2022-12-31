from sympy import symbols, solve, diff, Matrix, sign, re
from tutorial5 import SingularPointandType2

x, y = symbols('x, y')
sys1 = [-x-y, x-3*y]
sys2 = [-2*x-5*y, x -5*y]
sys3 = [0.25*x, -3*y]

result1 = SingularPointandType2(x, y, sys1)
print("Sys1 =>", result1)
print()

result2 = SingularPointandType2(x, y, sys2)
print("Sys2 =>", result2)
print()

result3 = SingularPointandType2(x, y, sys3)
print("Sys3 =>", result3)
