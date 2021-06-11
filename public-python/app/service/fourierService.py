import numpy as np


class FourierService:
    # channel (gray,red,green,blue) RGB
    def convertImageColor(self, image=None, channel="GRAY"):
        w, h, c = image.shape
        if c == 1:
            return Exception("Image null or image already gray")
        elif channel == "GRAY":
            image = (np.dot(image[...,:3], [0.2989, 0.5870, 0.1140])).astype(int)
        elif channel == "RED":
            image = image[:, :, 0]
        elif channel == "GREEN":
            image = image[:, :, 1]
        elif channel == "BLUE":
            image = image[:, :, 2]

        return image

    def ImageToFFT(self, image):
        return np.fft.fft2(image)

    def fftToImage(self, array):
        return np.fft.ifft2(array)

    def centerSpectrum(self, array=None):
        return np.fft.fftshift(array)

    def inverseSpectrum(self, array=None):
        return np.fft.ifftshift(array)

    def toImage(self, array):
        return np.log(1 + np.abs(array))
