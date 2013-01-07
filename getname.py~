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
	for i, line in enumerate(f):		#read a line from file
		if ("font=\"0\"" in line and i<30):	#check if its the title line
			titlepart = findtitle(line)
			article[1] += titlepart
			titlemark = i
		if ("abstract" in line.lower() or "introduction" in line.lower()):
			if abstractmark==1000:
				abstractmark=i
		else:
			if (abstractmark==1000 and titlemark!=0 and titlemark!=i):
				posauthor = findauthors(line)
				if posauthor != None:
					article[3].append(str(posauthor))

	#print article[0]
	return article

def findauthors(line):
	txt = line.split('>')
	j=1
	while (len(txt[j]) < 3 and txt[j]!=''):
		j+=1

	txt=txt[j].split('<')[0]
	if all(x not in txt.lower() for x in exclude):
		if len(txt) > 3:
			return txt

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

filelist = open('xmllist', 'r')
fileoutput = open('xmltitles', 'w')
exclude=[]
getexclude()
for currentpdf in filelist:
	article=getall(currentpdf)
	strtowrite = article[0]+"\n\t" + article[1]+"\n\t" + article[2]+"\n\t"
	for element in article[3]:
		strtowrite += element + "\n\t"
	strtowrite+="\n"
	fileoutput.write(strtowrite)
