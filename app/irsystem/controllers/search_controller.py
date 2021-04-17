from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import sqlalchemy as db

project_name = "New kicks recommendation system"
net_id = "'Weihang Xiao(wx228), Brandon Guo(bhg39), Jennifer Zhou(jz547),  Jesse Zhu(jz626),  Joy Qi(hq38)'"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		data = range(5)
	inputs = [Shoe("shoe1", 19.99, 3.5, 'black', 'description1', 'cotton', )]

	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



