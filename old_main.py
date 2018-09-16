import numpy as np
import math
import random
from PIL import Image, ImageChops
# EJEMPLO MANEJO IMAGENES
opciones = {"ruta_imagen": "C:\\Users\\Sute\\Pictures\\1516934130375.png",
            "iteraciones": 100}


# APLICACION
class PuzzlePiece:
    solution_box = None
    completed = False

    def __init__(self, box, route, image):
        self.box = box
        self.route = route
        self.image = image


class Coordinate:
    score = 0
    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "x : %d, y : %d" % (self.x, self.y)


class PuzzleMap:
    PUZZLE_INIT = "puzzle_ini.png"
    PUZZLE_FINAL = "puzzle_final.png"
    PUZZLE_SLICE = "puzzle_%d.png"
    PUZZLE_SHUFFLED = "puzzle_shuffled.png"
    PUZZLE_SOLUTION = "puzzle_solution.png"
    # recordar que los slices son O(x^2) a.k.a. se pone lento
    PUZZLE_SLICES = 4

    pieces = []
    shuffled = []
    coordinates = []
    solution = []

    flag_done = False

    def __init__(self, route):
        self.route = route
        self.invoke()

    def invoke(self):
        self.cut(self.route)
        self.shuffle2()
        # while not self.flag_done:
        #    self.reorder()

        for i in range(0, 20):
            self.reorder()

    def get_score(self, puzzle, shuffle):
        diff = ImageChops.difference(puzzle, shuffle)
        return int(np.array(diff).sum())

    def cut(self, route):
        k = 0
        im = Image.open(route)
        imgwidth, imgheight = im.size
        self.width = imgwidth
        self.height = imgheight
        im, width, height = self.initial_cut(im, imgwidth, imgheight)
        for i in range(0, height*self.PUZZLE_SLICES, height):
            for j in range(0, width*self.PUZZLE_SLICES, width):
                box = (j, i, j+width, i+height)
                a = im.crop(box)
                try:
                    puzzle_route = self.PUZZLE_SLICE % k
                    a.save(puzzle_route, "PNG")
                except:
                    print("ERROR CUTTING PUZZLE")
                    pass
                piece = PuzzlePiece(
                    box, puzzle_route, a)
                self.coordinates.append(box)
                # print(piece)
                self.pieces.append(piece)
                k += 1

    def initial_cut(self, img, imgwidth, imgheight):
        # Se corta la imagen en una imagen con dimensiones sin floats y se guarda el resultado puzzle_ini.png
        # Obtenemos las dimensiones de width y height luego de cortarlo por PUZZLE_SLICES
        width = math.floor(imgwidth / self.PUZZLE_SLICES)
        height = math.floor(imgheight / self.PUZZLE_SLICES)
        box = (0, 0, width*self.PUZZLE_SLICES, height * self.PUZZLE_SLICES)
        imgcrop = img.crop(box)
        imgcrop.save(self.PUZZLE_INIT, "PNG")
        return imgcrop, width, height

    def shuffle(self):
        # Se desordena el array de las piezas y se guarda en shuffled.png
        self.shuffled = self.pieces.copy()
        random.shuffle(self.shuffled)
        imgshuffled = Image.new('RGB', (self.width, self.height))
        for i in range(0, len(self.shuffled)):
            imgshuffled.paste(self.shuffled[i].image, self.coordinates[i])
        imgshuffled.save(self.PUZZLE_SHUFFLED, "PNG")

        # Creamos una imagen vacia para el puzzle ordenado
        temp_solution = Image.new('RGB', (self.width, self.height))
        temp_solution.save(self.PUZZLE_SOLUTION, "PNG")

    def shuffle2(self):
        # Se desordena el array de las piezas y se guarda en shuffled.png
        self.solution = self.pieces.copy()

    def save_solution_old(self):
        temp_solution = Image.new('RGB', (self.width, self.height))
        for i in range(0, len(self.solution)):
            if self.solution[i].solution_box is not None:
                temp_solution.paste(
                    self.solution[i].image, self.solution[i].solution_box)
        temp_solution.save(self.PUZZLE_SOLUTION, "PNG")

    def save_solution(self):
        temp_solution = Image.new('RGB', (self.width, self.height))
        for i in range(0, len(self.pieces)):
            if self.pieces[i].solution_box is not None:
                temp_solution.paste(
                    self.pieces[i].image, self.pieces[i].solution_box)
        temp_solution.save(self.PUZZLE_SOLUTION, "PNG")

    def array_solution(self):
        res = []
        for i in range(0, len(self.solution)):
            if self.solution[i].solution_box is not None:
                res.append(i)
        return res

    def array_completed(self, flag):
        res = []
        for i in range(0, len(self.solution)):
            if self.solution[i].completed == flag:
                res.append(i)
        return res

    def array_left(self):
        res = []
        for i in range(0, len(self.solution)):
            if self.solution[i].solution_box is None:
                res.append(i)
        return res

    def is_done(self):
        if len(self.coordinates) == 0:
            self.flag_done = True

    def reorder2(self):
        # index de la pieza del puzzle que se quiere encontrar
        index = random.randrange(0, len(self.coordinates))
        print(index)

        size_sample = self.PUZZLE_SLICES
        if len(self.pieces) < size_sample:
            size_sample = len(self.pieces)
        puzzle_samples = random.sample(self.pieces, size_sample)

        best_score, best_index = np.inf, -1
        # se itera a travez del espacio de busqueda obtenido el score de las piezas
        for i in range(0, len(puzzle_samples)):
            score = self.get_score(
                self.pieces[index].image, puzzle_samples[i].image)
            print('score', score)
            if score < best_score:
                best_score, best_index = score, i

        print('best_score', best_score)
        print('best_index', best_index)
        self.solution[index].solution_box = puzzle_samples[best_index].box
        if best_score == 0:
            del self.coordinates[index]
            del self.pieces[index]
        self.save_solution()

    def reorder(self):
        # index de la pieza del puzzle que se quiere encontrar
        array_incomplete = self.array_completed(False)
        if(len(array_incomplete) == 0):
            self.flag_done = True
            return

        index = random.choice(array_incomplete)
        print(index)

        size_sample = self.PUZZLE_SLICES
        if len(array_incomplete) < size_sample:
            size_sample = len(array_incomplete)
        puzzle_samples = random.sample(array_incomplete, size_sample)

        best_score, best_index = np.inf, -1
        # se itera a travez del espacio de busqueda obtenido el score de las piezas
        for i in puzzle_samples:
            score = self.get_score(
                self.pieces[index].image, self.pieces[i].image)
            print('score', score)
            if score < best_score:
                best_score, best_index = score, i

        print('best_score', best_score)
        print('best_index', best_index)
        self.pieces[index].solution_box = self.pieces[best_index].box
        if best_score == 0:
            print('COMPLETED', index)
            self.pieces[index].completed = True
        self.save_solution()


test = PuzzleMap("C:\\Users\\Sute\\Pictures\\1516934130375.png")
