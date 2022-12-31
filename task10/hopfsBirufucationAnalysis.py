def analysis(sys1, sys2=None, init_cond=None, prettyprint=False):
    """ Carries out Linear Analysis of Hopfs Birufications
        sys1: A list of Polar Coordinate based system, symbolic variable, tuple of symbolic consts
        sys2: A list of Catersian Coordinate based system odes
        init_cond: A list or tuple of initial conditions x0, y0 for the sys2
    """

    sys_p, r, *consts = sys1

    ConstMoreThanOne = True if len(consts) > 1 else False

    if prettyprint:
        from sympy import init_printing
        init_printing()
    
    from sympy import solve, N
    sde = solve(sys_p, r, check=False)

    if ConstMoreThanOne:
        sde_solv = solve(sde, const)
        sde_subed = enumerate([sol.subs(key, val) for sol in sde for key, val in sde_solv.items()])
    else:
        sde_subed = [(index,subed) for index,subed in enumerate([point.subs(consts[0], 0) for point in sde if point != 0]) if N(subed) >= 0]
    
    criticalpoints = [[sol[1]] if sol[1] == 0 else solve(sde[sol[0]], consts) for sol in sde_subed] # returns a list of lists

    # generate random values greater and lesser than the critical points with contraints -5 5
    import random
    analysisPoints = [(random.uniform(-1.0, point), random.uniform(point, 2.0)) for li in criticalpoints for point in li if point]

    print(f"ODE Sol: {sde_subed}\nCritical points: {criticalpoints}\nAnalysis points: {analysisPoints}\n")

    for pair in analysisPoints:
        for p in pair:
            print(f"Using the point: {p} ....\n")
            if ConstMoreThanOne:
                vals = [p]
                vals.append(val.subs(const for const in consts if const!=key) for key, val in sde_solv.items())
                sys_subed = [ode.subs(consts, vals).evalf(5) for ode in sys2]
            else:
                sys_subed = [ode.subs(consts[0], p).evalf(5) for ode in sys2]
            
            drawPhasePortrait(sys_subed, init_cond, p)
        

def drawPhasePortrait(sys, init_cond=None, save_key=None):
    '''Draws the phase portrait of a systemn using numpy and matplotlib modules.

            sys: A python function that returns numpy arrays of the system dynamics. Or a lamdified sympy function.
            init_cond: must be a tuple or list of init. conditions for sys. 
        return:
            Nothing
    '''
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(10,8))
    axis = fig.add_subplot(1,1,1)

    from sympy.abc import x, y

    # convert symbolic system of ode's into a lamdified function for numpy operations
    from sympy import lambdify
    fcn = lambdify((x, y), sys, "numpy")

    # define a mesh grid for the quiver plot
    import numpy as np
    xpos, ypos = np.meshgrid(np.linspace(-1.5, 1.5, 20), np.linspace(-1.5, 1.5, 20))
    xdir, ydir = fcn(xpos, ypos)

    n = -2
    color_array = np.sqrt(((ydir-n)/2)**2 + ((xdir-n)/2)**2)
    axis.quiver(xpos, ypos, xdir, ydir, color_array)

    def sym2scifunc(xy0, t):
        ''' needed for scipy's odeint function '''
        return np.array(fcn(xy0[0], xy0[1]))

    from scipy.integrate import odeint
    
    if init_cond is not None:
        t = np.linspace(-5, 5, 1000)
        x0, y0 = init_cond
        sol = odeint(sym2scifunc, [x0, y0], t)
        axis.plot(sol[:, 0], sol[:, 1], 'b')
    
    axis.grid()
    axis.set_aspect('equal')
    axis.set_title(f'Phase portrait of system\na = {save_key}; init. cond. = {init_cond}')
    #plt.savefig(f'constval_{save_key}.png')
    plt.show()
    

if __name__ == "__main__":
    from sympy.abc import a, r, x, y, pi

    # sys_polar = a*r-r+r*2*r**2-r**4*r # r -> variable; a -> constant
    # sys_cartesian = [x*(a-1+((x**2+y**2)*2-(x**2+y**2)**2)) - 2*pi*y, y*(a-1+((x**2+y**2)*2-(x**2+y**2)**2)) + 2*pi*x] # task 10

    # analysis([sys_polar, r, a], sys_cartesian, [0, 0.9])

    sys = [a*x + x**3, -y]
    sys = [ode.subs(a, -1).evalf(5) for ode in sys]
    drawPhasePortrait(sys, [0.5, 0])