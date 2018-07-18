import re
content = []
with open('E:/train_demo_car.txt') as f:
    for line in f.readlines():
        line2 = re.sub(r'\n', '', line)
        line2 = re.sub(r'Region Avg IOU:', '', line2)
        line2 = re.sub(r'Class:', '', line2)
        line2 = re.sub(r'No Obj:', '', line2)
        line2 = re.sub(r'Obj:', '', line2)
        line2 = re.sub(r'Avg Recall:', '', line2)
        line2 = re.sub(r'count:', '', line2)
        line2 = re.sub(r':', ',', line2)
        line2 = re.sub(r'avg', '', line2)
        line2 = re.sub(r'rate', '', line2)
        line2 = re.sub(r'seconds', '', line2)
        line2 = re.sub(r'images', '', line2)
        if re.match('Loaded',line2)==None :
            if re.match('Resizing', line2) == None:
                if re.match('Saving', line2) == None:
                   if len(line2)>3:
                       content.append(line2)

print(content)
print(len(content))
print(int(len(content)/2))
x=''
content2=[]
for i in range(0, int(len(content)/2)):
    x=content[2*i]+','
    x=x+content[2*i+1]
    x=x+'\n'
    content2.append(x)
content2.insert(0, 'Region Avg IOU, Class, Obj, No Obj, Avg Recall, count, num, lost, avg, rate, seconds, images')
print(content2)
print(len(content2))

with open('E:/result.txt','w') as f:
    for i in range(0,len(content2)):
        f.write(content2[i])
