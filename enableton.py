import gzip
import xml.etree.ElementTree as ET
import os
import shutil
import copy
import sys
import datetime

def spawn_dir(newpath):
    if not os.path.exists(newpath):
        os.makedirs(newpath)

proj_name = sys.argv[1]

tree = ET.parse(proj_name+'\\' + proj_name+'.xml')
root = tree.getroot()

tracks = root.find('LiveSet').find('Tracks')
for p in tracks:
    track_id = p.attrib.get('Id')
    track_name = p.tag + track_id
    track_path = proj_name + '\\' + track_name
    track_tree = ET.parse(track_path+'\\' + track_name+'.xml')
    for track_child in track_tree.getroot():
        p.append(track_child)

out_file = ET.tostring(tree.getroot(), encoding='unicode', method='xml')
out_file = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n" + out_file + "\r\n"

with gzip.open(proj_name+'.xml', 'wb', compresslevel = 9) as f:
    f.write(out_file.encode())
    
timestamp = datetime.datetime.now().strftime(" [%Y-%m-%d %H%M%S]")
try:
    shutil.move(proj_name+'.als', "Backup\\"+proj_name+timestamp+'.als')
except OSError as e:
    pass #shhhh that's okay
    
os.rename(proj_name+'.xml', proj_name+'.als')

