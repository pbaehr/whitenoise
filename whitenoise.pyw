from __future__ import division
import audiere
import Tkinter
import argparse

class App:
    def __init__(self, master, volume=100, pitch=100):
        frame = Tkinter.Frame(master, padx=10, pady=10)
        frame.pack()

        self.play_image = Tkinter.PhotoImage(file='sound.gif')
        self.stop_image = Tkinter.PhotoImage(file='sound_mute.gif')

        self.start_stop_button = Tkinter.Button(frame, image=self.stop_image, command=self.toggle_noise)
        self.start_stop_button.pack(side=Tkinter.LEFT, padx=10)

        slider_frame = Tkinter.Frame(frame)
        slider_frame.pack(side=Tkinter.LEFT)

        self.pitch_scale = Tkinter.Scale(slider_frame, label='Pitch', command=self.pitch_change,
                                         from_=1, to=200, orient=Tkinter.HORIZONTAL)
        self.pitch_scale.set(pitch)
        self.pitch_scale.pack()

        self.volume_scale = Tkinter.Scale(slider_frame, label="Volume", command=self.volume_change,
                                          from_=0, to=100, orient=Tkinter.HORIZONTAL)
        self.volume_scale.set(volume)
        self.volume_scale.pack()

        self.d = audiere.open_device()
        self.whitenoise = self.d.create_white()

        self.whitenoise.play()

    def toggle_noise(self):
        if self.whitenoise.playing:
            self.whitenoise.stop()
            self.start_stop_button.config(image=self.play_image)
        else:
            self.whitenoise.play()
            self.start_stop_button.config(image=self.stop_image)

    def pitch_change(self, v):
        self.whitenoise.pitchshift = float(v) / 100

    def volume_change(self, v):
        self.whitenoise.volume = float(v) / 100

    def destroy(self):
        self.whitenoise.stop()
        root.destroy()

arg_parser = argparse.ArgumentParser(description='Generates white noise')
arg_parser.add_argument('-v', '--volume', type=int,
                        dest='volume', help='Initial volume for white noise',
                        choices=range(1,101), default=100)
arg_parser.add_argument('-p', '--pitch', type=int,
                        dest='pitch', help='Initial pitch for white noise',
                        choices=range(0, 201), default=100)
args = arg_parser.parse_args()

root = Tkinter.Tk()
root.title("White Noise")
root.iconbitmap(default='wn.ico')
root.resizable(0, 0)

app = App(root, args.volume, args.pitch)
root.protocol('WM_DELETE_WINDOW', app.destroy)

root.mainloop()
