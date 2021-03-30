# ron.py
import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity

from flask import Flask, render_template, request

app = Flask(__name__) 

# import and clean data 
df = pd.read_csv('scotch-final.csv')
df.index = df['NAME']

# create quick cosine similarity model
distances = cosine_similarity(df[df.columns[1:]])    
simdf = pd.DataFrame(data=distances,columns=df['NAME'],index=df.index)


def get_sim_scotch(name): 
	return simdf[name].sort_values(ascending=False)[1:6]


@app.route('/')
def index():
	return render_template('index.html',whiskeys=df['NAME'].values,recs={})

@app.route('/sims/<brand>')
def sims(brand):
	if brand in df['NAME']:
		results = get_sim_scotch(brand).to_dict()
	else: 
		results = {"":""}
	print(results)
	return render_template('index.html',whiskeys=df['NAME'].values, recs=results)


if __name__ == "__main__": 
	app.run(debug=True)