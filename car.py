import numpy as np
import utils
import random
import pygame
import map


class Car:

    class NeuralNetwork:

        def __init__(self, layers):
            self.layers = layers
            self.num_layers = len(layers)
            self.weights = [np.random.randn(y, x) for y, x in zip(layers[:-1], layers[1:])]
            self.biases = [np.random.randn(1, x) for x in layers[1:]]
            self.input = np.ndarray((1, layers[0]))
            self.output = np.ndarray((1, layers[-1]))

        def forward(self, ds):
            self.input = [ds]
            self.input = utils.sigmoid(np.matmul(self.input, self.weights[0]) + self.biases[0])
            self.input = np.matmul(self.input, self.weights[1]) + self.biases[1]
            self.output = self.input
            return self.output

    def __init__(self):
        self.neural_network = self.NeuralNetwork([3, 7, 4])
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.img = pygame.image.load('Images/Sprites/car.png')
        self.rect = self.img.get_rect()
        self.img.fill(self.color)
        self.score = None
        self.alive = None
        self.x = None
        self.y = None
        self.angle = None
        self.velocity = None
        self.acceleration = None
        self.rotation = None
        self.init2()

    def init2(self):
        self.score = 0
        self.alive = True
        self.x = map.spawn_x
        self.y = map.spawn_y
        self.angle = 0
        self.velocity = 0
        self.acceleration = 0
        self.rotation = 0
        self.rect.center = (int(self.x), int(self.y))

    def draw(self, screen):
        screen.blit(self.img, self.rect)

    def rays(self):
        offsets = [0, 45, -45]
        res = []
        for offset in offsets:
            pos = (self.x, self.y)
            while not map.outside((int(pos[0]), int(pos[1]))):
                pos = utils.move((pos[0], pos[1]), self.angle + offset, 10)
            while map.outside((int(pos[0]), int(pos[1]))):
                pos = utils.move((pos[0], pos[1]), self.angle + offset, -1)
            res.append(utils.distance(pos, (self.x, self.y)))
        return res

    def process(self):
        decision = self.neural_network.forward(self.rays())

        if decision[0][0] > 0.5 and decision[0][1] > 0.5:
            self.acceleration = 0
        elif decision[0][0] > 0.5:
            self.acceleration = 1
        elif decision[0][1] > 0.5:
            self.acceleration = -1
        else:
            self.acceleration = 0

        if decision[0][2] > 0.5 and decision[0][3] > 0.5:
            self.rotation = 0
        elif decision[0][2] > 0.5:
            self.rotation = -1
        elif decision[0][3] > 0.5:
            self.rotation = 1
        else:
            self.rotation = 0

        return

    def update(self):

        if map.outside((self.x, self.y)):
            self.alive = False

        if not self.alive:
            return

        self.process()

        rotation_speed = 10
        acceleration_speed = 0.3
        max_speed = 10
        velocity_fraction = 0.90

        self.score += self.acceleration * acceleration_speed

        self.angle = (self.angle + self.rotation * rotation_speed) % 360

        if self.acceleration != 0:
            self.velocity += self.acceleration * acceleration_speed
            if self.velocity > max_speed:
                self.velocity = max_speed
            elif self.velocity < 0:
                self.velocity = 0
        else:
            self.velocity = self.velocity * velocity_fraction

        self.x, self.y = utils.move((self.x, self.y), self.angle, self.velocity)
        self.rect.center = (self.x, self.y)


cars = []


def draw(screen):
    for car in cars:
        car.draw(screen)


def update():
    for car in cars:
        car.update()


def refresh():
    for car in cars:
        car.init2()


def merge(car1: Car, car2: Car, cross, bias, weight, rareb, rarew) -> Car:
    car_new = Car()

    biases = []
    for ws, ws2 in zip(car1.neural_network.biases, car2.neural_network.biases):
        new_biases = np.ndarray(ws.shape)
        for j in range(ws.shape[0]):
            for i in range(ws.shape[1]):
                if np.random.rand() > cross:
                    new_biases[j][i] = ws[j][i]
                else:
                    new_biases[j][i] = ws2[j][i]
                if np.random.rand() < bias:
                    new_biases[j][i] *= 0.9 + np.random.rand() / 5  # 0.9 - 1.1
                if np.random.rand() < rareb:
                    new_biases[j][i] += np.random.randn() * np.random.rand()
        biases.append(new_biases)

    weights = []
    for ws, ws2 in zip(car1.neural_network.weights, car2.neural_network.weights):
        new_weights = np.ndarray(ws.shape)
        for j in range(ws.shape[0]):
            for i in range(ws.shape[1]):
                if np.random.rand() > cross:
                    new_weights[j][i] = ws[j][i]
                else:
                    new_weights[j][i] = ws2[j][i]
                if np.random.rand() < weight:
                    new_weights[j][i] *= 0.9 + np.random.rand() / 5  # 0.9 - 1.1
                if np.random.rand() < rarew:
                    new_weights[j][i] += np.random.randn() * np.random.rand()

        weights.append(new_weights)

    car_new.neural_network.biases = biases
    car_new.neural_network.weights = weights

    return car_new


def new_generation():
    cars.sort(key=lambda s: s.score)
    car1 = cars[-1]
    car2 = cars[-2]
    cars.clear()
    for i in range(10):
        cars.append(merge(car1, car2, 0.95, 0.1, 0.1, 0, 0))
    for i in range(10):
        cars.append(merge(car1, car2, 0.05, 0.1, 0.1, 0, 0))
    for i in range(10):
        cars.append(merge(car1, car2, 0.5, 0.1, 0.1, 0, 0))
    for i in range(10):
        cars.append(merge(car1, car2, 0.5, 0.1, 0.1, 0.1, 0.1))
    for i in range(10):
        cars.append(merge(car1, car2, 0.5, 0, 0, 0.1, 0.1))
    for i in range(10):
        cars.append(merge(car1, car2, 0.95, 0, 0, 0.1, 0.1))
    for i in range(10):
        cars.append(merge(car1, car2, 0.05, 0, 0, 0.1, 0.1))
    for i in range(10):
        cars.append(merge(car1, car2, 0.5, 0.05, 0.05, 0.05, 0.05))
    for i in range(10):
        cars.append(merge(car1, car2,
                          np.random.rand(),
                          np.random.rand(),
                          np.random.rand(),
                          np.random.rand(),
                          np.random.rand()))
    for i in range(10):
        cars.append(Car())
    cars.append(car1)
    cars.append(car2)
    car1.img.fill((0, 0, 0))
    car2.img.fill((0, 0, 0))
    refresh()


def generate_cars():
    global cars
    cars = []
    for i in range(100):
        cars.append(Car())
