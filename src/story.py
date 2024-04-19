import pygame
from src.support import *

def fun_0(story):
    if story.entity_map['bully1'].finished_chat:
        story.entity_map['bully1'].mood = 'idle'
        story.level.create_security()
        story.entity_map['security'].set_chat_node(story.chattrees['security_complain'])
        return 1
    else:
        return 0

def fun_1(story):
    if story.entity_map['player'].grass_cnt >= 1:
        story.entity_map['bully1'].set_chat_node(story.chattrees['bully1_finishtask'])
        return 2

    if story.entity_map['security'].finished_chat:
        story.entity_map['security'].mood = 'idle'
        if story.level.chatbox.choice_made == 1:
            story.level.chatbox.choice_made = 0
        else:
            story.entity_map['bully1'].kill()
            del story.entity_map['bully1']
            story.level.create_bully2()
            story.entity_map['bully2'].set_chat_node(story.chattrees['bully2_givetask'])
            return 3

    if story.entity_map['bully1'].finished_chat:
        story.entity_map['bully1'].mood = 'idle'
        story.entity_map['bully1'].set_chat_node(story.chattrees['bully1_standby'])

    return 1
        # successfully completed

def fun_2(story):
    if 'bully1' in story.entity_map and story.entity_map['bully1'].finished_chat:
        story.entity_map['bully1'].kill()
        del story.entity_map['bully1']
        story.level.create_bully2NA()
        story.entity_map['bully2'].set_chat_node(story.chattrees['bully2_givetask'])
        return 3

    return 2

def fun_3(story):
    if story.entity_map['player'].panty_cnt >= 1:
        story.entity_map['bully2'].set_chat_node(story.chattrees['bully2_finishtask'])
        return 4

    if story.entity_map['bully2'].finished_chat:
        if story.level.chatbox.choice_made == 1:
            story.level.chatbox.choice_made = 0
            story.level.create_bully2A()
            story.entity_map['bully2'].mood = 'attack'
            return 5
        else:
            story.entity_map['bully2'].mood = 'idle'
            story.entity_map['bully2'].set_chat_node(story.chattrees['bully2_standby'])

    return 3

def fun_4(story):
    if 'bully2' in story.entity_map and story.entity_map['bully2'].finished_chat:
        story.entity_map['bully2'].kill()
        del story.entity_map['bully2']
        story.level.create_bully3()
        story.entity_map['bully3'].set_chat_node(story.chattrees['bully3_givetask'])
        return 6
    
    return 4

def fun_5(story):
    if story.entity_map['bully2'].health <= 0:
        story.entity_map['player'].unlock_bat()
        del story.entity_map['bully2']
        story.level.create_bully3()
        story.entity_map['bully3'].set_chat_node(story.chattrees['bully3_givetask'])
        return 6

    return 5

def fun_6(story):
    if story.entity_map['bully3'].finished_chat:
        story.entity_map['bully3'].mood = 'idle'
        story.entity_map['bully3'].set_chat_node(story.chattrees['bully3_standby'])
        story.level.create_bully4()
        story.entity_map['bully4'].set_chat_node(story.chattrees['student_intro'])
        return 7

    return 6 


def fun_7(story):
    if story.entity_map['bully4'].finished_chat:
        if story.level.chatbox.choice_made == 1:
            story.level.chatbox.choice_made = 0
            story.entity_map['bully4'].mood = 'attack'
            story.entity_map['bully3'].set_chat_node(story.chattrees['bully3_finishtask'])
            return 8
        else:
            story.entity_map['bully4'].mood = 'idle'
            story.entity_map['player'].unlock_magic()
            story.entity_map['bully3'].set_chat_node(story.chattrees['bully3_betray'])
            return 9

    if story.entity_map['bully3'].finished_chat:
        if story.level.chatbox.choice_made == 1:
            story.level.chatbox.choice_made = 0
            story.entity_map['bully3'].mood = 'attack'
            return 10
        else:
            story.entity_map['bully3'].mood = 'idle'
            story.entity_map['bully3'].set_chat_node(story.chattrees['bully3_standby'])

    return 7


def fun_8(story):
    if story.entity_map['bully3'].finished_chat:
        story.entity_map['bully3'].kill()
        return 10

    return 8 

def fun_9(story):
    if story.entity_map['bully3'].finished_chat:
        story.entity_map['bully3'].mood = 'attack'
        return 10
    
    return 9

def fun_10(story):
    print("game over")
    return 10

class Story:
    def __init__(self, level):
        self.cur_state = 0
        self.entity_map = level.entity_map
        self.chattrees = import_csv_chat_tree('./chat_trees')
        self.level = level

        self.entity_map['bully1'].set_chat_node(self.chattrees['bully1_givetask'])
        
        self.funcs = {
                0 : fun_0,
                1 : fun_1,
                2 : fun_2,
                3 : fun_3,
                4 : fun_4,
                5 : fun_5,
                6 : fun_6,
                7 : fun_7,
                8 : fun_8,
                9 : fun_9,
                10 : fun_10,
                }

    def update(self):
        self.cur_state = self.funcs[self.cur_state](self)
