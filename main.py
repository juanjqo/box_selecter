import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import glob, os


from matplotlib.widgets import Button

def onclick(event):
    global ix, iy
    ix, iy = event.xdata, event.ydata
    print(f'x = {ix}, y = {iy}')

    global coords


    coords.append((ix, iy))
    if len(coords) == 2:
        fig.canvas.mpl_disconnect(cid)
        plt.close(1)
    return



fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)


class Index:
    ind = 0
    image_list = []

    def set_image_list(self, image_list):
        self.image_list = image_list

    def next(self, event):
        self.ind += 1
        #i = self.ind % len(freqs)
        #ydata = np.sin(2*np.pi*freqs[i]*t)
        #l.set_ydata(ydata)
        #plt.draw()
        print(f"index: {self.ind}")
        print(f"coord: {coords}")
        image = Image.open(self.image_list[self.ind])
        im = ax.imshow(image)
        plt.show()
        #plt.imshow(image)

    def prev(self, event):
        self.ind -= 1
        #i = self.ind % len(freqs)
        #ydata = np.sin(2*np.pi*freqs[i]*t)
        #l.set_ydata(ydata)
        #plt.draw()
        print(f"index: {self.ind}")
        print(f"coord: {coords}")
        image = Image.open(self.image_list[self.ind])
        im = ax.imshow(image)
        plt.show()

    def test(self, event):
        print(f"coord: {len(coords)}")
        print(f"len coord: {len(coords)}")


        #plt.imshow(image)


coords = []
def main() -> None:
    base_path = os.getcwd()
    origin_folder = base_path + '/images'
    os.chdir(origin_folder)
    image_list = []
    for file in glob.glob("*.jpg"):
        image_list.append(file)

    callback = Index()
    callback.set_image_list(image_list)

    axprev = fig.add_axes([0.7, 0.05, 0.1, 0.075])
    axnext = fig.add_axes([0.81, 0.05, 0.1, 0.075])
    axtest = fig.add_axes([0.5, 0.05, 0.1, 0.075])

    bnext = Button(axnext, 'Next')
    bnext.on_clicked(callback.next)
    bprev = Button(axprev, 'Previous')
    bprev.on_clicked(callback.prev)
    btest = Button(axtest, 'Test')
    btest.on_clicked(callback.test)
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    #timer = fig.canvas.new_timer(interval=100)
    #timer.add_callback(update_title, ax)
    #timer.start()


    print(image_list)
    plt.show()

if __name__ == "__main__":
    main()