import numpy as np
import time
import pyrealsense2 as rs

def realsense(depth, profile, frames, align):

    aligned_f = align.process(frames)
    aligned_d = aligned_f.get_depth_frame()

    center = []
    corner = []

    with open("box_corner.txt") as f:
        corner = f.readlines()

        corner = [x.strip() for x in corner]

        print("BOX CORNERS: ", corner)
        
    with open("box_center.txt") as f:
        center = f.readlines()
            
        center = [x.strip() for x in center]
    
        
        print("BOX CENTER: ", center)
    x = float(center[0])
    y = float(center[1])

    x = int(x)
    y = int(y)

    #print( "x y: ", x, y, type(x), type(y))
    dep = depth
    print("before");
    if not dep:
        print("NO DEPTH");
        return 1
    else:
        print("YES DEPTH");
        #dist = dep.get_distance(x, y)
        dist = aligned_d.get_distance(x,y)

        #xmin, xmax, ymin, ymax
        if(dist == 0.0):
            pixel_dist = 1
            while(dist == 0.0):
                #check pixel_dist to the left
                dist = aligned_d.get_distance(x-pixel_dist, y)
                #check pixel_dist to the right
                dist = aligned_d.get_distance(x+pixel_dist, y)
                #check pixel_dist above
                dist = aligned_d.get_distance(x, y+pixel_dist)
                #check pixel_dist below
                dist = aligned_d.get_distance(x, y-pixel_dist)

                pixel_dist += 1

            print("PIXEL DISTANCE TO VALID: ", pixel_dist)
                
        print("after");
            
    print("DISTANCE: ", dist, dist*3.28);

    #time.sleep(2)

    with open("distance.txt", 'w') as g:
        g.write("%s\n" %dist)
                
        g.close()

            
    depth_intrinsic = aligned_d.profile.as_video_stream_profile().intrinsics

    real_world = rs.rs2_deproject_pixel_to_point(depth_intrinsic, [x,y], dist)
            
    print("real world", real_world)

    time.sleep(0.5)

    return 0