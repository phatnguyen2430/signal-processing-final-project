import numpy as np
import math


class FilterService:
    # calculate distance of (x,y) to center of image => thus we know this point 
    def distance(self, point1, point2):
        return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)

    def idealLP(self, D0, imgShape):
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows/2, cols/2)
        for x in range(cols):
            for y in range(rows):
                if self.distance((y, x), center) <= D0:
                    base[y, x] = 1
        return base

    def idealHP(self, D0, imgShape):
        base = np.ones(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows/2, cols/2)
        for x in range(cols):
            for y in range(rows):
                if self.distance((y, x), center) <= D0:
                    base[y, x] = 0
        return base

    def idealBP(self, r_in, r_out, imgShape):
        base = np.ones(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows/2, cols/2)
        for x in range(cols):
            for y in range(rows):
                if self.distance((y, x), center) <= r_out and self.distance((y, x), center) >= r_in:
                    base[y, x] = 0
        return base


    def butterworthLP(self, D0, imgShape, n):
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows/2, cols/2)
        for x in range(cols):
            for y in range(rows):
                base[y, x] = 1/(1+(self.distance((y, x), center)/D0)**(2*n))
        return base

    def butterworthHP(self, D0, imgShape, n):
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows/2, cols/2)
        for x in range(cols):
            for y in range(rows):
                base[y, x] = 1-1/(1+(self.distance((y, x), center)/D0)**(2*n))
        return base

    def gaussianLP(self, D0, imgShape):
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows/2, cols/2)
        for x in range(cols):
            for y in range(rows):
                base[y, x] = math.exp(
                    ((-self.distance((y, x), center)**2)/(2*(D0**2))))
        return base

    def gaussianHP(self, D0, imgShape):
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows/2, cols/2)
        for x in range(cols):
            for y in range(rows):
                base[y, x] = 1 - \
                    math.exp(((-self.distance((y, x), center)**2)/(2*(D0**2))))
        return base
