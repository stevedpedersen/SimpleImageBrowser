# File: project1.py
# By: Steve Pedersen
# Date: September 12, 2017
# Usage: python3 project1.py 
# System: OS X
# Dependencies: Python3, PyQt5
# Description: Creates an image browser that displays images as 
# 	thumbnails and fullscreen. Navigation with keys and mouse.


import os, sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from itertools import cycle
from PyQt5.QtCore import *


class ClickableLabel(QLabel):
	# when QLabel is clicked, emit a signal with a str parameter
	clicked = pyqtSignal(str)

	def __init(self, parent):
		super().__init__(parent)

	def mousePressEvent(self, event):
		# on click sends the object name to mouseSel()
		self.clicked.emit(self.objectName())

class ImageBrowser(QWidget):
 
	def __init__(self, files):
		super().__init__()
		self.title = 'Project 1 - Simple Image Browser'
		(self.width, self.height) = [800, 600]
		(self.thumbW, self.thumbH, self.thumbB) = [144, 100, 5]
		(self.fullW, self.fullH, self.fullB) = [720, 540, 20]	
		(self.h, self.i, self.j) = [-1, 0, 1]
		self.mode = 0
		self.files = files		
		self.images = []
		self.labels = [ClickableLabel(self),ClickableLabel(self),ClickableLabel(self),
			ClickableLabel(self), ClickableLabel(self),ClickableLabel(self)]
		self.initUI()		

	def initUI(self):
		# window
		self.setWindowTitle(self.title)
		self.setGeometry(0, 0, self.width, self.height)
		self.initImages(self.files)
		# Start off in Thumbnail Mode on the first image
		self.draw(0, 0) 
		self.show()

	# Populates a 2D List of Pixmaps with Thumbnail & Full versions of all images
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

	# Scale image to width or height based on image orientation	& label dimensions
	def resizeAndFrame(self, filename, w, h, b):		
		pixmap = QPixmap(filename)		
		if pixmap.width() > pixmap.height():
			pixmap = pixmap.scaledToWidth(w - 2*b)
			if pixmap.height() > (h - 2*b):
				pixmap = pixmap.scaledToHeight(h - 2*b)
		else:
			pixmap = pixmap.scaledToHeight(h - 2*b)

		return pixmap

	# Attach images to labels in thumbnail or fullscreen mode
	def draw(self, mode, LIndex, selected = -1):
		if selected == -1:
			selected = LIndex
		self.h = (selected - 1) % len(self.files)
		self.i = (selected) 	% len(self.files)
		self.j = (selected + 1) % len(self.files)
		self.mode = mode

		# Thumbnail Mode
		if mode == 0:
			self.clearBrowser()
			y = self.height - self.thumbH * 2 
			for i in range(5):	
				thumb = selected+i if (selected+i < len(self.files)) else abs(len(self.files) - selected-i)
				color = 'green'
				if thumb == selected:
					color = 'red'					
				self.labels[i].setPixmap(self.images[mode][thumb])
				self.labels[i].setAlignment(Qt.AlignCenter)
				self.labels[i].setGeometry(QRect(40+i*self.thumbW, y, self.thumbW, self.thumbH))
				self.labels[i].setStyleSheet('border: ' + str(self.thumbB) + 'px solid '+ color)
				self.labels[i].setObjectName('Label: {},\tMode: {}'.format(thumb, mode))
				self.labels[i].clicked.connect(self.mouseSel)
		
		# Full Screen Mode		
		elif mode == 1:
			self.clearBrowser()
			y = (self.height - self.fullH) / 2
			self.labels[5].setPixmap(self.images[mode][selected])
			self.labels[5].setAlignment(Qt.AlignCenter)
			self.labels[5].setGeometry(QRect(40, y, self.fullW, self.fullH))
			self.labels[5].setStyleSheet('border: ' + str(self.fullB) + 'px solid red')
			self.labels[5].setObjectName('Label: {},\tMode: {}'.format(selected, mode))
			self.labels[5].clicked.connect(self.mouseSel)
	
	# Handles key events and responds according to current browser state
	def keyPressEvent(self, event):
		up = 16777235
		down = 16777237
		left = 16777234
		right = 16777236
		if (self.mode == 0) and event.key() == up:
			self.draw(1, self.h-1, self.i)
		elif (self.mode == 1) and event.key() == down:
			self.draw(0, self.h-1, self.i)
		elif (self.mode == 1) and event.key() == left:
			self.draw(1, self.h-1, self.h)
		elif (self.mode == 1) and event.key() == right:
			self.draw(1, self.h-1, self.j)
		elif (self.mode == 0) and event.key() == left:
			self.draw(0, self.h, self.h)
		elif (self.mode == 0) and event.key() == right:
			self.draw(0, self.h, self.j)

	def mouseClickEvent(self, event):
		print(event)

	def mouseSel(self, name):
		print('"%s" clicked' % name)

	# Hide any visible contents on browser window
	def clearBrowser(self):
		for i in range(6):
			self.labels[i].setStyleSheet('border: none')
			self.labels[i].clear()

# Create an image browser from the images in the 'data' folder
if __name__ == '__main__':
	app = QApplication(sys.argv)
	imageBrowser = ImageBrowser(os.listdir('data'))
	sys.exit(app.exec_())    
	
