from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import sqlalchemy as db
import math
from .util import *

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
    final_results = []
    if query == "":
        output_message = 'Search Cannot be Empty'
    elif not query:
        output_message = ''
    else:
        output_message = "Your search: " + query
        data = Shoe.query.filter(Shoe.price >= prices[0], Shoe.price <= prices[1])
        msgs = []
        treebank_tokenizer = TreebankWordTokenizer()
        if query_brand:
            data = data.filter(Shoe.brand == query_brand)
        for shoe in data:
            des_toks = treebank_tokenizer.tokenize(shoe.description.lower())
            msgs.append({
                'shoe_id': shoe.id,
                'toks': des_toks
            })
        inv_idx = build_inverted_index(msgs)
        idf = compute_idf(inv_idx, len(msgs))
        inv_idx = {key: val for key, val in inv_idx.items() if key in idf} 
        doc_norms = compute_doc_norms(inv_idx, idf, len(msgs))
        results = index_search(query, inv_idx, idf, doc_norms)

        
        for score, doc_id in results[:5]:
            shoe = data.filter(Shoe.id == msgs[doc_id]['shoe_id']).first()
            final_results.append((shoe.name, shoe.img_url, shoe.price, str(score)))

		# keywords = query.split()
		# for word in keywords:
		# 	word2 = '%{0}%'.format(word)
		# 	data_temp = data.filter(Shoe.description.ilike(word2))
		# 	if data_temp.first():
		# 		data = data_temp

		# for shoe in data:
		# 	results.append((shoe.name, shoe.img_url, shoe.price))

    print('Number returned results: ' + str(len(final_results)))
    print(query)
    print(output_message)
    return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=final_results[0:10])



