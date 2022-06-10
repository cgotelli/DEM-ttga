import math
import sys

xScale = yScale = 50

for year in [int(sys.argv[1])]:

	print('<ipeselection pos="0 0">')

	# striation
	points_striation = {}
	for delta in [6, 7, 8, 9]:
		points_striation[delta] = set()
		with open('../output/striation-1e' + str(delta) + '/network-' + str(year) + '.txt') as network:
			num_vertices = int(next(network))
			for i in range(num_vertices):
				next(network)
			num_channels = int(next(network))
			channels = []
			for i in range(num_channels):
				channel = next(network).strip().split(' ')
				coords = channel[4:]
				coords = list(map(int, coords))
				coords = [(coords[i], coords[i + 1]) for i in range(0, len(coords), 2)]
				for c in coords:
					points_striation[delta].add(c)

	# persistence
	points_persistence = {}
	for delta in [4, 5, 6, 7]:
		points_persistence[delta] = set()
		with open('../output/persistence/network-' + str(year) + '.txt') as network:
			num_channels = int(next(network))
			channels = []
			for i in range(num_channels):
				channel = next(network).strip().split(' ')
				persistence = math.inf if channel[1] == 'inf' else float(channel[1])
				coords = channel[2:]
				coords = list(map(int, coords))
				coords = [(coords[i], coords[i + 1]) for i in range(0, len(coords), 2)]
				channels.append([persistence, coords])
				if persistence > math.pow(10, delta):
					for c in coords:
						points_persistence[delta].add(c)

	# print result
	for s_delta in [6, 7, 8, 9]:
		line = 'striation 10^' + str(s_delta)

		if s_delta < 9:
			s_set = points_striation[s_delta].difference(points_striation[s_delta + 1])
		else:
			s_set = points_striation[s_delta]

		for p_delta in [4, 5, 6, 7]:
			if p_delta < 7:
				p_set = points_persistence[p_delta].difference(points_persistence[p_delta + 1])
			else:
				p_set = points_persistence[p_delta]
			overlap = len(s_set.intersection(p_set))

			x = 16 * s_delta
			y = 16 * p_delta
			print('<path layer="alpha" stroke="black" fill="' + str(max(0, 1 - overlap / 3000)) + '" cap="1" join="1">')
			print(str(x) + ' ' + str(y + 16) + ' m')
			print(str(x) + ' ' + str(y) + ' l')
			print(str(x + 16) + ' ' + str(y) + ' l')
			print(str(x + 16) + ' ' + str(y + 16) + ' l')
			print('h')
			print('</path>')

	print('</ipeselection>')
