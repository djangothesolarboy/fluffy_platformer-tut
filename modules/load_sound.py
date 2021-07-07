import pygame,sys,os

def load_sound(name):
	"""makes it easy to load a sound;
	'assets'->folder name;
	'name'->file name;"""
	class NoneSound:
		def play(self): pass
	if not pygame.mixer:
		return NoneSound()
	fullname=os.path.join('assets/sounds',name)
	try:
		sound=pygame.mixer.Sound(fullname)
	except pygame.error as message:
		print('Cannot load sound:',fullname)
		raise SystemExit(message)
	return sound
