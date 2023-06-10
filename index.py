from loader import conf
from loader import color
from loader import ultis
from loader import menu

import subprocess
config = conf.config
mode_run = int(config.get('run', 'console'))






if mode_run == 1:
    while True:
        ultis.clear()
        for section in config.sections():
            print(color.yellow, '==>', color.ubgreen, section, color.end)
            for key in config[section]:
                print(
                    color.yellow,
                    '[' + color.cyan + key + color.yellow + ']',
                    color.white, '=', color.purple,
                    config[section][key],
                )

        # load menu functions
        print(color.yellow, '==>', color.ubgreen, 'Menu', color.end)
        for KEY, VALUE in menu.tool_function.items():
            print(color.yellow, '[' + color.cyan + KEY + color.yellow + ']', color.white, '=', color.purple, VALUE)
        print("\n"*5)
        choice = input(color.yellow + '$' + color.end)
    
        if choice in menu.tool_function.keys():
            subprocess.call(['python', 'function/' + choice + '.py'])
        