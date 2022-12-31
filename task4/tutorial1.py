def SingularPointAndType(f, x):
    ''' Finds the singualr points of a 1st order function and determines their stability type 
        args: f => A symbolic function. Can be created using sympy's Lambda or Function module or
                    a regular expression with sympy's Symbol module.
              x => A sympy symbol created using sympy.Symbol('x')
        return: A list of tuples, i.e. [(point, type), ...]
    '''
    from sympy.solvers import solve
    #solve(exp, sym) finds the root of the expression targetting the symbol 
    from sympy.core import evalf
    # evalf(n=15) converts the results into equivalent floating point numbers; n determines the precision of the floating point number
    roots = solve(f, x, check=False)
    if f.is_algebraic_expr():
        roots = [root.evalf(5) for root in roots if root.is_real]
    else:
        roots = [root.evalf(5) for root in roots if root.is_real and root >= 0]
    print("Roots =>", roots)
    print()

    import random
    n = len(roots)
    y = [random.uniform(-1.0e6, roots[i]) if i==0 else \
        random.uniform(roots[n-1], 1.0e6) if i==n else \
        random.uniform(roots[i-1], roots[i]) for i in range(n+1)]
    #print(y)

    solution = [f.subs(x, i).evalf(5) for i in y]
    print("solution =>", solution)
    print()

    from sympy.functions import sign, re
    from sympy.core import I

    signs = [1 if sign(sol)==I else -1 if sign(sol)== -I else sign(re(sol)) for sol in solution]
    # print("signs =>", signs)
    # print()
    stype = ["critically stable" if signs[i]==signs[i+1] and signs[i]==0 else \
             "unstable" if signs[i] <= signs[i+1] else "stable" for i in range(n)]
    # print(solution, sign, stype)

    return list(zip(roots, stype))


if __name__ == "__main__":
    from sympy import Symbol, tan

    x = Symbol('x')
    # f = x**2-5

    #f = tan(x) + tan(2*x) - tan(3*x)
    f = tan(4*x) + tan(2*x) + tan(x)
    

    results = SingularPointAndType(f, x)
    print(results)