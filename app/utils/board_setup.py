
class BoardSetup:

    board_height = 500
    board_width = 400
    x_margin = 38
    y_margin = 34

    # board_height = 334
    # board_width = 380
    # x_margin = 16
    # y_margin = 16

    def __init__(self, x_num=7, y_num=10):
        self.x_num = x_num
        self.y_num = y_num
        inner_width = self.board_width - (self.x_margin * 2)
        inner_height = self.board_height - (self.y_margin * 2)
        self.x_spacing = inner_width / (self.x_num - 1)
        self.y_spacing = inner_height / (self.y_num - 1)
        self.x_coords = [self.x_margin]
        self.y_coords = [self.y_margin]
        self.append_coords()

    def append_coords(self):
        for n in range(1, self.x_num):
            self.x_coords.append(self.x_margin + int(n * self.x_spacing))
        for n in range(1, self.y_num):
            self.y_coords.append(self.y_margin + int(n * self.y_spacing))
