# Modules being called
import math as m
import numpy as np
from sympy.solvers import solve
import sympy as sp
from matplotlib import pyplot as plt
import scipy.linalg as sci
import scipy.integrate as scint



def plot_traj(ax1, g1, g2, x0, t, args=(), color='black', lw=2):
    """
    Plots a vector field plot.
    
    Parameters
    ----------
    ax : Matplotlib Axis instance
        Axis on which to make the plot
    g1 : function of the form g1(x1_)
        1/2 The right-hand-side of the dynamical system.
    g2 : function of the form g2(x1_)
        1/2 The right-hand-side of the dynamical system.
    x0 : array_like, shape (2,)
        Initial conditions of for the trajectory lines.  
    t : array_like
        Time points for trajectory.
    args : tuple, default ()
        Additional arguments to be passed to f
    color : Color of the trajectory lines.
        Set to 'black'
    linewidth: abbreviated as 'lw'. Default Value = 2
        
    Returns
    -------
    output : Matplotlib Axis instance
        Axis with streamplot included.
    """
    
    # Creates the set of points initialized by the parameter 'x'
    # for the difference equations g1 = -x1**3 - 4*x1 - x2; g2 = 3*x1
    def func(x,t):
        x_1, x_2 = x
        G1 = g1(x_1,x_2)
        G2 = g2(x_1,x_2)
        return [G1,G2]
    
    soln = scint.odeint(func, x0, t, args=args)
    ax1.plot(*soln.transpose(), color=color, lw=lw)
    return ax1 


def plot_vector_field(func1, func2, start= -3, stop= 3):
    """
    Plots a trajectory on a phase portrait.
    
    Parameters
    ----------
    func1 : function for form func1(y, t, *args)
        The right-hand-side of the dynamical system.
        Must return a 2-array.
    start : integer. Default value = 3
        The starting value. 
    stop : integer. Default value = 3
        The ending value
    color : Color of the trajectory lines.
        Set to 'black'
    linewidth: abbreviated as 'lw'. Default Value = 2
        
    Returns
    -------
    output : Matplotlib Axis instance
        Axis with streamplot included.
    """
    #----------------------------------------------------------------------------------
    # Creates the superimposed plot for stream plot of the model, as well as dPdt = 0
    #----------------------------------------------------------------------------------

    # Part 1: Creates the length of the 'X' and 'Y' Axis 
    x, y = np.linspace(start, stop), np.linspace(start, stop)
    X, Y = np.meshgrid(x, y)

    # Part 2: The approximated points of the function dx1/dt and dx2/dt which we'll use for the plot.
    U, V = func1(X, Y), func2(X, Y)

    # Part 3: Creating the figure for the plot
    fig, ax1 = plt.subplots()

    # Part 4: Sets the axis, and equilibrium information for the plot
    Title, xLabel, yLabel = input('Title?: '), input('x-axis label?: '), input('y-axis label?: ')
    ax1.set(title= Title, xlabel= xLabel, ylabel = yLabel)

    # Part 5: Plots the streamplot which represents the vector plot.
    ax1.streamplot(X, Y, U, V)
    ax1.grid()
    return ax1


### Jacobian Matrix

def poorManJacobian(func1, func2, var1, var2, points, Jac_matrix_On= True):
    """
    Plots the phase portrait of the actual dynamical system.
    
    Parameters
    ----------
    func1,func2 : sympy data type called for form sympy.core.add.Add.
        The data types of the functions we define using sympy.
        It just returns sympy.core.add.Add.
    var1, var2 : sympy data type called for form sympy.core.symbol.Symbol.
        The data types of the variables we define using sympy.
        It just returns sympy.core.symbol.Symbol.
    A_matrix_On : just a boolean check to return different things.
        If it's 'True' the it just returns the Jacobian w/o being
        evaluated at certain values of x1 and x2. 
        Default value is 'True'
        
    Returns
    -------
    output : Matplotlib Axis instance
        Axis with streamplot included.
    """
    if Jac_matrix_On:
        Jac_matrix = sp.Array([[sp.diff(func1, var1), sp.diff(func1, var2)], 
                             [sp.diff(func2, var1), sp.diff(func2, var2)]])
        return Jac_matrix
    else:
        for point in points:
            solMatrix = np.array([[float(sp.diff(func1, var1).subs({var1:point[0], var2:point[1]})), 
                            float(sp.diff(func1, var2).subs({var1:point[0], var2:point[1]}))], 
                           [float(sp.diff(func2, var1).subs({var1:point[0], var2:point[1]})), 
                            float(sp.diff(func2, var2).subs({var1:point[0], var2:point[1]}))]])
            return solMatrix


