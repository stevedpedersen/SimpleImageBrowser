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
	# when QLabel is clicked, emit a signal with an object param
	clicked = pyqtSignal(object)

	def __init__(self, parent):
		super().__init__(parent)
		self.pixIndex = 0
		self.labIndex = 0

	def mousePressEvent(self, event):
		# on click sends the object name to mouseSel()
		self.clicked.emit(self)

class ImageBrowser(QWidget):
 
	def __init__(self, files, windowWidth):
		super().__init__()
		self.title = 'Project 1 - Simple Image Browser'
		self.files = files
		self.setDimensions(windowWidth)
		self.h, self.i, self.j, self.mode = -1, 0, 1, 0
		self.images, self.labels = [], []
		for _ in range(6):
			self.labels.append(ClickableLabel(self))
		self.initUI()		

	# Scales everything that is displayed according to window width
	def setDimensions(self, windowWidth):
		self.width 	= int(windowWidth)
		self.height = int(3 * self.width / 4)
		self.thumbW = int(self.width / 6)
		self.thumbH = int(3 * self.thumbW / 4)
		self.thumbB = int(self.width / (self.thumbW * 0.75))
		self.fullW 	= int(self.width * 0.9)
		self.fullH	= int(3 * self.fullW / 4)
		self.fullB	= int(self.width / (self.thumbW * 0.25))

	# Display window in Thumbnail Mode with first image selected
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(0, 0, self.width, self.height)
		self.setStyleSheet('background-color: #B5B2C2;')
		self.initImages(self.files)
		self.draw(0, 0, 0) 
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
	def draw(self, mode, selected, centered = -1):
		if self.mode != mode:
			self.clearBrowser()
		self.mode = mode
		
		self.h = (selected - 1) % len(self.files)
		self.i = (selected) 	% len(self.files)
		self.j = (selected + 1) % len(self.files)

		# Thumbnail Mode
		if mode == 0:	
			y = self.height - (self.thumbH * 2) 
			for i in range(5):
				x = ((self.width - self.thumbW*5)/2) + i*self.thumbW
				# Center the highlighted thumbnail when returning from full screen mode
				if centered > 0:
					thumb = (centered + i) % len(self.files)
				else:
					thumb = (selected + i) % len(self.files)				
				color = '#A0C1D1'
				if thumb == selected:
					color = '#5A7D7C'	

				self.attachPixmap(thumb, i, x, y, self.thumbW, self.thumbH, self.thumbB, color)
		
		# Full Screen Mode		
		elif mode == 1:
			x = (self.width - self.fullW) / 2
			y = (self.height - self.fullH) / 2
			self.attachPixmap(selected, 5, x, y, self.fullW, self.fullH, self.fullB, '#5A7D7C')

	# Assigns an image to one of the labels
	def attachPixmap(self, pindex, lindex, x, y, w, h, b, color):
		mode = 0
		if lindex == 5:
			mode = 1
		self.labels[lindex].pixIndex = pindex
		self.labels[lindex].labIndex = lindex
		self.labels[lindex].setVisible(True)
		self.labels[lindex].setPixmap(self.images[mode][pindex])
		self.labels[lindex].setAlignment(Qt.AlignCenter)
		self.labels[lindex].setGeometry(QRect(x, y, w, h))
		self.labels[lindex].setStyleSheet('border: ' + str(b) + 'px solid '+ color+';')
		self.labels[lindex].clicked.connect(self.mouseSel)	

	def mouseSel(self, label):
		if self.mode == 0:
			self.draw(1, label.pixIndex)
	
	# Handles key events and responds according to current browser state
	def keyPressEvent(self, event):
		up = 16777235
		down = 16777237
		left = 16777234
		right = 16777236
		scrollL = 44
		scrollR = 46

		# Enter Full Screen Mode
		if self.mode == 0 	and event.key() == up:
			self.draw(1, self.i)
		# Exit Full Screen Mode			
		elif self.mode == 1 and event.key() == down:
			self.draw(0, self.i, (self.i - 2) % len(self.files))
		# Left - Full Screen
		elif self.mode == 1 and event.key() == left:
			self.draw(1, self.h)
		# Right - Full Screen		
		elif self.mode == 1 and event.key() == right:
			self.draw(1, self.j)
		# Left - Thumbnail
		elif self.mode == 0 and event.key() == left:
			self.draw(0, self.h)
		# Right - Thumbnail		
		elif self.mode == 0 and event.key() == right:
			self.draw(0, self.j)
		# Next set Left - Thumbnail		
		elif self.mode == 0 and event.key() == scrollL:
			nextIndex = (self.i - 5) % len(self.files)
			self.draw(0, nextIndex, nextIndex)
		# Next set Right - Thumbnail		
		elif self.mode == 0 and event.key() == scrollR:
			nextIndex = (self.i + 5) % len(self.files)
			self.draw(0, nextIndex, nextIndex)

	# Hide any visible contents on browser window
	def clearBrowser(self):
		for i in range(6):
			self.labels[i].setStyleSheet('border: none')
			self.labels[i].setVisible(False)

# Create an image browser from the images in the 'data' folder
if __name__ == '__main__':
	app = QApplication(sys.argv)
	width = sys.argv[1] if len(sys.argv) == 2 else 800
	imageBrowser = ImageBrowser(os.listdir('data'), width)
	sys.exit(app.exec_())    
	
