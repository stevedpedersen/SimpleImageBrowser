# File: project1.py
# By: Steve Pedersen
# Date: September 12, 2017
# Usage: python3 project1.py <w> <h> <b>
# 	<w> width, 
#	<h> height, 
#	<b> base, 
# System: OS X
# Description: Lists files, then resizes, frames and displays an 
#   image based on user args of Width, Height, Border, Image #


import os, sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
#from PyQt5.QtCore import Qt
 
class ImageBrowser(QWidget):
 
	def __init__(self, files):
		super().__init__()
		self.title = 'Project 1 - Simple Image Browser'
		self.width = 800
		self.height = 600
		self.thumbW = 140
		self.thumbB = 5
		self.fullW = 700
		self.fullB = 20
		self.files = files
		# self.images = [[None]*len(files) for _ in range(2)]
		self.thumbs = []
		self.fulls = []
		self.initUI()		
 
	def initUI(self):
		# window
		self.setWindowTitle(self.title)
		self.setGeometry(0, 0, self.width, self.height)
		self.initImages(self.files)
		self.draw(0, 0) # thumb mode & 1st image
		self.show()

	def initImages(self, files):
		thumbs = []
		fulls = []
		for f in files:		
			# print(f)
			thumbLabel = QLabel(self)
			fullLabel = QLabel(self)

			thumb = self.resizeAndFrame('data/' + f, thumbLabel, self.thumbW, self.thumbB)
			full = self.resizeAndFrame('data/' + f, fullLabel, self.fullW, self.fullB)
			thumbs.append(thumb)
			fulls.append(full)

		self.thumbs.append(thumbs)		
		self.fulls.append(fulls)


	def resizeAndFrame(self, filename, label, w, b):
		label.setStyleSheet('border: '+str(b)+'px solid green')
		pixmap = QPixmap(filename)

		# scale image to width or height based on image orientation
		if pixmap.width() > pixmap.height():
			pixmap = pixmap.scaledToWidth(pixmap.width() - 2*b)
			# print('1')
		else:
			pixmap = pixmap.scaledToHeight(pixmap.height() - 2*b)
			# print('2')	

		# align the image vertically or horizontally based on image orientation and label dimensions
		if pixmap.width() > pixmap.height():
			label.move(0, pixmap.height() / 2)
			# self.label.move(0, (h - 2*b - pixmap.height()) / 2)
			# self.label.move(0, (pixmap.height() - 2*b) / 2)
			# print('A')
		else:
			label.move(pixmap.width() / 2, 0)	
			# print('B')		

		# attach image to label
		label.setPixmap(pixmap)

		return label

	def draw(self, mode, index):
		self.label = self.fulls[mode][2]
		print(self.thumbs[mode][index])


if __name__ == '__main__':
	files = os.listdir('data')
	app = QApplication(sys.argv)
	imageBrowser = ImageBrowser(files)
	sys.exit(app.exec_())    
	
