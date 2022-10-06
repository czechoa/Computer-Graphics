These are my programs for computer graphics in my third year of college.

The first one is, a 3 d camera moving between solids. 

Phong's algorithm.
==================

The second program is Phong's algorithm.

Sample views 
===================

![image](data/dobrze_odbija.png)

Projection and display
=========================

- I used simple orthogonal projection.

- I determine the Z coordinate from the solution of the equation
    of the square of the sphere
    $((x-x_{0})^2 + (y-y_{0})^2 + (z-z_{0})^2 = r^2)$
- $((x − x0)^2 + (y − y0)2 + (z − z0)2 = r2)$
- The background is not refreshed.

For each pixel that displays a sphere, it solves the equations
phong:$$I=k_{a} \¢dot I_{a}+I_{i} \$$I = k_{d}({{vec {N}})+k_{s}}({{vec {R}}} \{{vec {V}^{n}})$$.

- $k_{a} \I_{a}$ - ambient intensity.

- $k_{d}$ - scattering coefficient

- $k_{s}$ - reflection coefficient

- $vec{N}$ - normal vector

- $vec{L}$ - vector of point a of the source

- $vec{V}$ - vector of point a of the observer

Program activities
==================

- For each pixel, coordinate calculations Z of the sphere.

- Only for each point from the sphere, calculation of light intensity (from the
    phong formula).

- Display each pixel from the sphere, multiplied by its
    phonga illumination.

Testowanie
==========

![image](data/bardzo_dobrze_odbija.png)

![image](data/dobrze_odbija.png)

![image](data/słabo_odbija.png)

![image](data/bardzo_slabo_odbija.png)


Both programs written in Python, using numpy vectoring for optimization.
