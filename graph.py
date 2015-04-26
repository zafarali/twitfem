import plotly.plotly as pltly
from plotly.graph_objs import *
import math
import pandas as pd
import csv


data = pd.read_csv('loglikelihoods.csv')

positivedata = data[:10]
negativedata = data[-10:]
positivedata.sort(columns=['loglikely'], ascending=False, inplace = True )
negativedata.sort(columns=['loglikely'], ascending=False, inplace = True )

positive_words = positivedata['token'].values.tolist()
negative_words = negativedata['token'].values.tolist()
positive_values = positivedata['loglikely'].values.tolist()
negative_values = negativedata['loglikely'].values.tolist()

positive_words = [w.replace('u0001f602', '&#x1f602;') for w in positive_words]

num_words = int((len(positive_values)+len(negative_values))/2.0)

max_neg = float(min(negative_values))
max_pos = float(max(positive_values))

def pickColor(value, what='COLOR'):
	alphaChannel = math.fabs(value / max_pos if value > 0 else value / max_neg)
	if value > 0:
		hashcolor = 'rgba(68, 122, 219,%f)'%alphaChannel
	else:
		hashcolor = 'rgba(219, 90, 68,%f)'%alphaChannel
	return hashcolor



# print zip(positive_words, positive_values)
###### ------- PLOT 1  ------- ######
positive = Bar(
		y = positive_words,
		x = positive_values,
		marker = Marker(
				color = [ pickColor(i) for i in positive_values ]
			),
		orientation = 'h',
		yaxis='y'
	)
negative = Bar(
		y = negative_words,
		x = negative_values,
		marker=Marker(
			color = [ pickColor(i) for i in negative_values] 
		),
		orientation = 'h',
		xaxis = 'x',
		yaxis = 'y1'
	)

data = Data( [  negative, positive ] )

layout = Layout(
	title='Most Characteristic Words in Pro and Anti Feminist Tweets',
	showlegend=False,
	xaxis = XAxis(title='Log-Likelihood'),
	yaxis = YAxis(
			autorange='reversed',
			position=0.5,
			anchor='x',
		),
	yaxis1 = YAxis(
			autorange='reversed',
			position=0.4,
			anchor='x'
		)
	)

fig = Figure(data=data, layout=layout)
plot_url = pltly.plot(fig, filename='bdw-feminism')
