import socket
 
HOST,PORT = '127.0.0.1',8080
 
my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)# socket.socket(family, type)
my_socket.bind((HOST,PORT)) #Liga o socket ao endereco e a porta
my_socket.listen(1)
 
print('Servidor na porta ',PORT)
 
while True:
	connection,address = my_socket.accept()
	request = connection.recv(2048).decode('utf-8')
	#A conecao transmite a data em bytes. Por isso e necessario converter a string no formato UTF-8
	#Tanto na recepcao como depois na transmissao
	
	string_list = request.split(' ')     #Divide a mensagem recebida e coloca numa lista. Para isso usa a funcao do python split usando os espacos
										 #entre os dados para faze-lo
 
	method = string_list[0] # Neste caso o metodo e GET e vai ficar na primeira posicao da lista, porque e a primeira coisa que aparece na mensagem
	requesting_file = string_list[1] #depois do GET esta o nome do ficheiro que fica armazenado na segunda posicao da lista que e o que vamos usar

	
	#print('metodo ',method)
	print('Client request ',requesting_file)
 
	
	myfile = requesting_file.lstrip('/') #remove a / do nome do ficheiro
	
	if(myfile == ''):
		myfile = 'index.html'    # Se nenhum nome de ficheiro for indicado, serve o index.html
 
	try:
		if(myfile != 'index.html'):	
			response = '<a href="index.html"> Inicio </a> <br><br>' # se nao for a pagina de index, coloca uma ligacao para ela
		else:
			response = ''#se for index, limpa o conteudo de response, para nao ter ligacao para a propria pagina de uma interacao anterior
			
		file = open(myfile,'rb') # abre o ficheiro , r => ler , b => formato byte 
		response += file.read()
		file.close()
 
		header = 'HTTP/1.1 200 OK\n'
		mimetype = 'text/html'
 
		header += 'Content-Type: '+str(mimetype)+'\n\n'
 
	except Exception as e:
		header = 'HTTP/1.1 404 Not Found\n\n'
		response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')
 
	final_response = header.encode('utf-8')
	final_response += response
	connection.send(final_response)
	connection.close()