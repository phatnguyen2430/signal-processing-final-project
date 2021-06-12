from app.service.filterService import FilterService
from app.service.fourierService import FourierService
import numpy as np
import uuid
from PIL import Image
import base64
from io import BytesIO

def readb64(uri):
   encoded_data = uri.split(',')[1]
   nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
   buf = BytesIO(nparr)
   img = Image.open(buf)
   return img


class ImageObject:
    key = None
    label = None
    image = None

    def __init__(self, label, image):
        self.key = uuid.uuid4()
        self.label = label
        self.image = Image.fromarray(image)

class ImageProcess:
    image = None
    gray_image = None
    mask_filter = None
    scale_value = None
    image_shape = (1, 1)
    filterService = FilterService()
    fourierService = FourierService()
    def __init__(self, image, scale_value=30):

        self.scale_value = int(image.size[0]/3)
        self.image = np.asarray(image.convert('RGB'))
        self.gray_image = np.array(image.convert("L"))
        self.image_shape = self.gray_image.shape
        # import filter service
        self.mask_filter = self.filterService.idealHP(
            scale_value, self.image_shape)

    # setup filter
    def set_filter(self, mask_type="IDEAL", filter_type="HIGH", scale_out=30, scale_in=20, n=20):
        if mask_type == "IDEAL":
            if filter_type == "HIGH":
                self.mask_filter = self.filterService.idealHP(
                    scale_out, self.image_shape)
            elif filter_type == "LOW":
                self.mask_filter = self.filterService.idealLP(
                    scale_out, self.image_shape)
            elif filter_type == "BAND":
                self.mask_filter = self.filterService.idealBP(
                    scale_in, scale_out, self.image_shape)
        elif mask_type == "BUTTERWORTH":
            if filter_type == "HIGH":
                self.mask_filter = self.filterService.butterworthHP(
                    scale_out, self.image_shape, n)
            elif filter_type == "LOW":
                self.mask_filter = self.filterService.butterworthLP(
                    scale_out, self.image_shape, n)
        elif mask_type == "GAUSSIAN":
            if filter_type == "HIGH":
                self.mask_filter = self.filterService.gaussianHP(
                    scale_out, self.image_shape)
            elif filter_type == "LOW":
                self.mask_filter = self.filterService.gaussianLP(
                    scale_out, self.image_shape)

    def bit_8_image_edge(self):
        # convert image to gray image
        converted_image_gray = self.fourierService.convertImageColor(
            self.image)
        saved_image_gray = ImageObject("Gray image", self.convertToRGB(converted_image_gray,"GRAY"))

        # make fourier spectrum 
        gray_spectrum = self.fourierService.ImageToFFT(converted_image_gray)
        saved_spectrum = ImageObject(
            "Fourier spectrum", self.convertToRGB(self.fourierService.toImage(gray_spectrum),"GRAY"))

        # make convert fourier spectrum out to center 
        center_gray_spectrum = self.fourierService.centerSpectrum(
            gray_spectrum)
        saved_center_spectrum = ImageObject(
            "Fourier center spectrum", self.convertToRGB(self.fourierService.toImage(center_gray_spectrum),"GRAY"))
        # multiple center fourier spectrum  with filter : y(x,y) = f(x,y)*h(x,y) => h is filter
        filtered_spectrum = center_gray_spectrum * self.mask_filter
        filtered_spectrum_image = ImageObject(
            "Fourier spectrum with mask", self.convertToRGB(self.fourierService.toImage(filtered_spectrum),"GRAY"))


        # convert filter image => inverse center filtered spectrum to outer filtered spectrum and use log to cover value to real image
        filtered_image = self.fourierService.fftToImage(
            self.fourierService.inverseSpectrum(filtered_spectrum))
        converted_image = ImageObject(
            "Filtered Image", self.convertToRGB(self.fourierService.toImage(filtered_image),"GRAY"))


        # # concatenate image to create image and save
        # concatenate_image = self.fourierService.toImage(np.dstack((filtered_image, filtered_image, filtered_image)))
        # final_image = ImageObject(
        #     "Final image", self.convertToRGB(concatenate_image,"RGB"))

            # result
        returnObject = [
                        [saved_image_gray], 
                        [saved_spectrum],
                        [saved_center_spectrum], 
                        [filtered_spectrum_image], 
                        [converted_image], 
                        [converted_image]
                    ]
        return returnObject

    def bit_24_image_edge(self):

        #convert section
        # convert image to red image to filter channel red
        converted_image_red = self.fourierService.convertImageColor(
            self.image, "RED")
        saved_image_red = ImageObject(
            "Red image", self.convertToRGB(converted_image_red, "RED"))
        # convert image to green image to filter channel green
        converted_image_green = self.fourierService.convertImageColor(
            self.image, "GREEN")
        saved_image_green = ImageObject(
            "Green image", self.convertToRGB(converted_image_green, "GREEN"))
        # convert image to blue image to filter channel blue
        converted_image_blue = self.fourierService.convertImageColor(
            self.image, "BLUE")
        saved_image_blue = ImageObject(
            "Blue image", self.convertToRGB(converted_image_blue, "BLUE"))
        #end convert section

        #convert to fourier spectrum 
        red_spectrum = self.fourierService.ImageToFFT(converted_image_red)
        saved_red_spectrum = ImageObject(
            "Fourier red spectrum", self.convertToRGB(self.fourierService.toImage(red_spectrum), "RED"))

        green_spectrum = self.fourierService.ImageToFFT(converted_image_green)
        saved_green_spectrum = ImageObject(
            "Fourier green spectrum", self.convertToRGB(self.fourierService.toImage(green_spectrum), "GREEN"))

        blue_spectrum = self.fourierService.ImageToFFT(converted_image_blue)
        saved_blue_spectrum = ImageObject(
            "Fourier blue spectrum", self.convertToRGB(self.fourierService.toImage(blue_spectrum), "BLUE"))
        #end convert to fourier spectrum 

        #convert to center fourier spectrum
        center_red_spectrum = self.fourierService.centerSpectrum(red_spectrum)
        saved_center_red_spectrum = ImageObject("Fourier centered red spectrum",
                                                self.convertToRGB(self.fourierService.toImage(center_red_spectrum), "RED"))
        center_green_spectrum = self.fourierService.centerSpectrum(
            green_spectrum)
        saved_center_green_spectrum = ImageObject("Fourier centered green spectrum",
                                                  self.convertToRGB(self.fourierService.toImage(center_green_spectrum), "GREEN"))

        center_blue_spectrum = self.fourierService.centerSpectrum(
            blue_spectrum)
        saved_center_blue_spectrum = ImageObject("Fourier centered blue spectrum",
                                                 self.convertToRGB(self.fourierService.toImage(center_blue_spectrum), "BLUE"))
        #end convert to center fourier spectrum


        
        # multiple center fourier spectrum  with filter : y(x,y) = f(x,y)*h(x,y) => h is filter
        mask_red = center_red_spectrum * self.mask_filter
        masked_red_spectrum = ImageObject("Masked red spectrum",
                                          self.convertToRGB(self.fourierService.toImage(mask_red), "RED"))

        mask_green = center_green_spectrum * self.mask_filter
        masked_green_spectrum = ImageObject("Masked green spectrum",
                                            self.convertToRGB(self.fourierService.toImage(mask_green), "GREEN"))

        mask_blue = center_blue_spectrum * self.mask_filter
        masked_blue_spectrum = ImageObject("Masked blue spectrum",
                                           self.convertToRGB(self.fourierService.toImage(mask_blue), "BLUE"))
        # end multiple



        # convert to image when filtered per channel
        red_image = self.fourierService.fftToImage(
            self.fourierService.inverseSpectrum(mask_red))
        filtered_red_image = ImageObject("Filtered Red Image",
                                         self.convertToRGB(self.fourierService.toImage(red_image), "RED"))

        green_image = self.fourierService.fftToImage(
            self.fourierService.inverseSpectrum(mask_green))
        filtered_green_image = ImageObject("Filtered Green Image",
                                           self.convertToRGB(self.fourierService.toImage(green_image), "GREEN"))

        blue_image = self.fourierService.fftToImage(
            self.fourierService.inverseSpectrum(mask_blue))
        filtered_blue_image = ImageObject("Filtered Blue Image",
                                          self.convertToRGB(self.fourierService.toImage(blue_image), "BLUE"))
        #end convert to image when filtered per channel

        # concatenate and map color image with each channel
        concatenate_image = np.dstack((red_image, green_image, blue_image))
        concatenate_image = self.fourierService.toImage(concatenate_image)

        saved_image = ImageObject(
            "Final image", self.convertToRGB(concatenate_image, "RGB"))


        # result
        returnObject = [
            [saved_image_red, saved_image_green, saved_image_blue],
            [saved_red_spectrum, saved_green_spectrum, saved_blue_spectrum],
            [saved_center_red_spectrum, saved_center_green_spectrum,
                saved_center_blue_spectrum],
            [masked_red_spectrum, masked_green_spectrum, masked_blue_spectrum],
            [filtered_red_image, filtered_green_image, filtered_blue_image],
            [saved_image]
        ]
        return returnObject

    def convertToRGB(self, array, type_convert):
        tempImage = np.zeros(self.image.shape, "uint8")
        divide_factor = (int(256 / (np.amax(array) + 1))) # divide_factor is number to convert [0..1] or [0..10] to [0..256] color code

        if type_convert == "RED":
            tempImage[:, :, 0] = (array*divide_factor).astype(int)
        elif type_convert == "GREEN":
            tempImage[:, :, 1] = (array*divide_factor).astype(int)
        elif type_convert == "BLUE":
            tempImage[:, :, 2] = (array*divide_factor).astype(int)
        elif type_convert == "GRAY":
            tempImage = np.zeros(self.gray_image.shape, "uint8")
            putArr = (array*divide_factor).astype(int)
            tempImage[:,:] = putArr
        elif type_convert == "RGB":
            array = (array * 255).astype(np.uint8)
            if len(array.shape) == len(self.image.shape):
                tempImage = array
        return tempImage


class MainService:
    def bit_8_image(self,filter_image,filter_mask_type="IDEAL",filter_mask_filter_type="HIGH",filter_scale_out=100,filter_scale_in=50,n = 20):
        image = readb64(filter_image)
        imageprocess = ImageProcess(image)
        imageprocess.set_filter(mask_type=filter_mask_type, scale_out=filter_scale_out)
        listReturn = imageprocess.bit_8_image_edge()
        return listReturn
    def bit_24_image(self,filter_image,filter_mask_type="IDEAL",filter_mask_filter_type="HIGH",filter_scale_out=100,filter_scale_in=50,n = 20):
        image = readb64(filter_image)
        imageprocess = ImageProcess(image)
        imageprocess.set_filter(mask_type=filter_mask_type, scale_out=filter_scale_out)
        listReturn = imageprocess.bit_24_image_edge()
        return listReturn