from wsgiref.simple_server import make_server
from cgi import parse_qs, escape
import json
import pickle

#load_stored_score_board
f = open('score_data.dat', 'rb')
score_board = pickle.load(f)
f.close()


#Ex) 192.168.200.142/?id=test& score=300& signal=1
def application(environ, start_response):
	d = parse_qs(environ['QUERY_STRING'])

	user_id = escape(d.get('id', [''])[0])
	user_score = int(escape(d.get('score', [''])[0]))
	signal = int(escape(d.get('signal', [''])[0]))
	code = 0 #default value


	#id dupliation check
	if signal == 1:
		if user_id in score_board:
			code = 'T' #True duplication
			response_body = json.dumps({'ID': user_id, 'SCORE': score_board[user_id],
										'BOARD': score_board, 'code': code})
		else:
			code = 'F' #Can use
			score_board[user_id] = 0
			response_body = json.dumps({'ID': user_id, 'SCORE': score_board[user_id],
			                            'BOARD': score_board, 'code': code})


	#score_register
	if signal == 2:
		if score_board[user_id] > user_score: #origin score > new score
			code = 'S' #Success to register
		else: 
			score_board[user_id] = user_score
			code = 'S'


	#sort by socre
	sorting_score_board = sorted(score_board.items(), key = lambda x:x[1], reverse=True)
	
	response_body = json.dumps({'ID': user_id, 'SCORE': score_board[user_id],
								'BOARD': sorting_score_board, 'code': code})
	status = '200 OK'
	response_headers = [('Content-Type', 'application/json'),('Content-Length', str(len(response_body)))]
	start_response(status, response_headers)


	#store score_board
	f = open('score_data.dat', 'wb+')
	pickle.dump(score_board, f)
	f.close()

	return [response_body]
	
httpd = make_server('192.168.200.142', 8051, application)	
httpd.serve_forever()