# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 23:01:59 2021

@author: HUANGYANGLAI
"""

import struct
import cv2
import numpy as np
if __name__=="__main__":
    img=cv2.imread("11.jpg")
    print(img.shape)
    img_encode=cv2.imencode('.jpeg',img)[1]
    print(img_encode.shape)
    data_encode=np.array(img_encode)
    print(data_encode)
    str_encode=data_encode.tostring()
    print(str_encode)
    
    #nparr=np.fromstring(str_encode,np.uint8)
    #img_decode=cv2.imdecode(nparr,cv2.IMREAD_COLOR)
    #cv2.imshow("img_decode",img_decode)
    #cv2.waitKey()
