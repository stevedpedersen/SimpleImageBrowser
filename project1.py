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
from itertools import cycle
from PyQt5.QtCore import Qt, QRect
 
class ImageBrowser(QWidget):
 
	def __init__(self, files):
		super().__init__()
		self.title = 'Project 1 - Simple Image Browser'
		(self.width, self.height) = [800, 600]
		(self.thumbW, self.thumbH, self.thumbB) = [144, 100, 5]
		(self.fullW, self.fullH, self.fullB) = [720, 540, 20]		
		self.files = files
		self.images = []
		self.labels = [QLabel(self),QLabel(self),QLabel(self),QLabel(self),QLabel(self),QLabel(self)]

		self.initUI()		
 
	def initUI(self):
		# window
		self.setWindowTitle(self.title)
		self.setGeometry(0, 0, self.width, self.height)
		self.initImages(self.files)
		self.draw(1, 14) # thumb mode & 1st image
		self.show()

	def initImages(self, files):
		thumbs = []
		fulls = []
		for f in files:		
			thumb = self.resizeAndFrame('data/' + f, self.thumbW, self.thumbH, self.thumbB)
			full = self.resizeAndFrame('data/' + f, self.fullW, self.fullH, self.fullB)
			thumbs.append(thumb)
			fulls.append(full)

		self.images.append(thumbs)
		self.images.append(fulls)
		# self.images[0] = cycle(self.images[0])
		# self.images[1] = cycle(self.images[1])

	def resizeAndFrame(self, filename, w, h, b):		
		pixmap = QPixmap(filename)
		# scale image to width or height based on image orientation	
		if pixmap.width() > pixmap.height():
			pixmap = pixmap.scaledToWidth(w - 2*b)
			if pixmap.height() > (h - 2*b):
				pixmap = pixmap.scaledToHeight(h - 2*b)
		else:
			pixmap = pixmap.scaledToHeight(h - 2*b)

		return pixmap

	def draw(self, mode, LIndex, selected = -1):
		if selected == -1:
			selected = LIndex
		
		if mode == 0:
			y = 100
			for i in range(5):			
				thumb = LIndex+i if (LIndex+i < len(self.files)) else abs(len(self.files) - LIndex-i)
				color = 'green'
				if thumb == selected:
					color = 'red'					
				self.labels[i].setPixmap(self.images[mode][thumb])
				self.labels[i].setAlignment(Qt.AlignCenter)
				self.labels[i].setGeometry(QRect(40+i*self.thumbW, y, self.thumbW, self.thumbH))
				self.labels[i].setStyleSheet('border: ' + str(self.thumbB) + 'px solid '+ color)
				
		elif mode == 1:
			y = 30
			self.labels[5].setPixmap(self.images[mode][selected])
			self.labels[5].setAlignment(Qt.AlignCenter)
			self.labels[5].setGeometry(QRect(40, y, self.fullW, self.fullH))
			self.labels[5].setStyleSheet('border: ' + str(self.fullB) + 'px solid red')



if __name__ == '__main__':
	files = os.listdir('data')
	app = QApplication(sys.argv)
	imageBrowser = ImageBrowser(files)
	sys.exit(app.exec_())    
	
# NOTES: Circular list operations
# i = len(l) - 1
# jIndex = (i - 1) % len(l)
# kIndex = (i + 1) % len(l)

# j = l[jIndex]
# k = l[kIndex]

# Or, to be less verbose:

# k = l[(i + 1) % len(l)]

# note that if 0 <= i < len(l), then l[(i + 1) % len(l)] can also be written l[i - (len(l)-1)], avoiding the modulo.