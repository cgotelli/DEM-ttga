import math
import matplotlib
from matplotlib.texmanager import TexManager
TexManager.font_info['lato'] = ('lato', r'\usepackage[default]{lato}\usepackage[T1]{fontenc}\usepackage[italic]{mathastext}')
from matplotlib import pyplot as plt
import matplotlib.ticker as mticker
import sys

xScale = yScale = 50
normalize = False

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

years = [sys.argv[1]]

print('$\\delta^L$ (m³)\tnetwork length (km)\tnetwork length (fraction of lowest path)')

volumes = []
lengths = []

for year in years:

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

	lengthSum = 0.0
	for persistence, coords in channels:
		if persistence < math.pow(10, 0):
			break
		lengthSum += pathLength(coords)
		if persistence == math.inf:
			lowestPathLength = lengthSum
		print(str(persistence) + '\t' + str(lengthSum / 1000) + '\t' + str(lengthSum / lowestPathLength))
		volumes.append(persistence)
		if normalize:
			lengths.append(lengthSum / lowestPathLength)
		else:
			lengths.append(lengthSum / 1000)

# make plot
plotColors = {
    "blue": (0.000, 0.400, 0.796),
    "green": (0.282, 0.557, 0.000),
    "yellow": (1.000, 0.604, 0.000),
    "red": (0.836, 0.000, 0.000)
}
plt.rc('text', usetex=True)
#plt.rcParams['text.latex.preamble'] = '\\usepackage{lmodern}'
plt.rcParams['figure.figsize'] = (3.5, 2.3)
#plt.rc('font', family='lmodern', size=9)
plt.rc('font', family='serif', serif='Lato', size=8)

plt.scatter(volumes, lengths, color=plotColors['blue'], s=10)

plt.xlabel('\\lato $\\delta^L$ (m$^3$)')
if normalize:
	plt.ylabel('\\lato network length\\\\(fraction of lowest path)')
	plt.ylim(0, 5.5)
	plt.axhline(1, color=plotColors['blue'], dashes=[2, 3], dash_capstyle='round', linewidth=1)
else:
	plt.ylabel('\\lato network length (km)')
	plt.ylim(100, 500)
	plt.yscale('log')
	ax = plt.gca()
	ax.get_yaxis().set_major_formatter(mticker.ScalarFormatter())
	ax.get_yaxis().set_minor_formatter(mticker.ScalarFormatter())
	plt.axhline(lowestPathLength / 1000, color=plotColors['blue'], dashes=[2, 3], dash_capstyle='round', linewidth=1)
	L = lambda delta: 1351 * math.pow(delta, -0.121)
	plt.plot([1e4, 10**8.0], [L(1e4), L(10**8.0)], color=plotColors['blue'], dashes=[2, 3], dash_capstyle='round', linewidth=1)
plt.xlim(math.pow(10, 4), math.pow(10, 8.0))
plt.xscale('log')
plt.tight_layout()

if normalize:
	plt.savefig('volume-vs-length-normalized/volume-vs-length-normalized-' + str(sys.argv[1]) + '.pdf')
else:
	plt.savefig('volume-vs-length/volume-vs-length-' + str(sys.argv[1]) + '.pdf')

