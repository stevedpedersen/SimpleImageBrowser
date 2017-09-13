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
		(self.label1,self.label2,self.label3,self.label4,self.label5) = [QLabel(self),QLabel(self),QLabel(self),QLabel(self),QLabel(self)]

		self.initUI()		
 
	def initUI(self):
		# window
		self.setWindowTitle(self.title)
		self.setGeometry(0, 0, self.width, self.height)
		self.initImages(self.files)
		self.draw(mode=0, index=0) # thumb mode & 1st image
		self.show()

	def initImages(self, files):
		thumbs = []
		fulls = []
		for f in files:		
			thumb = self.resizeAndFrame('data/' + f, self.thumbW, self.thumbH, self.thumbB)
			full = self.resizeAndFrame('data/' + f, self.fullW, self.fullH, self.fullB)
			thumbs.append(thumb)
			fulls.append(full)

		# self.images.append(cycle(thumbs))
		# self.images.append(cycle(fulls))
		self.images.append(thumbs)
		self.images.append(fulls)
		# self.images[0] = cycle(self.images[0])
		# self.images[1] = cycle(self.images[1])

	def resizeAndFrame(self, filename, w, h, b):		
		pixmap = QPixmap(filename)
		# scale image to width or height based on image orientation
		pixmap = pixmap.scaledToWidth(w - 2*b).scaledToHeight(h - 2*b)

		# if pixmap.width() > pixmap.height():
		# 	pixmap = pixmap.scaledToWidth(w - 2*b)
		# 	pixmap = pixmap.scaledToHeight(h - 2*b)
		# 	# setAlignment(Qt::Alignment)
		# else:
		# 	pixmap = pixmap.scaledToHeight(h - 2*b)
		# 	# setAlignment(Qt::Alignment)

		return pixmap

	def draw(self, mode, index):
		if mode == 0:
			y = 100
			self.label1.setPixmap(self.images[0][index])
			self.label1.setAlignment(Qt.AlignCenter) # 40+0*self.thumbW
			self.label1.setGeometry(QRect(40+0*self.thumbW, y, self.thumbW, self.thumbH))
			self.label1.setStyleSheet('border: ' + str(self.thumbB) + 'px solid green')
			
			self.label2.setPixmap(self.images[0][index+1])
			self.label2.setAlignment(Qt.AlignCenter) # 40+0*self.thumbW
			self.label2.setGeometry(QRect(40+1*self.thumbW, y, self.thumbW, self.thumbH))
			self.label2.setStyleSheet('border: ' + str(self.thumbB) + 'px solid green')
			
			self.label3.setPixmap(self.images[0][index+2])
			self.label3.setAlignment(Qt.AlignCenter) # 40+0*self.thumbW
			self.label3.setGeometry(QRect(40+2*self.thumbW, y, self.thumbW, self.thumbH))
			self.label3.setStyleSheet('border: ' + str(self.thumbB) + 'px solid green')
			
			self.label4.setPixmap(self.images[0][index+3])
			self.label4.setAlignment(Qt.AlignCenter) # 40+0*self.thumbW
			self.label4.setGeometry(QRect(40+3*self.thumbW, y, self.thumbW, self.thumbH))
			self.label4.setStyleSheet('border: ' + str(self.thumbB) + 'px solid green')
			
			self.label5.setPixmap(self.images[0][index+4])
			self.label5.setAlignment(Qt.AlignCenter) # 40+0*self.thumbW
			self.label5.setGeometry(QRect(40+4*self.thumbW, y, self.thumbW, self.thumbH))
			self.label5.setStyleSheet('border: ' + str(self.thumbB) + 'px solid green')

		elif mode == 1:
			print('cheese')
			# self.label.setStyleSheet('border: ' + str(self.thumbB) + 'px solid green')
			# self.label.setPixmap(self.images[mode][index])



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