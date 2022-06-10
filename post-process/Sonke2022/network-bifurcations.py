import math
import matplotlib
from matplotlib.texmanager import TexManager
TexManager.font_info['lato'] = ('lato', r'\usepackage[default]{lato}\usepackage[T1]{fontenc}\usepackage[italic]{mathastext}')
from matplotlib import pyplot as plt
from collections import defaultdict

years = [1955, 1964, 1968, 1972, 1976, 1980, 1982, 1986, 1988, 1989, 1990, 1992, 1994]
years.extend(range(1996, 2016))

print('year\tbifurcations (striation 10⁶)\tbifurcations (striation 10⁷)\tbifurcations (striation 10⁸)\tbifurcations (striation 10⁹)\t' +
		'bifurcations (persistence 10⁴)\tbifurcations (persistence 10⁵)\tbifurcations (persistence 10⁶)\tbifurcations (persistence 10⁷)')

results = [[] for i in range(8)]

for year in years:

	output = str(year)
	result = []

	# striation
	for delta in [6, 7, 8, 9]:
		node_occurrence = defaultdict(int)
		with open('../output/striation-1e' + str(delta) + '/network-' + str(year) + '.txt') as network:
			num_vertices = int(next(network))
			for i in range(num_vertices):
				next(network)
			num_channels = int(next(network))
			for i in range(num_channels):
				channel = next(network).strip().split(' ')
				coords = channel[4:]
				coords = list(map(int, coords))
				coords = [(coords[i], coords[i + 1]) for i in range(0, len(coords), 2)]
				node_occurrence[(coords[0])] += 1
				node_occurrence[(coords[-1])] += 1

		count = 0
		for node in node_occurrence.keys():
			if node_occurrence[node] > 2:
				count += 1
		output += '\t' + str(count)
		results[delta - 6].append(count)

	# persistence
	for delta in [4, 5, 6, 7]:
		node_occurrence = defaultdict(int)
		with open('../output/persistence/network-' + str(year) + '.txt') as network:
			num_channels = int(next(network))
			for i in range(num_channels):
				channel = next(network).strip().split(' ')
				persistence = math.inf if channel[1] == 'inf' else float(channel[1])
				coords = channel[2:]
				coords = list(map(int, coords))
				coords = [(coords[i], coords[i + 1]) for i in range(0, len(coords), 2)]
				# don't include the lowest path in this computation, because
				# otherwise we would be counting the global source and sink even
				# if they have degree 1
				if not math.isinf(persistence) and persistence > math.pow(10, delta):
					node_occurrence[(coords[0])] += 1
					node_occurrence[(coords[-1])] += 1

		count = 0
		for node in node_occurrence.keys():
			if node_occurrence[node] > 0:
				count += 1
		output += '\t' + str(count)
		results[delta].append(count)

	# print result
	print(output)

# make plot
plotColors = {
    "blue": (0.000, 0.400, 0.796),
    "green": (0.282, 0.557, 0.000),
    "yellow": (1.000, 0.604, 0.000),
    "red": (0.836, 0.000, 0.000)
}
plt.rc('text',usetex=True)
plt.rcParams['text.latex.preamble'] = '\\usepackage{lmodern}'
plt.rcParams['figure.figsize'] = (4, 2.6)
plt.rc('font', family='serif', serif='Lato', size=8)
for i, result in enumerate(results):
	color = plotColors['red'] if i < 4 else plotColors['blue']
	plt.scatter(years, result, color=color, s=10, zorder=-i)
	plt.plot(years, result, color=color, zorder=-i)

plt.xlabel('\\lato year')
plt.ylabel('\\lato node count')
plt.xlim(1950, 2020)
plt.ylim(1, 1000)
plt.yscale('log')
plt.tight_layout()
plt.savefig('network-bifurcations.svg')

