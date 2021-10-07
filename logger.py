import logging
import os


class Logging:
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	def __init__(self, name, level, text):
		self.logger = logging.getLogger(name)
		self.lvl = level
		self.text = text

		# self.logger.setLevel(f'logging.{self.level}')

	@property
	def level(self):
		if self.lvl == 'INFO':
			self.logger.setLevel(logging.INFO)
			return self.logger.info(self.text)
		elif self.lvl == 'DEBUG':
			self.logger.setLevel(logging.DEBUG)
			return self.logger.debug(self.text)

	@property
	def file_handler(self):
		path =  os.path.join(os.getcwd(), 'output_mcu', self.logger.name)
		file_handl = logging.FileHandler(path)
		self.logger.addHandler(file_handl)
		file_handl.setFormatter(self.formatter)
		print('called')
		return self.level

# logger = logging.getLogger(__name__)
# PATH = os.path.join(os.getcwd(), 'output_mcu', logger.name)
# logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)
# file_str = logging.FileHandler(PATH)
# logger.addHandler(file_str)

# file_str.setFormatter(formatter)