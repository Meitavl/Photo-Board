from PIL import ImageTk, Image


class PhotoSet:
    def __init__(self, img, num):

        self.real_img = img
        self.img = img
        self.num = num
        self.rotate = 0
        self.angle = 0
        self.size = (302, 302)
        self.row = 0
        self.column = 0
        self.photo = ImageTk.PhotoImage(self.img)
        self.bd = 5
        self.frame_size = [312, 312]
        self.relief = "solid"
        self.bg = "black"
        self.image_edit()

    def print_p(self):

        print(self.img, self.size, self.rotate, self.photo)

    def photo_rotate(self, angle):

        self.rotate = angle
        self.angle += angle
        self.image_edit()

    def photo_resize(self, width, height):

        size = [width, height]

        self.size = tuple(size)
        self.img_frame_size()
        self.image_edit()

    def img_frame_size(self):

        self.frame_size = [self.size[0] + self.bd * 2, self.size[1] + self.bd * 2]

    def img_grid(self, row, column):

        self.row = row
        self.column = column

    def image_edit(self):

        self.img = self.real_img.resize(self.size, Image.ANTIALIAS)
        self.img = self.img.rotate(self.angle)
        self.photo = ImageTk.PhotoImage(self.img)

    def image_att_copy(self, copy):
        self.size = copy.size
        self.bd = copy.bd
        self.bg = copy.bg
        self.relief = copy.relief

