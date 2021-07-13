'''

Copyright 2021, Aninda Zaman, All rights reserved.

'''


import cv2
import numpy as np
import time


def yolo(capture, tfnet):
    
    colors = [tuple(255 * np.random.rand(3)) for _ in range(10)]   

    while True:
        flag = 0
        stime = time.time()
        ret, frame = capture.read()
        if ret:
            results = tfnet.return_predict(frame)
            for color, result in zip(colors, results):
                tl = (result['topleft']['x'], result['topleft']['y'])
                br = (result['bottomright']['x'], result['bottomright']['y'])
                label = result['label']
                confidence = result['confidence']
                text = '{}: {:.0f}%'.format(label, confidence * 100)
                if (label == 'apple'):      #change label to target object
                    flag = 1
                    #capture.stop()
                    center = []
                    center.append((tl[0] + br[0])/2)
                    center.append((tl[1] + br[1])/2)

                    corner = []
                    #xmin, xmax, ymin, ymax
                    corner.append(tl[0])
                    corner.append(br[0])
                    corner.append(br[1])
                    corner.append(tl[1])

                    with open("box_corner.txt", 'w') as coord:
                        for item in corner:
                            coord.write("%s\n" %item)
                        coord.close()

                    with open("box_center.txt", 'w') as num_file:
                        for item in center:
                            num_file.write("%s\n" %item)

                        num_file.close()
                    
                    
                    print(label, ' Top Left: ', tl, 'Bottom Right: ', br, 'Center: ', center)
                frame = cv2.rectangle(frame, tl, br, color, 5)
                frame = cv2.putText(
                    frame, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
            cv2.imshow('YOLO', frame)
            #print('FPS {:.1f}'.format(1 / (time.time() - stime)))
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            #break
            capture.release()
            cv2.destroyAllWindows()
            return 2
        if flag == 1:
            return 1

    capture.release()
    cv2.destroyAllWindows()
    
    
'''

Copyright 2021, Aninda Zaman, All rights reserved.

'''
