import math
import cv2
import os
working_dir = r'C:/Users/Ros/Магистратура/NIR/dataset/'
out_dir = r'C:/Users/Ros/Магистратура/NIR/dataset/Rotate/'
f = open(working_dir+'coco_few_data_train.json')
fnew=open(out_dir+'rottrain.json', 'w')
j=0
file_id=0
fnew.write('{"images": [')
line=f.read();
while line.find('"file_name":')>-1:
        fnew.write('{"file_name": "') 
        i=line.find('"file_name":')+14
        file_name=''
        while line[i]!='"':
            file_name+=line[i]
            i+=1
        fnew.write(file_name+'", "id": '+str(file_id)+', "width": ')
        file_id+=1
        height=0
        width=0
        i=line.find('"width": ')+9
        while line[i]<='9' and line[i]>='0':
            width=width*10+ord(line[i])-ord('0')
            i+=1
        width=width
        i=line.find('"height": ')+10
        while line[i]<='9' and line[i]>='0':
            height=height*10+ord(line[i])-ord('0')
            i+=1
        height=height
        os.chdir(working_dir)
        img=cv2.imread(file_name, cv2.IMREAD_UNCHANGED)
        rotated=cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        image = cv2.flip(rotated, 0)
        os.chdir(out_dir)
        cv2.imwrite(file_name, image)
        i=line.find('}')
        fnew.write(str(height)+', "height": '+str(width))
        if line[i+1]!=']':
            fnew.write('}, ')
        line=line[i+1:]
fnew.write('}], "categories": [{')
i=line.find('"supercategory"')
j=line.find('{"segmentation"')
fnew.write(line[i:j-1])
line=line[j-1:]
s=''
sprev=''
flag=0
i=0
while i<len(line):
    sym=line[i]
    if flag>0 and sym>='0' and sym<='9':
        if flag==4:
            fnew.write(', ')
            flag-=1
        if flag==3:
            sprev+=sym
        if flag==1:
            s+=sym
            if line[i+1]<'0' or line[i+1]>'9':
                fnew.write(s+', '+sprev)
                s=''
                sprev=''
                flag=6
    elif flag>0 and (sym==',' or sym==' '):
        flag-=1
    else:
        if sym=='[':
            flag=3
        if sym==']':
            flag=0
            s=''
            sprev=''
        fnew.write(sym)
    i+=1
f.close()
fnew.close()


