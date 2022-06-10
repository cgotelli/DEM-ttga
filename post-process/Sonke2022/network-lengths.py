import math
import matplotlib
from matplotlib.texmanager import TexManager
TexManager.font_info['lato'] = ('lato', r'\usepackage[default]{lato}\usepackage[T1]{fontenc}\usepackage[italic]{mathastext}')
from matplotlib import pyplot as plt
import matplotlib.ticker as mticker

xScale = yScale = 50

def pathLength(coords):
	length = 0.0
	for i in range(len(coords) - 1):
		a = coords[i]
		b = coords[i + 1]

		if a[0] < 0 or b[0] < 0 or a[0] >= 966 or b[0] >= 966:
			# ignore virtual paths to source / sink
			continue

		dx = (a[0] - b[0]) * xScale
		dy = (a[1] - b[1]) * yScale
		length += math.sqrt(dx * dx + dy * dy)
	return length

years = [1955, 1964, 1968, 1972, 1976, 1980, 1982, 1986, 1988, 1989, 1990, 1992, 1994]
years.extend(range(1996, 2016))

print('year\tnetwork length (striation 10⁶)\tnetwork length (striation 10⁷)\tnetwork length (striation 10⁸)\tnetwork length (striation 10⁹)\t' +
		'network length (persistence 10⁴)\tnetwork length (persistence 10⁵)\tnetwork length (persistence 10⁶)\tnetwork length (persistence 10⁷)')

results = [[] for i in range(8)]

for year in years:

	output = str(year)
	result = []

	# striation
	for delta in [6, 7, 8, 9]:
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
				coords = [[coords[i], coords[i + 1]] for i in range(0, len(coords), 2)]
				channels.append(coords)

		striationLength = 0.0
		for coords in channels:
			striationLength += pathLength(coords)
		output += '\t' + str(round(striationLength) / 1000)
		results[delta - 6].append(striationLength / 1000)

	# persistence
	for delta in [4, 5, 6, 7]:
		with open('../output/persistence/network-' + str(year) + '.txt') as network:
			num_channels = int(next(network))
			channels = []
			for i in range(num_channels):
				channel = next(network).strip().split(' ')
				persistence = math.inf if channel[1] == 'inf' else float(channel[1])
				coords = channel[2:]
				coords = list(map(int, coords))
				coords = [[coords[i], coords[i + 1]] for i in range(0, len(coords), 2)]
				channels.append([persistence, coords])

		persistenceLength = 0.0
		for persistence, coords in channels:
			if persistence > math.pow(10, delta):
				persistenceLength += pathLength(coords)
		output += '\t' + str(round(persistenceLength) / 1000)
		results[delta].append(persistenceLength / 1000)

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
plt.ylabel('\\lato network length (km)')
plt.xlim(1950, 2020)
plt.ylim(100, 700)
plt.yscale('log')
ax = plt.gca()
ax.get_yaxis().set_major_formatter(mticker.ScalarFormatter())
ax.get_yaxis().set_minor_formatter(mticker.ScalarFormatter())
plt.tight_layout()
plt.savefig('network-lengths.svg')

