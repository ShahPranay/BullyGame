# game setup
WIDTH    = 1280	
HEIGTH   = 720
FPS      = 60
TILESIZE = 64
HITBOX_OFFSET = {
	'player': -26,
	'object': -40,
	'grass': -10,
	'invisible': 0}

# ui 
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = './graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# chatbox
CHATBOX_COLOR = '#111111'
CHOICE_COLOR = '#202020'
CHOICE_COLOR_SELECTED = '#EEEEEE'
CHOICE_TEXT_COLOR = '#EEEEEE'
CHOICE_TEXT_COLOR_SELECTED = '#202020'

# weapons 
weapon_data = {
	'fist': {'cooldown': 100, 'damage': 15,'graphic':'./graphics/weapons/fist/full.png'},
	'bat': {'cooldown': 400, 'damage': 30,'graphic':'./graphics/weapons/bat/full.png'},
	}

# magic
magic_data = {
	'rock': {'strength': 10,'cost': 20,'graphic':'./graphics/particles/rock/rock.png'}
	}

# enemy
monster_data = {
        'bully1': {'health': 100,'exp':100,'damage':10,'attack_type': 'slash', 'attack_sound':'./audio/attack/slash.wav', 'speed': 2, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360, 'attack_cooldown': 400},
	'bully2': {'health': 200,'exp':250,'damage':20,'attack_type': 'slash',  'attack_sound':'./audio/attack/slash.wav','speed': 3, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 400, 'attack_cooldown': 400},
	'bully3': {'health': 450,'exp':110,'damage':30,'attack_type': 'slash', 'attack_sound':'./audio/attack/slash.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 150, 'notice_radius': 350, 'attack_cooldown': 600},
	'bully4': {'health': 100,'exp':120,'damage':8,'attack_type': 'slash', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300, 'attack_cooldown': 600},
    'security': {'health': 1e8, 'exp': 0, 'damage': 0, 'attack_type': 'slash', 'attack_sound': './audio/attack/slash.wav', 'speed': 0, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 50, 'attack_cooldown': 400}
    }
