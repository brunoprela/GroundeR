import numpy as np

def load_file(fn):
	result = np.load(fn)
	print(result.shape)

if __name__ == '__main__':
	load_file('./feature/4944644486.npy')
