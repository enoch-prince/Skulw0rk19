from sympy import Symbol, sin, cos, plot
from tutorial1 import SingularPointAndType


x = Symbol('x')
f1 = 2*x**6 - x**4 - 5*x**2 - 2
f2 = (x**2 - 3*x + 1)**2 + 3*(x-1)*(x**2 - 3*x + 1) - 4*(x-1)**2
f3 = (x-1)**4 + (x-3)**4 - 82
y = Symbol('y')
f4 = sin(y) + cos(y)
z = Symbol('z')
f5 = sin(z) + sin(z)**2 + cos(z)**3

Plotting the Functions
plot(f1, (x, -5,5), show=False, line_color="r", title="f(x) = 2x^6-x^4-5x^2-2").save("f1_2.png")
plot(f2, (x, -5,5), show=False, line_color="g", title="f(x) = (x^2-3x+1)^2+3(x-1)(x^2-3x+1)-4(x-1)^2").save("f2.png")
plot(f3, (x, -5,5), show=False, line_color="r", title="f(x) = (x-1)^4+(x-3)^4-82").save("f3.png")
plot(f4, (y, -5,5), show=False, line_color="m", title="f(x) = sin(x)+cos(x)").save("f4.png")
plot(f5, (z, -5,5), show=False, title="f(x) = sin(x)+sin^2(x)+cos^3(x)").save("f5.png")

result1 = SingularPointAndType(f1, x)
print(result1)
print()

result2 = SingularPointAndType(f2, x)
print("f2 =>",result2)
print()

result3 = SingularPointAndType(f3, x)
print("f3 =>", result3)
print()

result4 = SingularPointAndType(f4, y)
print("f4 =>", result4)
print()

result5 = SingularPointAndType(f5, z)
print("f5 =>", result5)
