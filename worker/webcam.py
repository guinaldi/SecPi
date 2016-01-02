import pygame.camera
import pygame.image
import time
import logging

from tools.action import Action

class Webcam(Action):

	def __init__(self, id, params):
		super(Webcam, self).__init__(id, params)	

		try:
			self.path = params["path"]
			self.resolution = (int(params["resolution_x"]), int(params["resolution_y"]))
			self.data_path = params["data_path"]
		except ValueError, e: # if resolution can't be parsed as int
			logging.error("Webcam: Wasn't able to initialize the device, please check your configuration: %s" % e)
			return
		except KeyError, k: # if config parameters are missing in file
			logging.error("Webcam: Wasn't able to initialize the device, it seems there is a config parameter missing: %s" % k)
			return

		pygame.camera.init()
		self.cam = pygame.camera.Camera(self.path, self.resolution)
		logging.debug("Webcam: Video device initialized: %s" % self.path)

	# take a series of pictures within a given interval
	def take_adv_picture(self, num_of_pic, seconds_between):
		logging.debug("Webcam: Trying to take pictures")
		try:
			self.cam.start()
		except SystemError, e: # device path wrong
			logging.error("Webcam: Wasn't able to find video device at device path: %s" % self.path)
			return
		except AttributeError, a: # init failed, taking pictures won't work
			logging.error("Webcam: Couldn't take pictures because video device wasn't initialized properly")
			return

		try:
			for i in range(0,num_of_pic):
				img = self.cam.get_image()
				pygame.image.save(img, "%s/%s_%d.jpg" % (self.data_path, time.strftime("%Y%m%d_%H%M%S"), i))
				time.sleep(seconds_between)
		except Exception, e:
			logging.error("Webcam: Wasn't able to take pictures: %s" % e)

		self.cam.stop()
		logging.debug("Webcam: Finished taking pictures")

	
	def execute(self):
		self.take_adv_picture(int(self.params["count"]), int(self.params["interval"]))
		
	def cleanup(self):
		logging.debug("Webcam: No cleanup necessary at the moment")