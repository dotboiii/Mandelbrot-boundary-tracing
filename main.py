####################################################################################################################
# Description: This program traces the boundary of the Mandelbrot set using a stack.
# The stack is initialized with a starting point, and then neighboring pixels are added to the stack.
# The process is repeated until the stack is empty.
# The program also visualizes the tracing process by drawing a point on an image for each pixel that is visited.
# The image is saved as a file called "tracing_process.png".
# Not very fast but this will be a template for the next program which will use OpenGL compute shaders.
####################################################################################################################

# Written by co-authors Max Madden and Kyle Simmons 2023
# MIT License https://opensource.org/licenses/MIT

from PIL import Image, ImageDraw
import numpy as np
import time

# Constants
width = 1920
height = 1080
max_iterations = 200
escape_threshold = 2

def compute_color(x, y, max_iterations, escape_threshold):
    # Initialize complex number
    c = complex(x, y)
    z = 0
    
    for i in range(max_iterations):
        z = z * z + c
        
        if abs(z) >= escape_threshold:
            # Return the number of iterations before escaping
            return i
    
    # Point is inside the set, return the maximum iterations

    return max_iterations

def trace_boundary(start_x, start_y, max_iterations, escape_threshold):
    # Create an image to visualize the tracing process
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    
    # Create an array to keep track of visited pixels
    visited = np.zeros((width, height), dtype=bool)
    
    # Initialize the stack with the starting point
    stack = [(start_x, start_y)]
    
    # Start the timer
    start_time = time.time()
    
    while stack:
        # Pop the current pixel from the stack
        current_x, current_y = stack.pop()
        
        # Check if the pixel has already been visited
        if visited[current_x, current_y]:
            continue
        
        # Mark the pixel as visited
        visited[current_x, current_y] = True
        
        # Check color of current pixel (number of iterations)
        iterations = compute_color(current_x / width * 3.5 - 2.5, current_y / height * 2 - 1, max_iterations, escape_threshold)
        color = (iterations * 255 // max_iterations,) * 3  # Grayscale color
        
        # Draw a point on the image to represent the current pixel
        draw.point((current_x, current_y), fill=color)
        
        # Add neighboring pixels to the stack
        neighbors = [(current_x + 1, current_y), (current_x - 1, current_y), (current_x, current_y + 1), (current_x, current_y - 1)]
        for neighbor_x, neighbor_y in neighbors:
            if 0 <= neighbor_x < width and 0 <= neighbor_y < height and not visited[neighbor_x, neighbor_y]:
                stack.append((neighbor_x, neighbor_y))
    
    # Stop the timer
    end_time = time.time()
    
    # Calculate the elapsed time in milliseconds
    elapsed_time_ms = (end_time - start_time) * 1000
    
    print(f"Tracing completed in {elapsed_time_ms:.2f} ms")
    
    # Save the image as a file
    image.save("tracing_process.png")

def main():
    # Choose a starting point closer to the boundary
    trace_boundary(320, 240, max_iterations, escape_threshold)

if __name__ == "__main__":
    main()
