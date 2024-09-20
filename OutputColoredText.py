# This code is used to print colored text in the console.
# Made by zuo-qirun/undefined_左
colors = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m",
    "normal": ""
}

class ColoredText:
    def __init__(self, textsandcolors: list):
        '''
        textsandcolors: list of tuples, where each tuple contains a string and a color name.
        Example: [("Hello, world!", "green"), ("Error: Something went wrong!", "red")]
        '''
        try:
            self.texts = [textandcolor[0] for textandcolor in textsandcolors]
            self.colors = [textandcolor[1] for textandcolor in textsandcolors]
        except IndexError:
            raise ValueError("Invalid textsandcolors format")

    def __str__(self):
        '''
        Returns the colored text as a string.
        Example: "\033[32mHello, world!\033[0m\n\033[31mError: Something went wrong!\033[0m"
        '''
        text = ""
        try:
            for i in range(len(self.texts)):
                text += colors[self.colors[i]] + self.texts[i] + colors["reset"]
        except KeyError:
            raise ValueError("Invalid color name")
        return text
    

if __name__ == "__main__":
    text = ColoredText([("Hello, world!", "green"), ("Error: Something went wrong!", "red")])
    print(text)