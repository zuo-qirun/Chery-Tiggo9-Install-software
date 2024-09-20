import easygui as g

class ModeChooser:
    def __init__(self, modes: list, wrong_code: int = -1, wrong_input_message: str = "输入错误，请重新输入！"):
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
    def getmode(self):
        try:
            mode_input_str = g.choicebox(msg="请选择模式：", title="模式选择", choices=self.modes)
            mode_input = self.modes.index(mode_input_str)
            if mode_input < 0 or mode_input > len(self.modes) - 1:
                print(self.wrong_input_message)
                return self.wrong_code
            else:
                return mode_input
        except ValueError:
            print(self.wrong_input_message)
            return self.wrong_code
        except AttributeError:
            print(self.wrong_input_message)
            return self.wrong_code

if __name__ == "__main__":
    modes = ["模式1", "模式2", "模式3"]
    mode_chooser = ModeChooser(modes)
    print(mode_chooser)
    mode_input = mode_chooser.getmode()
    print(mode_input)