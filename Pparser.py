def post_parser(txt):
	tags = []
	shouts = []
	txts = txt.split(' ')

	for i in txts:
		if i[0] == "#":
			n=0
			for j in i[1:]:
				if j =='#'or j =='/'or j ==','or j ==';'or j =='?'or j ==':'or j =='!':
					break
				n+=1

			#adicionar tag
			#print("tag:",i[1:n+1])

			tags.append(i[1:n+1])

		elif i[0] == "@":
			n=0
			for j in i[1:]:
				if j =='#'or j =='/'or j ==','or j ==';'or j =='?'or j ==':'or j =='!':
					break
				n+=1

			#adicionar shout
			shouts.append(i[1:n+1])

	return tags,shouts
			#print("shout:",i[1:n+1])