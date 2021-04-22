from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import sqlalchemy as db

project_name = "New kicks recommendation system"
net_id = "'Weihang Xiao(wx228), Brandon Guo(bhg39), Jennifer Zhou(jz547),  Jesse Zhu(jz626),  Joy Qi(hq38)'"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('keywords')
	query_brand = request.args.get('brand')
	query_price = request.args.get('price')
	if query_price:
		prices = [int(query_price.split('-')[0]), int(query_price.split('-')[1])]
	else:
		prices = [0, float('inf')]
	results = []
	if query == "":
		output_message = 'Search Cannot be Empty'
	elif not query:
		output_message = ''
	else:
		output_message = "Your search: " + query
		#looking_for = '%{0}%'.format(query)
		data = Shoe.query.filter(Shoe.brand == query_brand, Shoe.price >= prices[0], Shoe.price <= prices[1]) #, Shoe.description.ilike(looking_for))

		keywords = query.split()
		for word in keywords:
			word2 = '%{0}%'.format(word)
			data_temp = data.filter(Shoe.description.ilike(word2))
			if data_temp.first():
				data = data_temp

		for shoe in data:
			results.append((shoe.name, shoe.img_url, shoe.price))

	print('Number returned results: ' + str(len(results)))
	print(query)
	print(output_message)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=results[0:10])




