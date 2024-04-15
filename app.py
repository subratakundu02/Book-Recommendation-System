from flask import Flask,render_template, request
import pickle
import numpy as np
import pandas as pd

# popularity_df = pickle.load(open('popular.pkl','rb'))
popularity_df = pd.read_csv('popularity.csv')
# popularity_df.reset_index(inplace=True)
pt = pd.compat.pickle_compat.load(open('pt.pkl','rb'))
# pt.reset_index(inplace=True)
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

books['Image-URL-S'] = books['Image-URL-S'].str.replace('http://','https://')

app = Flask(__name__)
@app.route('/')
def index():
      return render_template('index.html',
                             book_name = list(popularity_df['Book-Title'].values),
                             author = list(popularity_df['Book-Author'].values),
                             image = list(popularity_df['Image-URL-M'].values),
                             votes = list(popularity_df['num_ratings'].values),
                             rating = list(popularity_df['avg_ratings'].values),
                             )

@app.route('/recommend')
def recommend_ui():
      return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
      user_input = request.form.get('user_input')
      index=np.where(pt.index==user_input)[0][0]
      similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:5]
      data = []
      for i in similar_items:
            item = []
            temp_df=(books[books['Book-Title'] == pt.index[i[0]]])
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)
      # print(data)
      return render_template('recommend.html',data=data)
      return str(user_input)

if __name__ == '__main__':
      app.run(debug=True)