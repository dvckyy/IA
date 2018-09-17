import numpy as np
import math
import random
from PIL import Image, ImageChops

# APLICACION


class PuzzlePiece:
    # posicion de la pieza al momento de ordenarla segun su score
    solution_box = None
    # flag para saber si esta pieza ya encontro su lugar con certeza
    completed = False

    pyimage = None

    def __init__(self, box, route, image):
        self.box = box
        self.route = route
        self.image = image
        self.width, self.height = image.size
        self.x, self.y = box[0], box[1]


class PuzzleMap:
    PUZZLE_INIT = "puzzle_ini.png"
    PUZZLE_FINAL = "puzzle_final.png"
    PUZZLE_SLICE = "puzzle_%d.png"
    PUZZLE_SHUFFLED = "puzzle_shuffled.png"
    PUZZLE_SOLUTION = "puzzle_solution.png"
    # recordar que los slices son O(x^2) a.k.a. se pone lento mientras mas crece
    PUZZLE_SLICES = 8

    pieces = []

    flag_done = False
    iterations = 0

    def __init__(self, route, slices=None):
        self.route = route
        if slices is not None:
            self.PUZZLE_SLICES = slices
        self.cut(self.route)

    def invoke(self):
        self.cut(self.route)
        # while not self.flag_done:
        #    self.reorder()
        # for i in range(0, 100):
        #    self.reorder()
        #print('N ITERATIONS', self.iterations)

    def get_score(self, puzzle, shuffle):
        # diferencia de pixeles que posee la imagen del puzzle(posicion correcta) con la desordenada
        diff = ImageChops.difference(puzzle, shuffle)
        return int(np.array(diff).sum())

    def cut(self, route):
        # se realizan N cortes de la imagen, donde obtenemos las piezas y se guardan en los arrays
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

    def save_solution(self):
        # se guarda la solucion se tiene
        temp_solution = Image.new('RGB', (self.width, self.height))
        for i in range(0, len(self.pieces)):
            if self.pieces[i].solution_box is not None:
                temp_solution.paste(
                    self.pieces[i].image, self.pieces[i].solution_box)
        temp_solution.save(self.PUZZLE_SOLUTION, "PNG")

    def array_completed(self, flag):
        res = []
        for i in range(0, len(self.pieces)):
            if self.pieces[i].completed == flag:
                res.append(i)
        return res

    def reorder(self):
        # index de la pieza del puzzle que se quiere encontrar
        # se busca en el array de piezas que aun no estan completadas
        array_incomplete = self.array_completed(False)
        if(len(array_incomplete) == 0):
            self.flag_done = True
            return

        index = random.choice(array_incomplete)
        print(index)

        # se escoge una cantidad de piezas al azar
        size_sample = self.PUZZLE_SLICES
        if len(array_incomplete) < size_sample:
            size_sample = len(array_incomplete)

        print(array_incomplete)
        puzzle_samples = random.sample(array_incomplete, size_sample)

        best_score, best_index = np.inf, -1
        scores = []
        # se itera a travez del espacio de busqueda obteniendo el score de las piezas (menor score es mejor)
        for i in puzzle_samples:
            score = self.get_score(
                self.pieces[index].image, self.pieces[i].image)
            print('score', score)
            scores.append(score)
            if score < best_score:
                best_score, best_index = score, i

        print('best_score', best_score)
        print('best_index', best_index)
        #self.pieces[index].solution_box = self.pieces[best_index].box
        self.pieces[best_index].solution_box = self.pieces[index].box
        if best_score == 0:
            print('COMPLETED', best_index)
            #self.pieces[index].completed = True
            self.pieces[best_index].completed = True
        # self.save_solution()
        self.iterations += 1
        return puzzle_samples, scores, index, best_index


#test = PuzzleMap("imagen.png")
