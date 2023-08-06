""" liteco is an easy to use python script to add colors to your python program
    example:
    from liteco import show
    print('show.green')
    where green is the name of the color you want to use in your terminal application

    Limited amount of colors are available for now, more colors would be available in the next version
    """
import os

# this module is not optimized for the windows operating system
if os.name == 'nt':
    print('''This module is not optimized for Wndows operating system...
            would be available in later version''')
else:
    pass

# import all modules required by the program


class Color:
    def __init__(self):
        
        grey = '\033[1;30m\0'
        red = '\033[1;31m\0'
        green = '\033[1;32m\0'
        yellow = '\033[1;33m\0'
        blue = '\033[1;34m\0'
        purple = '\033[1;35m\0'
        cyan = '\033[1;36m\0'
        white = '\033[1;37m\0'
         
        self.grey = grey
        self.red = red
        self.green = green
        self.yellow = yellow
        self.blue = blue
        self.cyan = cyan
        self.purple = purple
        self.white = white


show = Color()

if __name__ == '__main__':
    import __main__
    
