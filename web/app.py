from flask import Flask, render_template, request
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

@app.route('/product_details_1.html')
def get_prod_details1():
	return render_template('product_details_1.html')

@app.route('/product_details_2.html')
def get_prod_details2():
	return render_template('product_details_2.html')

@app.route('/product_details_3.html')
def get_prod_details3():
	return render_template('product_details_3.html')

@app.route('/product_details_4.html')
def get_prod_details4():
	return render_template('product_details_4.html')

@app.route('/product_details_5.html')
def get_prod_details5():
	return render_template('product_details_5.html')

@app.route('/product_details_6.html')
def get_prod_details6():
	return render_template('product_details_6.html')

@app.route('/product_details_7.html')
def get_prod_details7():
	return render_template('product_details_7.html')

@app.route('/product_details_8.html')
def get_prod_details8():
	return render_template('product_details_8.html')

@app.route('/product_details_9.html')
def get_prod_details9():
	return render_template('product_details_9.html')

@app.route('/product_details_10.html')
def get_prod_details10():
	return render_template('product_details_10.html')

@app.route('/product_details_11.html')
def get_prod_details11():
	return render_template('product_details_11.html')

@app.route('/product_details.html')
def get_prod_details():
	return render_template('product_details.html')

@app.route('/product_details.html', methods=['POST'])
def handle_data():
	question = request.form['question']
	productId = request.form['productId']
	category = request.form['category']
	reviews,sents = predict(productId, question, category)
	answer = gen_answer(question, sents, category)
	return render_template('product_details.html', reviews=reviews, sents=sents, answer=answer)

@app.route('/product_details_1.html', methods=['POST'])
def handle_data_1():
	question = request.form['question']
	productId = request.form['productId']
	category = request.form['category']
	reviews,sents = predict(productId, question, category)
	answer = gen_answer(question, sents, category)
	return render_template('product_details_1.html', reviews=reviews, sents=sents, answer=answer)

@app.route('/product_details_2.html', methods=['POST'])
def handle_data_2():
	question = request.form['question']
	productId = request.form['productId']
	category = request.form['category']
	reviews,sents = predict(productId, question, category)
	answer = gen_answer(question, sents, category)
	return render_template('product_details_2.html', reviews=reviews, sents=sents, answer=answer)

@app.route('/product_details_3.html', methods=['POST'])
def handle_data_3():
	question = request.form['question']
	productId = request.form['productId']
	category = request.form['category']
	reviews,sents = predict(productId, question, category)
	answer = gen_answer(question, sents, category)
	return render_template('product_details_3.html', reviews=reviews, sents=sents, answer=answer)

@app.route('/product_details_4.html', methods=['POST'])
def handle_data_4():
	question = request.form['question']
	productId = request.form['productId']
	category = request.form['category']
	reviews,sents = predict(productId, question, category)
	answer = gen_answer(question, sents, category)
	return render_template('product_details_4.html', reviews=reviews, sents=sents, answer=answer)

@app.route('/product_details_5.html', methods=['POST'])
def handle_data_5():
	question = request.form['question']
	productId = request.form['productId']
	category = request.form['category']
	reviews,sents = predict(productId, question, category)
	answer = gen_answer(question, sents, category)
	return render_template('product_details_5.html', reviews=reviews, sents=sents, answer=answer)

@app.route('/product_details_6.html', methods=['POST'])
def handle_data_6():
	question = request.form['question']
	productId = request.form['productId']
	category = request.form['category']
	reviews,sents = predict(productId, question, category)
	answer = gen_answer(question, sents, category)
	return render_template('product_details_6.html', reviews=reviews, sents=sents, answer=answer)

@app.route('/product_details_7.html', methods=['POST'])
def handle_data_7():
	question = request.form['question']
	productId = request.form['productId']
	category = request.form['category']
	reviews,sents = predict(productId, question, category)
	answer = gen_answer(question, sents, category)
	return render_template('product_details_7.html', reviews=reviews, sents=sents, answer=answer)

@app.route('/product_details_8.html', methods=['POST'])
def handle_data_8():
	question = request.form['question']
	productId = request.form['productId']
	category = request.form['category']
	reviews,sents = predict(productId, question, category)
	answer = gen_answer(question, sents, category)
	return render_template('product_details_8.html', reviews=reviews, sents=sents, answer=answer)

@app.route('/product_details_9.html', methods=['POST'])
def handle_data_9():
	question = request.form['question']
	productId = request.form['productId']
	category = request.form['category']
	reviews,sents = predict(productId, question, category)
	answer = gen_answer(question, sents, category)
	return render_template('product_details_9.html', reviews=reviews, sents=sents, answer=answer)


@app.route('/product_details_10.html', methods=['POST'])
def handle_data_10():
	question = request.form['question']
	productId = request.form['productId']
	category = request.form['category']
	reviews,sents = predict(productId, question, category)
	answer = gen_answer(question, sents, category)
	return render_template('product_details_10.html', reviews=reviews, sents=sents, answer=answer)

@app.route('/product_details_11.html', methods=['POST'])
def handle_data_11():
	question = request.form['question']
	productId = request.form['productId']
	category = request.form['category']
	reviews,sents = predict(productId, question, category)
	answer = gen_answer(question, sents, category)
	return render_template('product_details_11.html', reviews=reviews, sents=sents, answer=answer)

if __name__ == "__main__":
    app.run(debug=True)
