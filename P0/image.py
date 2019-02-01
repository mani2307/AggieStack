from texttable import Texttable
import logging

class Image:

	def __init__(self):
		self.numOfImages=''
		self.imageDict={}

	def config (self, fileName):
		imageTempDict = {}
		with open(fileName) as f:
			for line in f:
				data = line.split()
				imgData = ImageData()
				if(len(data)>1):
					if(len(data)==2 and self.isValid(data)):
						imgData.image = data[0]
						imgData.location = data[1]
						imageTempDict[data[0]] = imgData
					else:
						print("data invalid, skipping file")
						logging.error('Data not proper, config not complete, Skipping file ...')
						return
				else:
					self.numOfImages=data[0]
		self.imageDict.update(imageTempDict)
		logging.info('SUCCESS')

	def isValid(self,data):
		return True

	def show(self):
		tempDataList = []
		tempDataList.append(['Image', 'Location'])
		for name, imageData in self.imageDict.items():
			tempList = []
			tempList.append(imageData.image)
			tempList.append(imageData.location)
			tempDataList.append(tempList)

		T = Texttable()
		T.add_rows(tempDataList)
		print (T.draw()) 
		logging.info('SUCCESS')

	def getImageDataSize(self):
		return len(self.imageDict)

class ImageData:
	"""docstring for ImageData"""
	def __init__(self):
		self.image = ""
		self.location = ""
		