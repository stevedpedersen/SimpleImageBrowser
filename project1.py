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
 
	def __init__(self, files):
		super().__init__()
		self.title = 'Project 1 - Simple Image Browser'
		(self.width, self.height) = [800, 600]
		(self.thumbW, self.thumbH, self.thumbB) = [144, 100, 5]
		(self.fullW, self.fullH, self.fullB) = [720, 540, 20]	
		(self.h, self.i, self.j) = [-1, 0, 1]
		self.l = 0
		self.selectedLabel = 0
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
	def draw(self, mode, selected, l = -1, transition = 'none'):
		if self.mode != mode:
			self.clearBrowser()
		self.mode = mode
		
		self.h = (selected - 1) % len(self.files)
		self.i = (selected) 	% len(self.files)
		self.j = (selected + 1) % len(self.files)

		# Thumbnail Mode
		if mode == 0:	
			y = self.height - self.thumbH * 2 
			for i in range(5):
				x = ((self.width - self.thumbW*5)/2) + i*self.thumbW
				# Center the highlighted thumbnail when returning from full screen mode
				if l > 0:
					self.l = l
					thumb = (l + i) % len(self.files)
					self.selectedLabel = i
				else:
					thumb = (selected + i) % len(self.files)
					self.selectedLabel = i					
				color = 'green'
				if thumb == selected:
					color = 'red'	

				self.attachPixmap(thumb, i, x, y, self.thumbW, self.thumbH, self.thumbB, color)
		
		# Full Screen Mode		
		elif mode == 1:
			x = (self.width - self.fullW) / 2
			y = (self.height - self.fullH) / 2
			self.attachPixmap(selected, 5, x, y, self.fullW, self.fullH, self.fullB, 'red')

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
		self.labels[lindex].repaint(QRect(x+5, y, w+5, h))		

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
		elif self.mode == 0 and event.key() == left:	# TODO: Update self.l on move, transition
			self.draw(0, self.h)
		# Right - Thumbnail		
		elif self.mode == 0 and event.key() == right:	# TODO: Update self.l on move, transition
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
	imageBrowser = ImageBrowser(os.listdir('data'))
	sys.exit(app.exec_())    
	
