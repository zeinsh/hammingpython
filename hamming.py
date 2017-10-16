#    This is implementation for Hamming coding
# this is done as an assignment in coding theory subject 
import math
_FILENAME='report.txt'
def cleanFile(filename):
    f=open(filename,'w')
    f.close()
def logtofile(filename,message):
    f=open(filename,'a')
    f.write(message+'\n')
    f.close()

def binstrTOarray(str):
    return [int(c) for c in str]
def arrayTobinstr(arr):
    return ''.join(str(e) for e in arr)
def getHammingParameters(message,type):
    if type=='encode':
	n=len(message)
	r=int(math.ceil(math.sqrt(n)))
	if math.pow(2,r)<=r+n:
            r+=1
	l=n+r
    else:
	l=len(message)
	r=int(math.ceil(math.sqrt(l)))
	n=l-r
    report='Hamming parameters\n'+'-'*20+'\n'
    report+='Original message length n=%d\nParity-check matrix length r=%d\nEncoded message length l=%d\n'%(n,r,l)
    report+='-'*20+'\n'
    logtofile(_FILENAME,report)
    return n,r,l
def getMap(n,r):
    l=n+r
    maps=[]
    for i in xrange(r):
        p=int(math.pow(2,i))
	repeat=l/p+1
        map=(['_']*p+['X']*p)*repeat
        maps.append(map[1:l+1])
    return maps
def binstrTOarray(str):
    return [int(c) for c in str]
def arrayTobinstr(arr):
    ret=''.join(str(e) for e in arr)
    return ret.replace('2','X')
def hamming_code(message):
    n,r,l=getHammingParameters(message,'encode')
    maps=getMap(n,r)
    for i in range(r):
	p=int(math.pow(2,i))
        message.insert(p-1,2)
    report=arrayTobinstr(message)+'   S\n'
    for i in range(r):
	p=int(math.pow(2,i))
	v=0
	for j in range(l):
	    if maps[i][j]=='X':
		v+=message[j]%2
        report+='%s   %d\n'%(arrayTobinstr(maps[i]),v)
	message[p-1]=v%2
    report+='%s\n'%('-'*20)
    report+=arrayTobinstr(message)+'\n'
    logtofile(_FILENAME,report)
    return message
def hamming_check(message):
    n,r,l=getHammingParameters(message,'decode')
    positions=[int(math.pow(2,x)) for x in xrange(r)]
    maps=getMap(n,r)
    error=[]
    report=arrayTobinstr(message)+'   S\n'
    errorcode=''
    for i in range(r):
        v=0
        for j in range(l):
            if maps[i][j]=='X':
                v+=message[j]
        report+='%s   %d\n'%(arrayTobinstr(maps[i]),v)
	errorcode=str(v%2)+errorcode
        if (v%2!=0):
	    error.append(positions[i])
    report+='The resulting error code is %s\n'%errorcode
    logtofile(_FILENAME,report)
    return len(error)==0,sum(error)


if __name__ == '__main__':
    """   The program will run on two inputs , one as a sended message 
	and the other as recieved message .
	the steps of the algorithm and the output will be described in 
	the report file 'report.txt' 
    """
    cleanFile(_FILENAME)
    #Input : 
    original='011001011'
    recieved='0000010101011'

    #sending message
    report='Hamming coding algorithm implementation\n'+'-'*40+'\n'
    report+='Original message : %s\n'%original
    logtofile(_FILENAME,report)
    orgarr=binstrTOarray(original)
    encoded=hamming_code(orgarr)

    # recieved
    report='-'*40+'\n'
    report+='Recieved message : %s\n'%recieved
    logtofile(_FILENAME,report)
    recarr=binstrTOarray(recieved)
    iscorrect,errorplace=hamming_check(recarr)
    
    if iscorrect:
	report='\n\nThe recieved message %s is correct\n'%recieved
    else:
        recarr[errorplace-1]+=1
        recarr[errorplace-1]%=2
	corrected=arrayTobinstr(recarr)
	report='The recieved message %s contains error \nin position number %d\nThe corrected Message is %s\n'%(recieved,errorplace,corrected)
    logtofile(_FILENAME,report)


