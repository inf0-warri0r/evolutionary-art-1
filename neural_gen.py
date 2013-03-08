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

import math
import random


class node:

    def __init__(self, inp):

        self.num_inputs = inp
        self.weights = list()
        self.inputs = list()
        self.errors = list()
        self.output = 0.0


class layer:

    def __init__(self, nn):

        self.num_nodes = nn
        self.chr = list()


class neural:

    def __init__(self, inp, out, num, hn):

        self.layers = list()
        self.weights = list()
        self.num_inputs = inp
        self.num_outputs = out
        self.num_layers = num
        self.num_hid_nodes = hn
        self.num_weights = 0
        self.fitness = 0.0

        l_in = layer(inp)

        for i in range(0, self.num_inputs):
            tmp = node(1)
            l_in.chr.append(tmp)
            self.num_weights = self.num_weights + 1

        self.layers.append(l_in)

        for i in range(1, self.num_layers - 1):

            ltmp = layer(self.num_hid_nodes)
            nd = self.layers[i - 1].num_nodes

            for j in range(0, hn):
                tmp = node(nd + 1)
                ltmp.chr.append(tmp)
                self.num_weights = self.num_weights + nd + 1

            self.layers.append(ltmp)

        nd = self.layers[self.num_layers - 2].num_nodes
        l_out = layer(self.num_outputs)

        for i in range(0, self.num_outputs):
            tmp = node(nd + 1)
            l_out.chr.append(tmp)
            self.num_weights = self.num_weights + nd + 1

        self.layers.append(l_out)

    def init(self):

        for i in range(0, self.num_layers):
            for j in range(0, self.layers[i].num_nodes):
                for k in range(0, self.layers[i].chr[j].num_inputs):
                    w = random.randrange(-1.0, 1.0)
                    self.layers[i].chr[j].weights.append(w)
                    self.weights.append(0.0)
                    self.layers[i].chr[j].inputs.append(0.0)
                    self.layers[i].chr[j].errors.append(0.0)

    def get_num_weights(self):

        return self.num_weights

    def get_fitness(self):

        return self.fitness

    def update_fitness(self, value):

        self.fitness = self.fitness + value

    def reset_fitness(self):

        self.fitness = 0.0

    def get_weights(self):

        n = 0

        for i in range(0, self.num_layers):
            for j in range(0, self.layers[i].num_nodes):
                for k in range(0, self.layers[i].chr[j].num_inputs):
                    self.weights[n] = self.layers[i].chr[j].weights[k]
                    n = n + 1
        return self.weights

    def put_weights(self, weights):

        n = 0

        for i in range(0, self.num_layers):
            for j in range(0, self.layers[i].num_nodes):
                for k in range(0, self.layers[i].chr[j].num_inputs):
                    self.layers[i].chr[j].weights[k] = weights[n]
                    n = n + 1

    def update(self, inputs):

        outputs = list()

        for i in range(0, self.num_layers):
            outputs = list()
            if i == 0:
                sm = 0.0

                for j in range(0, self.layers[i].num_nodes):
                    self.layers[i].chr[j].inputs[0] = inputs[0]
                    sm = sm + self.layers[i].chr[j].weights[0] * inputs[j]
                    self.layers[i].chr[j].output = self.convert(sm)
                    outputs.append(self.convert(sm))
            else:
                for j in range(0, self.layers[i].num_nodes):
                    sm = 0.0

                    for k in range(0, self.layers[i].chr[j].num_inputs - 1):
                        self.layers[i].chr[j].inputs[k] = inputs[k]
                        sm = sm + self.layers[i].chr[j].weights[k] * inputs[k]

                    index = self.layers[i].chr[j].num_inputs - 1
                    sm = sm - self.layers[i].chr[j].weights[index]
                    self.layers[i].chr[j].output = self.convert(sm)
                    outputs.append(self.convert(sm))

            inputs = outputs

        return outputs

    def get_weighted_error(self, l, inp):
        sm = 0.0
        for j in range(0, self.layers[l].num_nodes):
            error = self.layers[l].chr[j].errors[inp]
            weight = self.layers[l].chr[j].weights[inp]
            sm += error * weight
        return sm

    def convert(self, value):
        return (1.0 / (1.0 + math.exp(-1.0 * value)))
