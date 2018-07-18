#!/usr/bin/env python
# encoding:utf-8

import os,sys,time
import shutil
import xml.etree.ElementTree as ET
import pickle
import string

from os import listdir, getcwd
from os.path import join

classes = ["demo car"] 
def rename_by_count(path): #按序号命名
    count = 1000;
    filelist = os.listdir(path)  # 该文件夹下所有的文件（包括文件夹）
    for files in filelist:  # 遍历所有文件
        Olddir = os.path.join(path, files);  # 原来的文件路径
        if os.path.isdir(Olddir):  # 如果是文件夹则跳过
            continue;
        filename = os.path.splitext(files)[0];  # 文件名
        filetype = os.path.splitext(files)[1];  # 文件扩展名
        Newdir = os.path.join(path, str(count) + filetype);  # 新的文件路径
        os.rename(Olddir, Newdir);  # 重命名
        count += 1;


def listname(path,idtxtpath):
    filelist = os.listdir(path);  # 该文件夹下所有的文件（包括文件夹）
    f = open(idtxtpath, 'w');
    for files in filelist:  # 遍历所有文件
        Olddir = os.path.join(path, files);  # 原来的文件路径
        if os.path.isdir(Olddir):  # 如果是文件夹则跳过
            continue;
        filename = os.path.splitext(files)[0];  # 文件名
        filetype = os.path.splitext(files)[1];  # 文件扩展名
        #Newdir = os.path.join(path, "1000" + filetype);  # 新的文件路径: path+filename+type
        f.write(filename);
        f.write('\n');
    f.close();

def process_data(img_path, savepath, valid_num):
    #Create new folders.
    valid_path = savepath + "/validateImage"
    train_path = savepath + "/trainImage"

    if os.path.exists(valid_path) == False:
        os.mkdir(valid_path)
    if os.path.exists(train_path) == False:
        os.mkdir(train_path)

    xml_valid = savepath + "/validateImageXML"
    xml_train = savepath + "/trainImageXML"

    if os.path.exists(xml_valid)== False:
        os.mkdir(xml_valid)
    if os.path.exists(xml_train) == False:
        os.mkdir(xml_train)

    img_file_list = os.listdir(img_path)
    count = 0

    for f_item in img_file_list:
        olddir = os.path.join(img_path, f_item)
        newdir1 = os.path.join(valid_path, f_item)
        newdir2 = os.path.join(train_path, f_item)
        filename = os.path.splitext(f_item)[0]
        xml_folder = savepath + "/xml"
        xml_valid = savepath + "/validateImageXML"
        xml_train = savepath + "/trainImageXML"

        if count<valid_num:
            shutil.copy(olddir, newdir1) #validate

            xmlolddir = os.path.join(xml_folder, filename + ".xml")
            xmlnewdir = os.path.join(xml_valid,filename+".xml")
            shutil.copy(xmlolddir,xmlnewdir)
        else:
            shutil.copy(olddir, newdir2)
            
            xmlolddir = os.path.join(xml_folder, filename + ".xml")
            xmlnewdir = os.path.join(xml_train, filename + ".xml")
            shutil.copy(xmlolddir, xmlnewdir)

        count=count+1;
    imgidtxtpath1 = savepath + "/validateImageId.txt";
    imgidtxtpath2 = savepath + "/trainImageId.txt";
    listname(valid_path, imgidtxtpath1);
    listname(train_path, imgidtxtpath2);


def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_id,flag,savepath):
    #s = '\xef\xbb\xbf'
    #nPos = image_id.index(s)
    #if nPos >= 0:
     #   image_id = image_id[3:]
    if flag == 0:
        in_file = open(savepath+'/trainImageXML/%s.xml' % (image_id))
        labeltxt = savepath+'/trainImageLabelTxt';
        if os.path.exists(labeltxt) == False:
            os.mkdir(labeltxt);
        out_file = open(savepath+'/trainImageLabelTxt/%s.txt' % (image_id), 'w')
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
    elif flag == 1:
        in_file = open(savepath+'/validateImageXML/%s.xml' % (image_id))
        labeltxt = savepath + '/validateImageLabelTxt';
        if os.path.exists(labeltxt) == False:
            os.mkdir(labeltxt);
        out_file = open(savepath+'/validateImageLabelTxt/%s.txt' % (image_id), 'w')
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)



    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

def translate_xml_to_annotation(wd):
    savepath = os.getcwd();
    idtxt = savepath + "/validateImageId.txt";
    pathtxt = savepath + "/validateImagePath.txt";
    image_ids = open(idtxt).read().strip().split()
    list_file = open(pathtxt, 'w')
    s = '\xef\xbb\xbf'
    for image_id in image_ids:
        nPos = image_id.find(s)
        if nPos >= 0:
            image_id = image_id[3:]
        list_file.write('%s/validateImage/%s.jpg\n' % (wd, image_id))
        print(image_id)
        convert_annotation(image_id, 1, savepath)
    list_file.close()

    idtxt = savepath + "/trainImageId.txt";
    pathtxt = savepath + "/trainImagePath.txt" ;
    image_ids = open(idtxt).read().strip().split()
    list_file = open(pathtxt, 'w')
    s = '\xef\xbb\xbf'
    for image_id in image_ids:
        nPos = image_id.find(s)
        if nPos >= 0:
           image_id = image_id[3:]
        list_file.write('%s/trainImage/%s.jpg\n'%(wd,image_id))
        print(image_id)
        convert_annotation(image_id,0,savepath)
    list_file.close()
    
    pass

if __name__ == '__main__':
    cur_path = os.getcwd()
    print 'Current path:\t', cur_path
    img_path = cur_path + "/Image"
    print 'Image raw data path:\t', img_path
    valid_num = 10
    process_data(img_path, cur_path, valid_num)
    translate_xml_to_annotation(cur_path)
    pass
    
