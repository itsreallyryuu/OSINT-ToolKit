BRIGHT_RED = "\033[91m"
RED = "\033[31m"
DARK_RED = "\033[31;2m"
RESET = "\033[0m"

def show_banner():
    banner_lines = r"""
  ______   ______  ________   ______  ________   ______  
 /      \ |      \|        \ /      \|        \ /      \ 
|  $$$$$$\ \$$$$$$| $$$$$$$$|  $$$$$$\\$$$$$$$$|  $$$$$$\
| $$___\$$  | $$  | $$__    | $$___\$$  | $$   | $$__| $$
 \$$    \   | $$  | $$  \    \$$    \   | $$   | $$    $$
 _\$$$$$$\  | $$  | $$$$$    _\$$$$$$\  | $$   | $$$$$$$$
|  \__| $$ _| $$_ | $$_____ |  \__| $$  | $$   | $$  | $$
 \$$    $$|   $$ \| $$     \ \$$    $$  | $$   | $$  | $$
  \$$$$$$  \$$$$$$ \$$$$$$$$  \$$$$$$    \$$    \$$   \$$

                SIESTA v1 | OSINT FRAMEWORK!
                 :: Developed by Ryuudev ::

    """
    colors = [BRIGHT_RED, BRIGHT_RED, BRIGHT_RED]
    for i, line in enumerate(banner_lines.split("\n")):
        color = colors[i % len(colors)]
        print(color + line + RESET)
