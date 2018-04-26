from flask import Flask, render_template, request
from xyz import hello
from temp import get_reviews
from predict import predict, gen_answer

app = Flask(__name__)

@app.route('/index.html',)
def display_home():
	return render_template('index.html')

# @app.route('/index.html')
# def choose_prod():
# 	print(request)
# 	data = request.get_json()
# 	print("ADITYA: ", data)
# 	return render_template('product_details.html')

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/product_details.html')
def get_prod_details():
	return render_template('product_details.html')

@app.route('/product_details.html', methods=['POST'])
def handle_data():
	question = request.form['question']
	productId = request.form['productId']
	category = request.form['category']
	reviews,sents = predict(productId, question, category, 4)
	answer = 'yes . it has a phono cord that plugs in the amp .'#gen_answer(question, sents)
	print("HIIIII", answer)
	return render_template('product_details.html', reviews=reviews, sents=sents, answer=answer)

@app.route('/xyz.html')
def hi():
    return render_template('xyz.html')

if __name__ == "__main__":
    app.run(debug=True)
