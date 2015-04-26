import plotly.plotly as pltly
from plotly.graph_objs import *
import math
import pandas as pd
import csv

data = pd.read_csv('loglikelihoods.csv')
data2 = pd.read_csv('loglikelihoods_few_statuses.csv')

both = pd.merge(data, data2, how='inner', on='token')

# remove the two outliers
both = both.drop(both.index[:1])
both = both.drop(both.index[-1:])

x = both['loglikely_x'].tolist()
y = both['loglikely_y'].tolist()
scat_text = both['token'].tolist()

positivedata = data[:20]
negativedata = data[-20:]

positive_words = positivedata['token'].values.tolist()
negative_words = negativedata['token'].values.tolist()
positive_values = positivedata['loglikely'].values.tolist()
negative_values = negativedata['loglikely'].values.tolist()

positive_words = [w.replace('u0001f602', '&#x1f602;') for w in positive_words]

num_words = int((len(positive_values)+len(negative_values))/2.0)

max_neg = float(min(negative_values))
max_pos = float(max(positive_values))

def pickAlpha(value):
	alphaChannel = math.fabs(value / max_pos if value > 0 else value / max_neg)
	# return alphaChannel
	return 0.5


# print zip(positive_words, positive_values)
###### ------- PLOT 1  ------- ######

trace1 = Scatter(
	x=x,
	y=y,
	text=scat_text,
	mode='markers',
	marker=Marker(
    opacity=[pickAlpha(i) for i in x]
   )
	)

data = Data( [  trace1 ] )

layout = Layout(
	title='Low Activity Accounts vs All Accounts',
	showlegend=False,
	annotations=Annotations([
        Annotation(
            x=-13441.173828122865,
            y=-601.5201578504234,
            xref='x',
            yref='y',
            text='&#x1f602;',
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40
        )
    ]),
	xaxis = XAxis(title='All Accounts'),
	yaxis = YAxis(title='Low Activity'),

	)

fig = Figure(data=data, layout=layout)
plot_url = pltly.plot(fig, filename='bdw-feminism2')
