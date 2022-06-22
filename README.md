
FractalGen

Version: 1.0
Author: Nicolás Rodrigo Pérez
Date: 14/10/2021

A fractal generator written in python using tkinter and PIL (Python Imaging Library),
able to display recursive, complex number derived, and ifs (iterated function sistems)
fractals.

To execute:
- In windows you just double click the .pyw file.
- Execute FractalGen.py on your favourite IDE.
- Place the link in your desktop and double click it (may only work for windows).

To use:
- Recursive:
  - n is the recursion depth.
- Complex:
  - Mandelbrot:
    - Displays random coloured mandelbrot of 256 iterations in under 10 secs!!!(i7-8550u).
  - Julia Set:
    - Displays random Julia Set unless user specifies new complex number above.
- IFS:
  - Click on the IFS's names in the box to display them. Select the complexity of the
    image in the iters param. The functions that compose the image are in diferent colours,
    for the user to identify them.
  - Add a new ifs code by typing the values of the diferent parameters of its functions,
    adding these functions one by one with the add button. When you have all the functions that compose
    the image inserted, hit Draw to display your own IFS. If you like it, save it's IFS code
    with the Save button.
