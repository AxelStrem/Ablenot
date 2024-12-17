import gzip
import xml.etree.ElementTree as ET
import os
import shutil
import copy
import sys

def spawn_dir(newpath):
    if not os.path.exists(newpath):
        os.makedirs(newpath)

proj_name = sys.argv[1]

with gzip.open(proj_name+'.als', 'rb') as f:
    file_content = f.read()

root = ET.fromstring(file_content)

tracks = root.find('LiveSet').find('Tracks')

track_list = []
for track in tracks:
    track_list.append(copy.deepcopy(track))
    for track_child in list(track):
        track.remove(track_child)        
    
try:
    shutil.rmtree(proj_name)
except OSError as e:
    pass #shhhh that's okay
    
spawn_dir(proj_name)
    

for p in track_list:    
    track_id = p.attrib.get('Id')
    track_name = p.tag + track_id
    track_path = proj_name + '\\' + track_name
    spawn_dir(track_path)
    track_tree = ET.ElementTree(p)
    with open(track_path+'\\' + track_name+'.xml', 'w') as f:
        track_tree.write(f, encoding='unicode')
    
    
tree = ET.ElementTree(root)
with open(proj_name+'\\' + proj_name+'.xml', 'w') as f:
    tree.write(f, encoding='unicode')

