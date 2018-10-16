import cv2

vc = cv2.VideoCapture('/media/root/tmp/2018-09-20_11_50_54.mp4')
c=1
a=0
if vc.isOpened():
    rval,frame=vc.read()
else:
    rval = False

timeF = 3

# munster   _000032_000019_leftImg8bit.png
# lindau   _000000_000019_leftImg8bit.png
while rval:
    rval,frame = vc.read()
    if(c%timeF == 0):
        strzyx = 'outpic/'+'munster_'+ '%06d' % a +'_000019_leftImg8bit.png'
        frame = cv2.resize(frame,(960,480))
        cv2.imwrite(str(strzyx),frame)
        a = a + 1
    c = c+1
    # print('1536822933796196.mp4.pic/'+'3_'+str(a) +'.png')
    print(a)
    if 174==a:
        exit(0)
        pass
    cv2.waitKey(1)
vc.release()
