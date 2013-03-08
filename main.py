#!/usr/bin/env python

"""
Author : tharindra galahena (inf0_warri0r)
Project: evolutionary art generator
Blog   : http://www.inf0warri0r.blogspot.com
Date   : 08/03/2013
License:

     Copyright 2013 Tharindra Galahena

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version. This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details.

* You should have received a copy of the GNU General Public License along with
This program. If not, see http://www.gnu.org/licenses/.

"""

import Tkinter as tk
import thread
import time
import neural_gen
import ga
from PIL import Image as im, ImageTk
import random


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.image = im.new("RGB", (200, 200))
        self.pix = self.image.load()
        self.net = list()

        for i in range(0, 10):
            self.net.append(neural_gen.neural(2, 1, 4, 5))
            self.net[i].init()

        self.pop = ga.population(10, self.net[0].num_weights, 90, 30)

        self.chro = self.pop.genarate()
        self.fit = list()
        for i in range(0, 10):
            self.fit.append(0.0)
            self.net[i].reset_fitness()
            self.net[i].put_weights(self.chro[i])

        self.gen_count = 0
        self.timer = 0
        self.vote_mode = False
        self.run = False
        self.ft = 0.0
        self.vt = False

    def createWidgets(self):
        self.start_button = tk.Button(self, text='start', command=self.red)
        self.stop_button = tk.Button(self, text='stop', command=self.stop)
        self.vote_button = tk.Button(self, text='vote', command=self.vote)

        self.content = tk.StringVar()
        self.gen_entry = tk.Entry()
        self.chr_entry = tk.Entry()
        self.vote_entry = tk.Entry(textvariable=self.content)

        self.canvas = tk.Canvas(width=640, height=640, background="black")

        self.start_button.grid(column=0, row=0, sticky=tk.W)
        self.stop_button.grid(column=1, row=0, sticky=tk.W)
        self.vote_button.grid(column=2, row=0, sticky=tk.W)
        self.var = tk.IntVar()
        self.check_vote = tk.Checkbutton(text="Vote mode", variable=self.var)
        self.check_vote.grid(row=1, sticky=tk.W)

        tk.Label(text="Genaration :").grid(column=0, row=2, sticky=tk.W)
        tk.Label(text="Art             :").grid(column=0, row=3, sticky=tk.W)
        tk.Label(text="Vote           :").grid(column=0, row=4, sticky=tk.W)

        self.gen_entry.grid(column=0, row=2)
        self.chr_entry.grid(column=0, row=3)
        self.vote_entry.grid(column=0, row=4)

        self.chr_entry.delete(0, tk.END)
        self.chr_entry.insert(0, "0")
        self.gen_entry.delete(0, tk.END)
        self.gen_entry.insert(0, "0")
        self.vote_entry.delete(0, tk.END)
        self.vote_entry.insert(0, "0")

        self.canvas.grid(row=5)

    def vote(self):
        if self.var.get() == 1:
            text = self.content.get()

            self.ft = float(text)
            print "ft = ", self.ft
            if self.ft > 100:
                self.ft = 100
            elif self.ft < 0:
                self.ft = 0
            self.vt = True

    def red(self):
        self.run = True
        thread.start_new_thread(self.thread_func, ())

    def stop(self):
        self.run = False
        self.gen_entry.delete(0, tk.END)
        self.gen_entry.insert(0, "0")
        self.chr_entry.delete(0, tk.END)
        self.chr_entry.insert(0, "0")
        self.vote_entry.delete(0, tk.END)
        self.vote_entry.insert(0, "0")

    def thread_func(self):
        if self.var.get() == 1:
            self.vote_mode = True
        else:
            self.vote_mode = False

        self.gen_entry.delete(0, tk.END)
        self.gen_entry.insert(0, "1")
        self.chr_entry.delete(0, tk.END)
        self.chr_entry.insert(0, "0")
        while self.run:
            if self.timer >= 1:
                self.timer = 0
                for i in range(0, 10):
                    self.fit[i] = self.net[i].get_fitness()

                self.chro = self.pop.new_gen(self.fit)

                for i in range(0, 10):
                    self.net[i].reset_fitness()
                    self.net[i].put_weights(self.chro[i])

                self.gen_count = self.gen_count + 1
                self.gen_entry.delete(0, tk.END)
                self.gen_entry.insert(0, str(self.gen_count + 1))

            for i in range(0, 10):
                if not self.run:
                    break
                for y in range(0, 200):
                    for x in range(0, 200):
                        l = ((x - 100) ** 2.0 + (y - 100) ** 2.0) ** 0.5
                        l = l / 10.0
                        t = float(y * 200 + x - 200 * 100) / (200 * 100)
                        inps = [l, t]
                        outputs = self.net[i].update(inps)
                        m = 0b00000000111111111111111111111111
                        color = int(outputs[0] * m)
                        r = (color & 0b00000000111111110000000000000000) >> 16
                        g = (color & 0b00000000000000001111111100000000) >> 8
                        b = color & 0b00000000000000000000000011111111

                        self.pix[x, y] = (r, g, b)

                image2 = self.image.resize((600, 600))
                im = ImageTk.PhotoImage(image2)
                self.canvas.delete(tk.ALL)
                self.canvas.create_image(20, 20, anchor=tk.NW, image=im)
                self.canvas.update()
                self.chr_entry.delete(0, tk.END)
                self.chr_entry.insert(0, str(i + 1))
                if self.vote_mode:
                    while not self.vt:
                        if not self.run:
                            break
                        time.sleep(0.01)
                    self.vt = False
                    self.vote_entry.delete(0, tk.END)
                    self.vote_entry.insert(0, "0")
                else:
                    self.ft = random.uniform(0, 100)
                self.net[i].update_fitness(self.ft)
            self.timer = self.timer + 1

if __name__ == '__main__':

    app = Application()
    app.master.title('evolutionary art generator')
    app.mainloop()
