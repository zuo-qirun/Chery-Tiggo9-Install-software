# This code is used to select the mode of the software.
# Made by zuo-qirun/undefined_左

class Mode:
    def __init__(self, modes: list = [], wrong_code: int = -1, wrong_input_message: str = "输入错误，请重新输入！"):
        self.modes = modes
        self.wrong_code = wrong_code
        self.wrong_input_message = wrong_input_message

    def __str__(self) -> str:
        ret = ""
        for mode in self.modes:
            ret += f"{self.modes.index(mode)}. {mode}\n"
        return ret
    def addmode(self, mode: list):
        for m in mode:
            if m not in self.modes:
                self.modes.append(m)
    
    def printmodes(self):
        for mode in self.modes:
            print(f"{self.modes.index(mode)}. {mode}")
    
    def getmode(self):
        try:
            self.printmodes()
            mode_input = int(input(f"请输入模式序号(0-{len(self.modes)-1}): "))
            if mode_input < 0 or mode_input > len(self.modes) - 1:
                print(self.wrong_input_message)
                print(f"mode_input: {mode_input}")
                return self.wrong_code
            else:
                return mode_input
        except ValueError:
            print(self.wrong_input_message)
            return self.wrong_code

if __name__ == "__main__":
    while True:
        mode = Mode()
        mode.addmode(["模式1", "模式2", "模式3"])
        mode_input = mode.getmode()
        if mode_input != mode.wrong_code:
            print(f"你选择的模式是: {mode.modes[mode_input]}")