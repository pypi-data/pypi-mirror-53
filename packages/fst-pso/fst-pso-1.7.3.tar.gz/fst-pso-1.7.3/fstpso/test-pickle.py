import pickle

if __name__ == '__main__':

	g = open("bla", "rb")
	obj = pickle.load(g)
	print(obj._Solutions)
