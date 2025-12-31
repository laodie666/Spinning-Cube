import os
import sys
import time
import math


os.system("")

h = 70  
w = 70

def draw(screen): 
    # start from topleft
    # frame = "\033[H"
    
    # This works better, some solution from stack overflow
    print(chr(27) + "[2J")
    frame = ""
    
    for y in range(h):
        line = ""
        for x in range(w):
            if (x, y) in screen:
                line += screen[(x,y)] * 2
            else:
                line += "  "
        
        frame += line + "\n"
        
    # print faster hopefully
    sys.stdout.write(frame)
    sys.stdout.flush()

def middle_to_topleft_coor(point):
    # -1 to 1 convered to 0 to w or h 
    x = (point[0] + 1) / 2 * w
    y = (point[1] + 1) / 2 * h
    return (x,y)

# Coordinate is (x, y, z)
def project(coordiante):
    return (coordiante[0]/coordiante[2], coordiante[1]/coordiante[2])

def shift_z(coordinate, dz):
    return (coordinate[0], coordinate[1], coordinate[2] + dz)

def round_point(point):
    return (round(point[0]), round(point[1]))

def rotate_x(coordainte, angle):
    cos = math.cos(angle)
    sin = math.sin(angle)
    x = coordainte[0]
    y = coordainte[1]
    z = coordainte[2]
    
    yp = y * cos - z * sin
    zp = y * sin + z * cos
    
    return (x, yp, zp)

def rotate_y(coordainte, angle):
    cos = math.cos(angle)
    sin = math.sin(angle)
    x = coordainte[0]
    y = coordainte[1]
    z = coordainte[2]
    
    xp = x * cos + z * sin
    zp =  -x * sin + z * cos
    
    return (xp, y, zp)

def rotate_z(coordainte, angle):
    cos = math.cos(angle)
    sin = math.sin(angle)
    x = coordainte[0]
    y = coordainte[1]
    z = coordainte[2]
    
    xp = x * cos - y * sin
    yp =  x * sin + y * cos
    
    return (xp, yp, z)

def check_inbound (point):
    return 0<=point[0]<w and  0<=point[1]<h
         
# DDA line drawing algorithm
def draw_line(screen, p1, p2, symbol):
    # From point 1 to point 2, calculate slope and go along the line until point 2 is reached.
    p1 = round_point(p1)
    p2 = round_point(p2)
    point = list(p1)
    
    dy = p2[1]-p1[1]
    dx = p2[0]-p1[0]
    step = max(abs(dy), abs(dx))
    for i in range(step):
        if not check_inbound(point):
            break
        screen[round_point(point)] = symbol
        point[0] += dx/step
        point[1] += dy/step
        
def three_dimension_to_drawable(coordinate):
    return round_point(middle_to_topleft_coor(project(coordinate)))

# Scanline algorithm
def draw_polygon(screen, points, symbol):
    slopes = []
    
    for i in range(len(points)):
        point = points[i]
        next_point = points[(i+1)%len(points)]
        if point[0]-next_point[0] != 0:
            slopes.append((point[1]-next_point[1])/(point[0]-next_point[0]))
        else:
            slopes.append(float('inf'))    
            
    for x in range(w):
        # For every edge, check whether that edge intersect with the scanline at x
        intersect_ps = []
        for i in range(len(points)):
            point = points[i]
            next_point = points[(i+1)%len(points)]
            
            if point[0] < next_point[0]:
                left_point = point
                right_point = next_point
            else:
                left_point = next_point
                right_point = point
            
            if x == left_point[0] and left_point[0] == right_point[0]:
                draw_line(screen, point, next_point, symbol)
                continue
            
            if left_point[0] <= x < right_point[0]:
                intersect_ps.append((x, left_point[1] + (x-left_point[0]) * slopes[i]))
        
        intersect_ps.sort(key=lambda p: p[1])
        for i in range(0, len(intersect_ps), 2):
            if i + 1 < len(intersect_ps):
                draw_line(screen, intersect_ps[i], intersect_ps[i+1], symbol)
            
def threed_to_draw_list(coordinates):
    points = []
    for coor in coordinates:
        points.append(three_dimension_to_drawable(coor))
    return points

def subtract_points(p1, p2):
    return (p1[0]-p2[0], p1[1]-p2[1], p1[2]-p2[2])

def cross_product(v1, v2):
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    x = y1*z2 - z1*y2
    y = z1*x2 - x1*z2
    z = x1*y2 - y1*x2
    
    return (x,y,z)

def dot_product(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

# Back face culling, 
# given two vectors of the face, determine whether it is visible to the normal vector of camera

# NOTE Figuring out how the faces should be ordered to put into this face_visible function was the 
# most EXCRUCIATING part of this entire program
def face_visible(face):
    
    p0 = face[0]
    p1 = face[1]
    p2 = face[2]
    
    v1 = subtract_points(p1, p0)
    v2 = subtract_points(p2, p0)
    
    camera_normal = p0
    
    face_normal = cross_product(v1, v2)
    if dot_product(camera_normal, face_normal) < 0:
        return True
    return False

if __name__=="__main__":
    

    # Plane
    # coordinates = [
    #     (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5)]
    # screen = {}
    
    # Rotating cube
    coordinates = [
        # Back
        (-0.5, -0.5, -0.5), 
        (0.5, -0.5, -0.5), 
        (0.5, 0.5, -0.5), 
        (-0.5, 0.5, -0.5),
        
        # Front
        (-0.5, -0.5, 0.5), 
        (0.5, -0.5, 0.5), 
        (0.5, 0.5, 0.5), 
        (-0.5, 0.5, 0.5)]
    
    faces = [
        ([3, 2, 1, 0], '#'),
        ([4, 5, 6, 7], '@'),
        ([0, 4, 7, 3], '%'),
        ([1, 2, 6, 5], '+'),
        ([3, 7, 6, 2], '='),
        ([0, 1, 5, 4], '$')
    ]
    
    coor_count = len(coordinates)
    for i in range(0, 760):
        # print(i)
        
        screen = {}
        
        adjusted_coordinate = []
        for coordinate in coordinates:
            coordinate = rotate_x(coordinate, math.radians(i))
            coordinate = rotate_z(coordinate, math.radians(2*i))
            coordinate = rotate_y(coordinate, math.radians(i/2))
            coordinate = shift_z(coordinate, 1.5)
            adjusted_coordinate.append(coordinate)
            

        # print(adjusted_coordinate)
        points = threed_to_draw_list(adjusted_coordinate)
        
        # Lines drawing
        # for i in range(4):
        #     draw_line(screen, three_dimension_to_drawable(adjusted_coordinate[i]), three_dimension_to_drawable(adjusted_coordinate[(i+1)%4]), "@")
         
        # for i in range(4, coor_count):
        #     if i == 7:
        #         draw_line(screen, three_dimension_to_drawable(adjusted_coordinate[i]), three_dimension_to_drawable(adjusted_coordinate[4]), "@")
        #     else:
        #         draw_line(screen, three_dimension_to_drawable(adjusted_coordinate[i]), three_dimension_to_drawable(adjusted_coordinate[i+1]), "@")
            
        # for i in range(4):  
        #     draw_line(screen, three_dimension_to_drawable(adjusted_coordinate[i]), three_dimension_to_drawable(adjusted_coordinate[i+4]), "@")
   
        for face in faces:
            if face_visible([adjusted_coordinate[i] for i in face[0]]):
                draw_polygon(screen, [points[i] for i in face[0]], face[1])
   
        draw(screen)
        time.sleep(0.01)
            
