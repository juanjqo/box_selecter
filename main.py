import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import glob, os
from matplotlib.widgets import Button
import time

class Annotate(object):
    def __init__(self, image_list):
        self.plt = plt
        self.ax = plt.gca()
        self.rect = Rectangle((0,0), 1, 1)
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.ax.add_patch(self.rect)
        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.ind = 0
        self.previous_ind = -1
        self.image_list = image_list
        self.coords = []
        self.area = 0
        self.area_threshold = 100
        self.counter_saves_per_image = 0
        self.reduce_factor = 10
        self.current_image_size = []
        self.img = self.ax.imshow(self.get_resized_image_from_index(0), aspect='auto')
        #
        self.ax.set_title(self.image_list[self.ind], loc='center', fontstyle='oblique', fontsize='medium')

    def get_resized_image_from_index(self, index):
        image = Image.open(self.image_list[index])
        new_size = (int((1 / self.reduce_factor) * image.size[0]), int((1 / self.reduce_factor) * image.size[1]))
        self.current_image_size = new_size
        return image.resize(new_size, Image.Resampling.LANCZOS)

    def get_figure(self):
        return self.ax.figure

    def on_press(self, event):
        self.x0 = event.xdata
        self.y0 = event.ydata
        #print(f'press. x0: {self.x0}, y0: {self.y0}')

    def on_release(self, event):
        self.x1 = event.xdata
        self.y1 = event.ydata
        #print(f'release. x1: {self.x1}, y1: {self.y1}')
        self.rect.set_width(self.x1 - self.x0)
        self.rect.set_height(self.y1 - self.y0)
        self.rect.set_xy((self.x0,self.y0))
        self.area = self.rect.get_width()*self.rect.get_height()
        if abs(self.area) > self.area_threshold:
            self.coords = [self.x0, self.y0, self.x1, self.y1]
        #print(f"area: {self.area}")
        self.rect.set_fill(False)
        self.rect.set_edgecolor('red')
        self.rect.set_linewidth(2)
        self.ax.figure.canvas.draw()

    def next(self, event):
        self.previous_ind = self.ind
        self.ind += 1
        #self.plt.cla()
        self.ax.set_title(self.image_list[self.ind], loc='center', fontstyle='oblique', fontsize='medium')

        self.img.set_data(self.get_resized_image_from_index(self.ind))
        self.img.set_extent((0, self.current_image_size[0], self.current_image_size[1], 0))

        #self.plt.cla()

        print("size:", self.current_image_size)
        plt.show()

    def prev(self, event):
        self.previous_ind = self.ind
        self.ind -= 1

        self.ax.set_title(self.image_list[self.ind], loc='center', fontstyle='oblique', fontsize='medium')
        self.img.set_data(self.get_resized_image_from_index(self.ind))
        self.img.set_extent((0, self.current_image_size[0], self.current_image_size[1], 0))
        #self.plt.cla()
        print("size:", self.current_image_size)
        plt.show()

    def save(self, event):
        print(f"Coords: {self.coords}, ")
        can_save_picture = False
        if len(self.coords) > 0:
            x0 = self.coords[0]
            y0 = self.coords[1]
            x1 = self.coords[2]
            y1 = self.coords[3]
            area = (x1 - x0)*(y1-y0)

            x0_is_lower_x1 = x0 < x1
            y0_is_lower_y1 = y0 < y1
            if x0_is_lower_x1:
                if y0_is_lower_y1:
                    img_area = (x0, y0, x1, y1)
                else:
                    img_area = (x0, y1, x1, y0)
            else:
                if y0_is_lower_y1:
                    img_area = (x1, y0, x0, y1)
                else:
                    img_area = (x1, y1, x0, y0)

            if abs(area) > self.area_threshold:
                if self.previous_ind == self.ind:
                    self.counter_saves_per_image += 1
                else:
                    self.counter_saves_per_image = 1
                    self.previous_ind = self.ind

                print("1. ", img_area)
                # Save image
                #img_area = (int(self.reduce_factor*img_area[0]), int(self.reduce_factor*img_area[1]),
                #            int(self.reduce_factor*img_area[2]), int(self.reduce_factor*img_area[3]))
                img_area = (self.reduce_factor * img_area[0], self.reduce_factor * img_area[1],
                            self.reduce_factor * img_area[2], self.reduce_factor * img_area[3])
                print("2. ", img_area)
                img = Image.open(self.image_list[self.ind])

                img_cropped = img.crop(img_area)

                print(img.size)
                new_name = self.image_list[self.ind][:-4] + "_" + str(self.counter_saves_per_image) + ".JPG"
                img_cropped.save(new_name)
                print(f"Image {self.counter_saves_per_image} from {self.image_list[self.ind]} was saved as {new_name}.")
                #img_cropped2.show()
                self.coords = []

            else:
                print("You need to select the box first.")
        else:
            print("You need to select the box first.")


def main() -> None:
    base_path = os.getcwd()
    origin_folder = base_path + '/images'
    os.chdir(origin_folder)
    image_list = []
    for file in glob.glob("*.jpg"):
        image_list.append(file)

    a = Annotate(image_list)
    axprev = a.get_figure().add_axes([0.7, 0.01, 0.1, 0.075])
    axnext = a.get_figure().add_axes([0.81, 0.01, 0.1, 0.075])
    axsave = a.get_figure().add_axes([0.5, 0.01, 0.1, 0.075])

    bnext = Button(axnext, 'Next')
    bnext.on_clicked(a.next)
    bprev = Button(axprev, 'Previous')
    bprev.on_clicked(a.prev)
    bsave = Button(axsave, 'Save')
    bsave.on_clicked(a.save)

    plt.show()


if __name__ == "__main__":
    main()