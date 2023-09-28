#version 430

layout (local_size_x = 16, local_size_y = 16) in;

uniform int max_iterations;
uniform float width;
uniform float height;
uniform image2D outputImage; // Output image to store the result

void main() {
    ivec2 pixelCoord = ivec2(gl_GlobalInvocationID.xy);
    vec2 c = vec2(pixelCoord.x / width * 3.5 - 2.5, pixelCoord.y / height * 2 - 1);

    vec2 z = vec2(0.0, 0.0);
    int iterations = 0;

    // Mandelbrot set calculation
    while (iterations < max_iterations && dot(z, z) < 4.0) {
        vec2 temp = z;
        z = vec2(temp.x * temp.x - temp.y * temp.y, 2.0 * temp.x * temp.y) + c;
        iterations++;
    }

    // Determine whether the pixel is inside the Mandelbrot set
    bool isInMandelbrotSet = iterations == max_iterations;

    // Color for pixels inside the set
    vec4 insideSetColor = vec4(0.0, 0.0, 0.0, 1.0);

    // Color for pixels outside the set (contour tracing)
    vec4 outsideSetColor = vec4(1.0, 1.0, 1.0, 1.0);

    // Fill the Mandelbrot set and trace the boundaries
    vec4 finalColor = isInMandelbrotSet ? insideSetColor : outsideSetColor;

    // Write the final color to the output image
    imageStore(outputImage, pixelCoord, finalColor);
}
