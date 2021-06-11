from app import app
from flask import request, jsonify
from datetime import date
from app.service.mainService import MainService, ImageObject
from app.service.imageReturner import ReturnObject
from app.service.inputObject import InputObject

mainService = MainService()

@app.route('/', methods=["GET", "POST"])
def home():
   request_data = str(request.get_json())
   request_data = request_data.replace("\'", "\"")
   listImage = [[]]
   # if(string)
   # listImage = mainService.bit_8_image(stringbase64)
   input_data = InputObject.from_json(request_data)

   if input_data.bit_24:
      listImage = mainService.bit_24_image(filter_image=input_data.image, filter_mask_type=input_data.use_filter,
                                          filter_mask_filter_type=input_data.filter_type, filter_scale_out=input_data.scale_out, filter_scale_in=input_data.scale_in, n=input_data.n)
   else:
      listImage = mainService.bit_8_image(filter_image=input_data.image, filter_mask_type=input_data.use_filter,
                                            filter_mask_filter_type=input_data.filter_type, filter_scale_out=input_data.scale_out, filter_scale_in=input_data.scale_in, n=input_data.n)
   returnList = []
   for row in listImage:
      for item in row:
         tempObject = ReturnObject(item)
         returnList.append(tempObject.__dict__)

   objectReturn = {
      "time": str(date.today()),
      "data": returnList,
      "success": True
   }
   return jsonify(objectReturn)