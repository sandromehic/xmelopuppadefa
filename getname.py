# coding=utf-8

import linecache

def getall(filename):
	f = open(filename.strip(), 'r')
	article = ['', '', '', [], []]
	article[0]=(filename.strip().split('/')[-1])	
										#0 is the filename
										#1 is for title, 2 for date
	article[2]='2012'					#3 for authors and 4 for datasets
	#here we define a couple of variables needed for line numbering
	titlemark=0							#mark the line where the title ends
	abstractmark=1000				
	depthsearchds=2						#how many line to expand searching for
										#dataset in a file
	for i, line in enumerate(f):		#read a line from file
		#find title		
		if ("font=\"0\"" in line and i<30):	#check if its the title line
			titlepart = findtitle(line)
			article[1] += titlepart
			titlemark = i
		#find year of article
		if 'copyright' in line.lower():
			article[2] = findyear(line, 'copyright')
		if '©' in line:
			article[2] = findyear(line, '©')
		#find authors delimited by title and abstract
		if ("abstract" in line.lower() or "introduction" in line.lower()):
			if abstractmark==1000:
				abstractmark=i
		elif(abstractmark==1000 and titlemark!=0 and titlemark!=i):
			#extract possible authors and adds the list to the existing one
			posauthors = findauthors(line)
			if posauthors != None:
				article[3].extend(posauthors)
		if ('dataset' in line.lower() or 'database' in line.lower()):
			#if we find dataset or database in text, we make an extensive
			#search for the matching keywords that would tell us a name
			#of the dataset that we are searching for
			#IMPORTANT: here we pass i+1 as line number, as linecache mod
			#start the index counting from 1 instead of 0 like enumerate
			findds(filename.strip(), i+1, depthsearchds, article[4])
			#print filename
	return article

def findds(filename, i, depthsearch, dss):
	line = constructline(filename,i,depthsearch)
	for d in datasets:
		if (d in line.lower() and d not in dss):
			dss.append(d)

def constructline(filename,i,dpt):
	defline=''
	for j in range(i-dpt,i+dpt):
		line=linecache.getline(filename,j)
		line=line.split('>')
		if len(line)>2:
			k=1
			while (len(line[k]) < 3 and line[k] != ''):
				k+=1
			defline+=line[k].split('<')[0] + ' '
	return defline

def findyear(line, splitter):
	return line.lower().split(splitter)[1].split()[0]

def findauthors(line):
	authors=[]
	posauthor=''
	txt = line.split('>')
	j=1
	while (len(txt[j]) < 3 and txt[j]!=''):
		j+=1

	txt=txt[j].split('<')[0]
	if all(x not in txt.lower() for x in exclude):
		if len(txt) > 3:
			posauthor = txt
	if ' and' in posauthor:
		posauthor=posauthor.replace(' and',',')
	for x in posauthor.split(','):
		author=''
		for y in x.split():
			if (len(y)>1 and y[0]==y[0].upper()):
				author+=y+" "
		
		if author!='':
			authors.append(author)
			author=''
	return authors

def findtitle(line):
	if line.split('>')[1]=="<b":
		return line.split('>')[2].split('<')[0]
	else:
		return line.split('>')[1].split('<')[0]

def getexclude():
	global exclude
	f = open('excludekeywords','r')
	for line in f:
		for keyword in line.split():
			exclude.append(keyword)	

def getdatasets():
	global datasets
	f = open('datasetkeywords','r')
	for line in f:
		datasets.append(line.strip())

filelist = open('xmllist', 'r')
fileoutput = open('xmltitles', 'w')
exclude=[]
getexclude()
datasets=[]
getdatasets()
for currentpdf in filelist:
	article=getall(currentpdf)
	strtowrite = article[0]+"\n\t" + article[1]+"\n\t" + article[2]+"\n\t" + "Authors:" + "\n\t\t"
	for element in article[3]:
		strtowrite += element + "\n\t\t"
	strtowrite += "\n\t" + "Datasets:" + "\n\t\t"
	for element in article[4]:
		strtowrite += element + "\n\t\t"
	strtowrite+="\n"
	fileoutput.write(strtowrite)
