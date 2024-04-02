import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import glob, os
from matplotlib.widgets import Button

class Annotate(object):
    def __init__(self, image_list):
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
        self.image_list = image_list

    def get_figure(self):
        return self.ax.figure

    def on_press(self, event):
        print('press')
        self.x0 = event.xdata
        self.y0 = event.ydata

    def on_release(self, event):
        print('release')
        self.x1 = event.xdata
        self.y1 = event.ydata
        self.rect.set_width(self.x1 - self.x0)
        self.rect.set_height(self.y1 - self.y0)
        self.rect.set_xy((self.x0, self.y0))
        self.rect.set_fill(False)
        self.rect.set_edgecolor('red')
        self.rect.set_linewidth(2)
        self.ax.figure.canvas.draw()

    def next(self, event):
        self.ind += 1
        #i = self.ind % len(freqs)
        #ydata = np.sin(2*np.pi*freqs[i]*t)
        #l.set_ydata(ydata)
        #plt.draw()
        print(f"index: {self.ind}")
        #print(f"coord: {coords}")
        image = Image.open(self.image_list[self.ind])
        self.ax.imshow(image)
        plt.show()
        #plt.imshow(image)

    def prev(self, event):
        self.ind -= 1
        #i = self.ind % len(freqs)
        #ydata = np.sin(2*np.pi*freqs[i]*t)
        #l.set_ydata(ydata)
        #plt.draw()
        print(f"index: {self.ind}")
        #print(f"coord: {coords}")
        image = Image.open(self.image_list[self.ind])
        self.ax.imshow(image)
        plt.show()

    def test(self, event):
        print(f"Coords: {self.rect.get_width()}, ")


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
    axtest = a.get_figure().add_axes([0.5, 0.01, 0.1, 0.075])

    bnext = Button(axnext, 'Next')
    bnext.on_clicked(a.next)
    bprev = Button(axprev, 'Previous')
    bprev.on_clicked(a.prev)
    btest = Button(axtest, 'Test')
    btest.on_clicked(a.test)

    plt.show()

if __name__ == "__main__":
    main()