def phasePortrait(func1, func2, points, start= -3, stop= 3, 
                  jacobian_00= 4/5 , jacobian_01= -1/10, discreteON = False):
    """
    Plots the phase portrait of the actual dynamical system.
    
    Parameters
    ----------
    func1 : function for form func1(y, t, *args)
        The right-hand-side of the dynamical system.
        Must return a 2-array.
    start : integer. Default value = 3
        The starting value. 
    stop : integer. Default value = 3
        The ending value
    color : Color of the trajectory lines.
        Set to 'black'
    linewidth : abbreviated as 'lw'. Default Value = 2
    discreteON : boolean, 
        True for Phase Portrait of Discrete Systems
        False for Phase Portraits of Continuous Systems.
        Default is False.
        
    Returns
    -------
    output : Matplotlib Axis instance
        Axis with streamplot included.
    """
    if discreteON == False:
        #----------------------------------------------------------------------------------
        # Creates the superimposed plot for stream plot of the model, as well as dPdt = 0
        #----------------------------------------------------------------------------------

        # Part 1: Creates the length of the 'X' and 'Y' Axis  and the time vector
        x, y = np.linspace(start, stop), np.linspace(start, stop)
        X, Y = np.meshgrid(x, y)
        t = np.linspace(0, 100, 5000)

        # Part 2: The approximated points of the function dx1/dt and dx2/dt which we'll use for the plot.
        U, V = func1(X, Y), func2(X, Y)

        # Part 3: Creating the figure for the plot
        fig, ax1 = plt.subplots()

        # Part 4: Sets the axis, and equilibrium information for the plot
        Title, xLabel, yLabel = input('Title?: '), input('x-axis label?: '), input('y-axis label?: ')
        ax1.set(title= Title, xlabel= xLabel, ylabel = yLabel)

        # Part 5: Plots the streamplot which represents the vector plot.
        ax1.streamplot(X, Y, U, V)
        ax1.grid()

        # Part 6: Plots the trajectory lines on the stream plot
        for point in points:
            plot_traj(ax1, func1, func2, point, t)
        return ax1
    else:
        #----------------------------------------------------------------------------------
        # Creates the superimposed plot for stream plot of the model, as well as dPdt = 0
        #----------------------------------------------------------------------------------

        # Part 1: Creates the length of the 'X' and 'Y' Axis  and the time vector
        x, y = np.linspace(start, stop), np.linspace(start, stop)
        X, Y = np.meshgrid(x, y)
        t = np.linspace(0, 100, 5000)

        # Part 2: The approximated points of the function dx1/dt and dx2/dt which we'll use for the plot.
        U, V = func1(X, Y), func2(X, Y)

        # Part 3: Creating the figure for the plot
        fig, ax1 = plt.subplots()

        # Part 4: Sets the axis, and equilibrium information for the plot
        Title, xLabel, yLabel = input('Title?: '), input('x-axis label?: '), input('y-axis label?: ')
        ax1.set(title= Title, xlabel= xLabel, ylabel = yLabel)

        # Part 5: Plots the streamplot which represents the vector plot.
        ax1.streamplot(X, Y, U, V)
        ax1.grid()
        
        # Part 6:
        nextTerm = lambda L: np.array([jacobian_00*L[0]+jacobian_01*L[1],L[0]])
        param=np.linspace(0,2*np.pi,200) 
        cosX=np.cos(param)
        sinY=np.sin(param)
        a=zip(cosX,sinY) 
        for i in range(N):
            a=map(nextTerm,a)
        ax1.scatter(a)
        return ax1

def approxVectors(x1_0= -4, x2_0 = 3):
    """
    Approximates the vectors for Discrete Dynamical System Time Delay
    
    Parameters
    ----------
    x1_0, x2_0: two numbers that act as the initial value, starting point
        Default points are (-4, 3)
        
    Returns
    -------
    output : A tuple.
        
    """
    Lx, Ly = [x1_0], [x2_0]
    for i in range(10):
        x1_Last = Lx[-1]
        x2_Last = Ly[-1]
        x1_New = x1_Last + deltaX1(x1_Last,x2_Last)
        x2_New = x2_Last + deltaX2(x1_Last,x2_Last)
        Lx.append(x1_New)
        Ly.append(x2_New)
    return Lx, Ly