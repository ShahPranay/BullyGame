import pygame
from src.support import *

def fun_0(chattrees, entity_map):
    if entity_map['bully1'].finished_chat:
        entity_map['bully1'].mood = 'idle'
        return 1
    else:
        return 0

def fun_1(chattrees, entity_map):
    if entity_map['player'].grass_cnt >= 10:
        entity_map['bully1'].set_chat_node(chattrees['bully1_finishtask'])
        return 4

    if entity_map['bully1'].finished_chat:
        entity_map['bully1'].mood = 'idle'
        entity_map['bully1'].set_chat_node(chattrees['bully1_standby'])

    return 1
        # successfully completed

class Story:
    def __init__(self, entity_map):
        self.cur_state = 0
        self.entity_map = entity_map
        self.chattrees = import_csv_chat_tree('./chat_trees')

        entity_map['bully1'].set_chat_node(self.chattrees['bully1_givetask'])
        
        self.funcs = {
                0 : fun_0,
                1 : fun_1,
                }

    def update(self):
        self.cur_state = self.funcs[self.cur_state](self.chattrees, self.entity_map)
