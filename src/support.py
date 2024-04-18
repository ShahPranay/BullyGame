from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
	terrain_map = []
	with open(path) as level_map:
		layout = reader(level_map,delimiter = ',')
		for row in layout:
			terrain_map.append(list(row))
		return terrain_map

def import_folder(path):
	surface_list = []

	for _,__,img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list

class TextNode:
    def __init__(self, nodeid, text, leftchoice = None, rightchoice = None, action_type = ''):
        self.nodeid = nodeid
        self.action_type = action_type
        self.text = text
        self.leftchoice = leftchoice
        self.rightchoice = rightchoice

    def get_choice_cnt(self):
        if self.leftchoice is not None:
            if self.rightchoice is not None:
                return 2
            else:
                return 1
        else:
            return 0

    def get_next_node(self, choice):
        if self.get_choice_cnt() == 0:
            return None
        elif self.get_choice_cnt() == 1:
            return self.leftchoice
        elif choice == 0:
            return self.leftchoice
        else:
            return self.rightchoice

def get_dict(dic, key):
    if key in dic.keys():
        return dic[key]
    else:
        return None

def import_csv_chat_tree(path):
    chat_tree = {  }
    for _, __, csv_files in walk(path):
        for csv_file in csv_files:
            full_path = path + '/' + csv_file
            all_lines = []
            with open(full_path) as file:
                tmp_tree = reader(file, delimiter=';')
                for row in tmp_tree:
                    all_lines.append(row)
            all_lines.reverse()
            nodes = {}
            for row in all_lines:
                # nodeid text leftid rightid action_type
                treenode = TextNode(int(row[0]), row[1], get_dict(nodes, row[2]), get_dict(nodes, row[3]), row[4])
                if row[0] == '0':
                    chat_tree[csv_file.split('.')[0]] = treenode
                else:
                    nodes[row[0]] = treenode
    return chat_tree
