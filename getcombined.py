import subprocess

def getpages(filename):
	f = open(filename.strip(), 'r')
	pages=[]
	for line in f:		#read a line from file
		if "<page" in line:
			page = line.split()[1].split('"')[1]
		if ('dataset' in line.lower() and page not in pages):
			pages.append(page)
	return pages

filelist = open('xmllist', 'r')
cmd = 'pdftk '
#subprocess.call(["pdftk A=4520a063.pdf B=p117-de12.pdf cat A1 A3 B2 output combined.pdf"], shell=True)
alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
			'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
str1=str2=''
i=0 	#index for pdfs with dataset
j=0		#index for combined pdfs if there are more than alphabet
for currentpdf in filelist:
	pages=getpages(currentpdf)
	if pages:
		str1+=alphabet[i%len(alphabet)]+'='+ \
			currentpdf.replace('.xml','.pdf').strip()+' '
		for p in pages:
			str2+=alphabet[i%len(alphabet)]+p+' '
		i+=1
		if i==len(alphabet):
			#reached the limit write to a combined file
			#print cmd+str1+'cat '+str2+'output combined'+str(j)+'.pdf'
			subprocess.call([cmd+str1+'cat '+str2+'output combined'+str(j)+\
				'.pdf'], shell=True)			
			str1=str2=''
			j+=1
			i=0

if j==0:
	#print cmd + str1 + 'cat ' + str2 + 'output combined.pdf'
	subprocess.call([cmd + str1 + 'cat ' + str2 + 'output combined.pdf'], \
		shell=True)
else:
	#print cmd + str1 + 'cat ' + str2 + 'output combined'+str(j)+'.pdf'
	subprocess.call([cmd + str1 + 'cat ' + str2 + 'output combined'+\
		str(j)+'.pdf'],shell=True)
	strk=''
	for k in range(j+1):
		strk+='combined'+str(k)+'.pdf '
	#print cmd + strk + 'cat output combined.pdf'
	subprocess.call([cmd + strk + 'cat output combined.pdf'], shell=True)
