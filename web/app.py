from flask import Flask, render_template, request
from xyz import hello
from temp import get_reviews

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/product_details.html')
def get_prod_details():
	return render_template('product_details.html')

@app.route('/handle_data', methods=['POST'])
def handle_data():
	productId = request.form['productId']
	question = request.form['question']
	reviews = get_reviews(productId, question)
	return render_template('xyz.html', reviews=reviews)

@app.route('/xyz.html')
def hi():
    return render_template('xyz.html')

if __name__ == "__main__":
    app.run(debug=True)
