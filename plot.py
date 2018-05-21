import matplotlib.pyplot as plt

def get_data(fn):
	f = open(fn);
	step = [];
	acc = []
	for line in f:
		l = line.split(' ')
		if len(l) != 3:
			print 'error'
		acc.append(l[2].astype(int))
		cur_steps = l[0].split('/')[:-1]
		step.append(cur_steps.astype(int))
	return step, acc

def plt(step, acc):
	plt(step, acc)

if __name__ == '__main__':
	step, acc = get_data('.log/ground_supervised_realGrounder.log ')
	plt(step, acc)

