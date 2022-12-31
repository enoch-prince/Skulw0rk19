
def drawPhasePortrait(sys, sys_const=None, equilibria=None, save_key=None):
    '''Draws the phase portrait of a systemn using numpy and matplotlib modules.

            sys: A python function that returns numpy arrays of the system dynamics. Or a lamdified sympy function.
            sys_const: must be a tuple or list of init. conditions for sys. 
            equilibria: Equilibrium points of the system. 
                        Its's a list of dictionaries, e.g [{x: 1, y: 0}, ...] or
                        A list of lists, e.g [[1, 0], ...]
        return:
            Nothing
    '''
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(10,8))
    axis = fig.add_subplot(1,1,1)

    from sympy.abc import x, y
    # plot equilibrium points
    if equilibria is not None:
        if not isinstance(equilibria, list):
            equilibria = [equilibria]
        
        if isinstance(equilibria[0], dict):
            all_x = [point[x] for point in equilibria for val in point if val == x]
            all_y = [point[y] for point in equilibria for val in point if val == y]
        else:
            print(equilibria)
            all_x = [point[0] for point in equilibria]
            all_y = [point[1] for point in equilibria]
        
        axis.plot(all_x, all_y, 'ro', markersize = 5.0, label='equilibrium points')

    # convert symbolic system of ode's into a lamdified function for numpy operations
    from sympy import lambdify
    fcn = lambdify((x, y), sys, "numpy")

    # define a mesh grid for the quiver plot
    import numpy as np
    xpos, ypos = np.meshgrid(np.linspace(-2, 2, 20), np.linspace(-2, 2, 20))
    xdir, ydir = fcn(xpos, ypos)

    # growth_rate = (np.hypot(xdir, ydir))
    # growth_rate[ growth_rate == 0 ] = 1 # avoid zero division errors
    # xdir /= growth_rate                 # normalize each arrow
    # ydir /= growth_rate
    # axis.quiver(xpos, ypos, xdir, ydir, growth_rate, pivot='mid')

    n = -2
    color_array = np.sqrt(((ydir-n)/2)**2 + ((xdir-n)/2)**2)
    axis.quiver(xpos, ypos, xdir, ydir, color_array)

    def sym2scifunc(xy0, t):
        ''' needed for scipy's odeint function '''
        return np.array(fcn(xy0[0], xy0[1]))

    from scipy.integrate import odeint
    # if equilibria is not None:
    #     t = np.linspace(-5, 5, 1000)
    #     for x0, y0 in zip(all_x, all_y):
    #         sol = odeint(sym2scifunc, [x0, y0], t)
    #         axis.plot(sol[:, 0], sol[:, 1], 'k')
    #         # axis.plot(t, sol[:, 0], 'b', t, sol[:, 1], 'k')
    
    if sys_const is not None:
        t = np.linspace(-10, 10, 1000)
        sol = odeint(sym2scifunc, sys_const, t)
        axis.plot(sol[:, 0], sol[:, 1], 'b', label='system plot')
    

    # axis.xaxis.set_ticks([])
    # axis.yaxis.set_ticks([])
    axis.grid()
    axis.set_aspect('equal')
    axis.set_title('Phase portrait of system')
    axis.legend(loc='best')
    axis.set_title(f'Phase portrait of system\na = {save_key}; init. cond. = {sys_const}')
    plt.show()
    return

if __name__ == "__main__":
    print("Run this file outside the it's folder with the command: \n\t" \
        "python -m <folder-where-file-is>.task6.task6 \n\n")
    from sympy.abc import x, y, a, pi
    from StabilityLinearAnalysis.task5.tutorial5 import SingularPointandType2

    # sys = [x**2-y**2-5, x**2+y**2-13] # main task - task 6
    #sys = [x**2+y**2-17, x*y+4] # example from tutorial -task 6
    #sys = [-2*x-4*y, 4*x-4*y] # task 6

    #sys = [a*x + x**3, -y] # task 9. Ex.1
    sys = [-a*x*(y+1)-x**3+x, y] # task 9 Ex.2
    #sys = [x*(a-1+((x**2+y**2)*2-(x**2+y**2)**2)) - 2*pi*y, y*(a-1+((x**2+y**2)*2-(x**2+y**2)**2)) + 2*pi*x] # Task 10
    #sys = [ode.subs(a, 1).evalf(5) for ode in sys]

    result = SingularPointandType2(x, y, sys, [a, 0.5])
    print(result)

    sys = [ode.subs(a, 0.5).evalf(4) for ode in sys]
    drawPhasePortrait(sys, sys_const=[0,0], equilibria=result['sde'], save_key=0.5)
