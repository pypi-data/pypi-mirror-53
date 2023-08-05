from tkinter import Tk, Label, Button, Entry, Checkbutton, filedialog
from pathlib import Path
from copy_spotlights import copy_spotlights_images

# default padding settings
px = 20
py = 10


class MyGui:

    def __init__(self):

        self.window = Tk()
        self.window.title('Extract Spotlight Images')

        # setting default values for variables
        self.home = Path.home()
        self.source_location = Path.joinpath(self.home, Path('AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets'))
        self.save_location = Path.joinpath(self.home, Path('Desktop'))
        self.split = True
        self.min_res = 1920

        # setting up buttons and their actions
        self.b_save = Button(self.window, text="Save Location", command=self.set_save_location)
        self.b_source = Button(self.window, text="Spotlights source", command=self.set_source_location)
        self.b_reset = Button(self.window, text="Set Defaults", command=self.reset)
        self.b_split = Checkbutton(self.window, text="Don't split", command=self.toggle_split)
        self.b_min_res = Entry(self.window, textvariable=self.min_res)
        self.b_main = Button(self.window, text="Get Spotlights", command=self.copy_spotlights, fg="white", bg="green", bd=4)

        # setting up labels to represent button actions
        self.l_save = Label(self.window, text=self.save_location)
        self.l_source = Label(self.window, text=self.source_location)
        self.l_settings = Label(self.window, text="Advanced Settings below :")
        self.l_split = Label(self.window, text="If checked, landscape and portrait image will not be separated")
        self.l_min_res = Label(self.window, text="Only include images with width or height greater than or equal to this value")

        self.setup_button_layouts()
        self.setup_label_layouts()

        self.window.mainloop()

    def setup_button_layouts(self):
        self.b_save.grid(row=0, column=0, padx=px, pady=py)
        self.b_source.grid(row=3, column=0, padx=px, pady=py)
        self.b_min_res.grid(row=5, column=0, padx=px, pady=py)
        self.b_min_res.insert(0, self.min_res)
        self.b_reset.grid(row=6, column=0, padx=px, pady=py)
        self.b_split.grid(row=4, column=0, padx=px, pady=py)
        self.b_main.grid(row=1, columnspan=2, padx=2*px, pady=2*py)

    def setup_label_layouts(self):
        self.l_save.grid(row=0, column=1, padx=px, pady=py)
        self.l_source.grid(row=3, column=1, padx=px, pady=py)
        self.l_split.grid(row=4, column=1, padx=px, pady=py)
        self.l_settings.grid(row=2, column=0, padx=px, pady=py)
        self.l_source.grid(row=3, column=1, padx=px, pady=py)
        self.l_min_res.grid(row=5, column=1, padx=px, pady=py)

    def update_labels(self):
        self.l_save.destroy()
        self.l_save = Label(self.window, text=self.save_location)
        self.l_source.destroy()
        self.l_source = Label(self.window, text=self.source_location)
        self.setup_label_layouts()

    def set_source_location(self):
        source_location = filedialog.askdirectory()
        if source_location:
            self.source_location = source_location
        self.update_labels()

    def set_save_location(self):
        save_location = filedialog.askdirectory()
        if save_location:
            self.save_location = save_location
        self.update_labels()

    def toggle_split(self):
        self.split = False if self.split else True

    def copy_spotlights(self):
        min_res = self.b_min_res.get()
        if min_res:
            self.min_res = min_res
        copy_spotlights_images(self.source_location, self.save_location, self.split, self.min_res)
        self.popup_finished()

    @staticmethod
    def popup_finished():
        done = Tk()
        Label(done, text="Finished!").grid(row=0, columnspan=3, padx=2*px, pady=py)
        Button(done, text="Ok", command=done.destroy).grid(row=1, column=1, padx=px)

    def reset(self):
        self.window.destroy()
        self.__init__()


def main():
    MyGui()


if __name__ == '__main__':
    main()
