So I watched a Tsoding Video about projecting a 3d point onto a plane, and I'm like, whoa that's pretty cool. Credit: https://www.youtube.com/watch?v=qjWkNZ0SXfo

https://github.com/user-attachments/assets/b1bc252e-85e1-4b6c-8207-9c292ae483f5

Because I implemented this in the console, there are some technical details I had to go through. 

Drawing a line is just DDA algorithm, which is just simply uses the slope of the line to draw every pixel along the way. 

Drawing a plane uses the scanline algorithm. 

Deciding which face of the cube to draw uses something called backface culling, which uses the dot product between the normal vector of the face and the normal vector of the camera to see whether a face is visible.

P.S. Ordering the points of the plane so the cross product works out was very very painful. 


