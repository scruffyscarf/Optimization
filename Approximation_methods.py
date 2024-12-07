a = float(input())
b = float(input())
e = float(input())

def bisection_method(a, b, e):
    # Define the function whose root we are finding
    def f(x):
        return x**3 - 6*x**2 + 11*x - 6

    # Loop until the absolute value of the function at the midpoint is less than the precision
    while abs(f((a + b) / 2)) > e:
        c = (a + b) / 2  # Compute the midpoint
        if f(c) >= 0:    # If the function value at c is non-negative, shift the right boundary
            b = c
        else:            # Otherwise, shift the left boundary
            a = c
    return (a + b) / 2  # Return the midpoint as the approximate root

root = bisection_method(a, b, e)

print("Approximate root of the function:", root)



a = float(input())
b = float(input())
e = float(input())

def golden_section_method(a, b, e):
    # Define the function whose minimum we are finding
    def f(x):
        return (x - 2)**2 + 3

    # Loop until the interval length is less than the precision
    while abs(a - b) > e:
        # Compute points using the golden section ratio
        x1 = b - (((5)**(0.5) - 1) / 2) * (b - a)
        x2 = a + (((5)**(0.5) - 1) / 2) * (b - a)
        if f(x1) > f(x2):  # If value of the function at x1 more than value of the function at x2, cut the left part of the interval
            a = x1
        elif f(x1) < f(x2):  # If value of the function at x1 less than value of the function at x2, cut the right part of the interval
            b = x2
        else:  # If f(x1) == f(x2), cut the interval from two sides
            a = x1
            b = x2
    return (a + b) / 2, f((a + b) / 2)  # Return the midpoint and the function value at the midpoint

x_min, f_x_min = golden_section_method(a, b, e)

print("Approximate minimum:", x_min)
print("Function value at minimum:", f_x_min)



x0 = float(input())
alpha = float(input())
N = int(input())

# Define the target function
def f(x):
    return -x**2 + 4*x + 1

def grad_f(x):
    return -2*x + 4  # Gradient of the function

# Function implementing the Gradient Ascent Method
def gradient_ascent_method(f, grad_f, x0, alpha, N):
    x = x0  # Initialize the starting point
    
    # Perform N iterations
    for i in range(N):
        grad = grad_f(x)  # Compute the gradient at the current point
        x += alpha * grad  # Update x using the gradient and step size alpha

    return x  # Return the point approximating the maximum

maximum = gradient_ascent_method(f, grad_f, x0, alpha, N)

print("Approximate maximum:", maximum)
print("Function value at maximum:", f(maximum))
