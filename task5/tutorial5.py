def computedSign(li):
    '''Recomputes the overall sign of a list of eigenvalues 
       args => li: A list of eigenvalues
       return => returns an integer: -1, 0, 1
    '''
    from sympy import sign, re

    sgn = sum([sign(i) if i.is_real else sign(re(i)) for i in li])
    return 1 if sgn > 1 else -1 if sgn < -1 else sgn

def SingularPointandType2(x, y, sys, const=None):
    '''Finds the singualr points of a 2nd order system and determines the stability type.
        args:
            x, y => A sympy symbol created using sympy.symbols('x, y')
            sys => A list of SymPy symbolic functions [dx, dy]. Can be created using sympy's Lambda or Function module or
                    a regular expression with sympy's Symbol module.
            const => A list or tuple of constant symbol and value, e.g [a, 1] or (a, 1)
        return: 
              A list of tuples, i.e. [(point, type), ...]
    '''
    from sympy import solve, diff, Matrix, re, Symbol, Mul, Add #,Eq

    #sde = solve((Eq(sys[0], 0), Eq(sys[1], 0)), x, y) # Solutions to the Differential Equations (SDE) or Equilibrium Points
    sde = solve(sys, x, y, dict=True)
    print("sde =>", sde)
    print()
    #dx, dy = sys

    #Jacobian = Matrix([[diff(dx, x), diff(dx, y)], [diff(dy, x), diff(dy, y)]])
    Jacobian = Matrix(sys).jacobian(Matrix([x, y]))
    print("Jacobian =>", Jacobian)

    jacobian_checks = [True for m in Jacobian if any([isinstance(m, Symbol), isinstance(m, Mul), isinstance(m, Add)])] # checks if the jacobian matrix contains symbolic expressions
    print("Eigen Values =>", Jacobian.eigenvals(multiple=True))

    if True in jacobian_checks:
        assert any([const != None, isinstance(const, list),  isinstance(const, tuple)]), "ODE contains an undefined constant!! const argument must not be None and must be a tuple or list!"
        ld = [ [val.evalf(5) for val in Jacobian.subs([ (x, ep[x]), (y, ep[y]), (const[0], const[1]) ]).eigenvals(multiple=True) ] for ep in sde]
        sde = [ [ep[val].subs(const[0], const[1]).evalf(2) for val in ep] for ep in sde ]
    else:
        ld = Jacobian.eigenvals(multiple=True) # multiple=True turns the output into a list instead of a dict
        ld = [i.evalf(5) for i in ld] # evaluate each value of the Jacobian in the most simplest form

    # Jacobian.subs([ (x, ep[x]), (y, ep[y]) ]).eigenvals(multiple=True)
    print("Ld =>", ld)

    scriteria = {-1:"stable", 0:"saddle", 1:"unstable", 2:"center"}
    if not isinstance(ld[0], list):
        csgn = computedSign(ld)
        stype = scriteria.get(csgn)+" node" if ld[1].is_real else \
                scriteria.get(2) if re(ld[1]) == 0  else \
                scriteria.get(csgn)+ " focus"
    else:
        stype = [scriteria.get(computedSign(val))+" node" if val[0].is_real else \
                scriteria.get(2) if re(val[0]) == 0  else \
                scriteria.get(computedSign(val))+ " focus" for val in ld]

    return {'sde': sde, 'lambda': ld, 'type': stype} 


if __name__ == "__main__":
    from sympy import symbols

    # This is Just an Example
    x, y = symbols('x, y')

    dx = -x - 4*y
    dy = 2*x + 5*y

    result = SingularPointandType2(x, y, [dx, dy])
    print(result)
