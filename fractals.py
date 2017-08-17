#!/usr/bin/python3

# Draw Julia sets that are based upon complex quadratic polynomials. Briefly,
# pick a complex number c. Then, to test if a point z on the complex plane is
# part of the Julia set, consider f_n(z, c), where f_0(z, c) = z^2 + c, and
# f_n(z, c) = [f_n-1(z, c)]^2 + c. If lim n->inf f_n(z, c) is not infinity,
# then z is a member of the Julia set determined by c.
# This program performs a feasible number of iterations and tests to see if the
# final value has a sufficiently small magnitude.

# Use `Decimal`s so that more significant figures can optionally be used, which
# would be necessary to draw small region in detail.
from decimal import *
getcontext().traps[FloatOperation] = True

# A point is a tuple of Decimals, where the first element is the real part of
# the number and the second element is the imaginary part of the number.

# Basic complex arithmetic necssary for these computations.
def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def multiply(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])

def absolute_value(a):
    return (a[0] * a[0] + a[1] * a[1]).sqrt()

# Compute one iteration of the point inclusion test, z^2 + c
def compute_iterate(z, c):
    return add(multiply(z, z), c)

# Determine if a given point is within the Julia set specified by a given
# complex parameter. As a heuristic, if after a specified number of iterations
# of the point inclusion test the point does not surpass a specified magnitude,
# the originally-supplied point is assumed to be in the set.
# Returns the number of iterations necessary to decide the point was not in the
# set, or -1 if the point was determined to be in the Julia set.
def is_point_contained(point, iterate_parameter, iterations, boundary):
    # Ensure that the test point can possibly even be in the set
    if absolute_value(point) > boundary:
        return 0
    iterated_point = point
    # Attempt a fixed number of iterations
    for iteration in range(iterations):
        # Run another iteration of the point inclusion test
        iterated_point = compute_iterate(iterated_point, iterate_parameter)
        # Did the point leave the circle with the specified radius?
        if absolute_value(iterated_point) > boundary:
            # Return the current iteration number
            return iteration + 1
    # Return -1 to signify point is contained
    return -1

# Take an (x, y) location of a pixel, where (0, 0) is the top left pixel of the
# eventual image, and take the width and height of the image in pixels, as well
# as the boundaries of the section of the complex plane being mapped. Return
# the complex point corresponding to the pixel location.
def map_pixel_to_point(pixel_x, pixel_y, width, height, min_x, max_x, min_y,
                       max_y):
    point_x = Decimal(str((pixel_x / width) * (max_x - min_x) + min_x))
    point_y = Decimal(str((1 - pixel_y / height) * (max_y - min_y) + min_y))
    return (point_x, point_y)

# Take the number of iterations required to escape and return an integer color
# value in [0, 255]. A value of -1 signifies the test point did not escape the
# testing boundary; ie the point is in the Julia set.
# These methods are rigidly fixed for now but shall become more flexible later.
def red(value):
    return 0

def green(value):
    return 255

def blue(value):
    if value >= 0:
        return 255
    else:
        return 0

# Save the image to a file using the simple PPM format. Takes as input a file
# name and a two dimensional array of the number of iterations required for
# each pixel to be ruled out of being in the set, or -1 if the pixel is in the
# set.
def write_ppm(filename, pixel_data):
    # Determine the image's dimensions.
    width = len(pixel_data[0])
    height = len(pixel_data)
    # Open image and write header
    image = open(filename, "w")
    image.write("P3\n{} {}\n255\n".format(width, height))
    # Write the color information for each row.
    for row in pixel_data:
        # Convert all the color information for the row into a string
        row_text = " ".join([str(red(cell)) + " " + str(green(cell)) + " " +
                             str(blue(cell)) for cell in row])
        # Write the row data
        image.write(row_text)
        image.write("\n")
    image.close()

# Generate a two dimensional array of data about whether pixels in a rectangle
# are within a Julia set or not
def draw(width, height, min_x, max_x, min_y, max_y, iterate_parameter,
         iterations, boundary):
    pixel_data = []
    # For each row
    for y in range(height):
        row = []
        # Print an update message
        print("Row {}/{}".format(y, height))
        # For each column
        for x in range(width):
            # Get the complex number corresponding to this pixel
            point = map_pixel_to_point(x, y, width, height, min_x, max_x, min_y,
                                       max_y)
            # Compute the number of iterations needed to rule a point out of
            # being in the Julia set and insert that number into the row data
            row.append(is_point_contained(point, iterate_parameter, iterations,
                                          boundary))
        # Add the row data to the overall result
        pixel_data.append(row)
    return pixel_data

# Draw a sample fractal
write_ppm("sample.ppm", draw(500, 500, -2.0, 2.0, -2.0, 2.0, [Decimal('-.8'),
                           Decimal('.156')], 50, 5))
