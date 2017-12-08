
# coding: utf-8

# # Hamming code
# 
# Hamming code is a set of error-correction code s that can be used to detect and correct bit errors that can occur when computer data is moved or stored. Hamming code is named for R. W. Hamming of Bell Labs.
# 

# In[1]:


import math
import sys
_FILENAME='report.txt'
_COUNTER=0


# In[2]:


## Helpers functions
def cleanFile(filename):
    # clean file content
    f=open(filename,'w')
    f.close()
def logtofile(filename,message,WR=True):
    global _COUNTER
    _COUNTER=_COUNTER+1
    print "#{}\n{}\n".format(_COUNTER , message)
    if WR:
        f=open(filename,'a')
        f.write(message+'\n')
        f.close()
def binstrTOarray(str):
    return [int(c) for c in str]
def arrayTobinstr(arr):
    ret=''.join(str(e) for e in arr)
    return ret.replace('2','X')


# ## find parameters 
# 1- if it is encoding process : 
# 
# - message length : n 
# - find r "number of parity bits" : $2^r\geq n+r+1$
# - encoded message length : l=n+r
# 
# 2- else if it is decoding process :
# 
# - encoded message length : l
# - find r "number of parity bits" : $ceil(log_2(l))$
# - original message length : n=l-r

# In[3]:


def log2(n):
    return math.log(n)/math.log(2)
def getHammingParameters(message,type,WR=True):
    if type=='encode':
        n=len(message)
        r=int(math.ceil(log2(n)))
        if math.pow(2,r)<=r+n:
            r+=1
        l=n+r
    else:
        l=len(message)
        r=int(math.ceil(log2(l)))
        n=l-r
    report='Hamming parameters\n'+'-'*20+'\n'
    report+='Original message length n=%d\nParity-check matrix length r=%d\nEncoded message length l=%d\n'%(n,r,l)
    report+='-'*20+'\n'
    logtofile(_FILENAME,report,WR)
    return n,r,l


# ## Hamming code map 
# 
# where are parity bits located ?
# 
# for number of parity bits = r , location of parity bits in {$2^p;p\leq r$}
# 
# The function getMap will determine the bits that each parity is responsible for
# 
# <table class="wikitable">
# <tbody><tr>
# <th>Bit #</th>
# <th>1</th>
# <th>2</th>
# <th>3</th>
# <th>4</th>
# <th>5</th>
# <th>6</th>
# <th>7</th>
# </tr>
# <tr>
# <th>Transmitted bit</th>
# <th><span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML">
#   <semantics>
#     <mrow class="MJX-TeXAtom-ORD">
#       <mstyle displaystyle="true" scriptlevel="0">
#         <msub>
#           <mi>p</mi>
#           <mrow class="MJX-TeXAtom-ORD">
#             <mn>1</mn>
#           </mrow>
#         </msub>
#       </mstyle>
#     </mrow>
#     <annotation encoding="application/x-tex">{\displaystyle p_{1}}</annotation>
#   </semantics>
# </math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/b9b58f22283ca46dd5da309cc34303b06a797783" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; margin-left: -0.079ex; width:2.32ex; height:2.009ex;" alt="p_{1}"></span></th>
# <th><span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML">
#   <semantics>
#     <mrow class="MJX-TeXAtom-ORD">
#       <mstyle displaystyle="true" scriptlevel="0">
#         <msub>
#           <mi>p</mi>
#           <mrow class="MJX-TeXAtom-ORD">
#             <mn>2</mn>
#           </mrow>
#         </msub>
#       </mstyle>
#     </mrow>
#     <annotation encoding="application/x-tex">{\displaystyle p_{2}}</annotation>
#   </semantics>
# </math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/43f1b08d7d69712872e051c2b33fdfa9f5d42319" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; margin-left: -0.079ex; width:2.32ex; height:2.009ex;" alt="p_{2}"></span></th>
# <th><span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML">
#   <semantics>
#     <mrow class="MJX-TeXAtom-ORD">
#       <mstyle displaystyle="true" scriptlevel="0">
#         <msub>
#           <mi>d</mi>
#           <mrow class="MJX-TeXAtom-ORD">
#             <mn>1</mn>
#           </mrow>
#         </msub>
#       </mstyle>
#     </mrow>
#     <annotation encoding="application/x-tex">{\displaystyle d_{1}}</annotation>
#   </semantics>
# </math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/4cccb5a6a2f1acab4ca255e0be86c224ed82282a" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; width:2.281ex; height:2.509ex;" alt="d_{1}"></span></th>
# <th><span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML">
#   <semantics>
#     <mrow class="MJX-TeXAtom-ORD">
#       <mstyle displaystyle="true" scriptlevel="0">
#         <msub>
#           <mi>p</mi>
#           <mrow class="MJX-TeXAtom-ORD">
#             <mn>3</mn>
#           </mrow>
#         </msub>
#       </mstyle>
#     </mrow>
#     <annotation encoding="application/x-tex">{\displaystyle p_{3}}</annotation>
#   </semantics>
# </math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/2a79626b787857474daa665c953bbc6725e7c345" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; margin-left: -0.079ex; width:2.32ex; height:2.009ex;" alt="p_{3}"></span></th>
# <th><span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML">
#   <semantics>
#     <mrow class="MJX-TeXAtom-ORD">
#       <mstyle displaystyle="true" scriptlevel="0">
#         <msub>
#           <mi>d</mi>
#           <mrow class="MJX-TeXAtom-ORD">
#             <mn>2</mn>
#           </mrow>
#         </msub>
#       </mstyle>
#     </mrow>
#     <annotation encoding="application/x-tex">{\displaystyle d_{2}}</annotation>
#   </semantics>
# </math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/9276f8f68c5c23329de74ad76e69f6801358fb1f" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; width:2.281ex; height:2.509ex;" alt="d_{2}"></span></th>
# <th><span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML">
#   <semantics>
#     <mrow class="MJX-TeXAtom-ORD">
#       <mstyle displaystyle="true" scriptlevel="0">
#         <msub>
#           <mi>d</mi>
#           <mrow class="MJX-TeXAtom-ORD">
#             <mn>3</mn>
#           </mrow>
#         </msub>
#       </mstyle>
#     </mrow>
#     <annotation encoding="application/x-tex">{\displaystyle d_{3}}</annotation>
#   </semantics>
# </math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/0f051bd12b5413014eeb4944816cb5672edfcff4" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; width:2.281ex; height:2.509ex;" alt="d_{3}"></span></th>
# <th><span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML">
#   <semantics>
#     <mrow class="MJX-TeXAtom-ORD">
#       <mstyle displaystyle="true" scriptlevel="0">
#         <msub>
#           <mi>d</mi>
#           <mrow class="MJX-TeXAtom-ORD">
#             <mn>4</mn>
#           </mrow>
#         </msub>
#       </mstyle>
#     </mrow>
#     <annotation encoding="application/x-tex">{\displaystyle d_{4}}</annotation>
#   </semantics>
# </math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/d43e86e828c6871d10a70e4c86a6cea2415991f0" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; width:2.281ex; height:2.509ex;" alt="d_{4}"></span></th>
# </tr>
# <tr>
# <td><span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML">
#   <semantics>
#     <mrow class="MJX-TeXAtom-ORD">
#       <mstyle displaystyle="true" scriptlevel="0">
#         <msub>
#           <mi>p</mi>
#           <mrow class="MJX-TeXAtom-ORD">
#             <mn>1</mn>
#           </mrow>
#         </msub>
#       </mstyle>
#     </mrow>
#     <annotation encoding="application/x-tex">{\displaystyle p_{1}}</annotation>
#   </semantics>
# </math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/b9b58f22283ca46dd5da309cc34303b06a797783" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; margin-left: -0.079ex; width:2.32ex; height:2.009ex;" alt="p_{1}"></span></td>
# <td style="background:#9F9;vertical-align:middle;text-align:center;" class="table-yes">Yes</td>
# <td style="background:#F99;vertical-align:middle;text-align:center;" class="table-no">No</td>
# <td style="background:#9F9;vertical-align:middle;text-align:center;" class="table-yes">Yes</td>
# <td style="background:#F99;vertical-align:middle;text-align:center;" class="table-no">No</td>
# <td style="background:#9F9;vertical-align:middle;text-align:center;" class="table-yes">Yes</td>
# <td style="background:#F99;vertical-align:middle;text-align:center;" class="table-no">No</td>
# <td style="background:#9F9;vertical-align:middle;text-align:center;" class="table-yes">Yes</td>
# </tr>
# <tr>
# <td><span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML">
#   <semantics>
#     <mrow class="MJX-TeXAtom-ORD">
#       <mstyle displaystyle="true" scriptlevel="0">
#         <msub>
#           <mi>p</mi>
#           <mrow class="MJX-TeXAtom-ORD">
#             <mn>2</mn>
#           </mrow>
#         </msub>
#       </mstyle>
#     </mrow>
#     <annotation encoding="application/x-tex">{\displaystyle p_{2}}</annotation>
#   </semantics>
# </math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/43f1b08d7d69712872e051c2b33fdfa9f5d42319" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; margin-left: -0.079ex; width:2.32ex; height:2.009ex;" alt="p_{2}"></span></td>
# <td style="background:#F99;vertical-align:middle;text-align:center;" class="table-no">No</td>
# <td style="background:#9F9;vertical-align:middle;text-align:center;" class="table-yes">Yes</td>
# <td style="background:#9F9;vertical-align:middle;text-align:center;" class="table-yes">Yes</td>
# <td style="background:#F99;vertical-align:middle;text-align:center;" class="table-no">No</td>
# <td style="background:#F99;vertical-align:middle;text-align:center;" class="table-no">No</td>
# <td style="background:#9F9;vertical-align:middle;text-align:center;" class="table-yes">Yes</td>
# <td style="background:#9F9;vertical-align:middle;text-align:center;" class="table-yes">Yes</td>
# </tr>
# <tr>
# <td><span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML">
#   <semantics>
#     <mrow class="MJX-TeXAtom-ORD">
#       <mstyle displaystyle="true" scriptlevel="0">
#         <msub>
#           <mi>p</mi>
#           <mrow class="MJX-TeXAtom-ORD">
#             <mn>3</mn>
#           </mrow>
#         </msub>
#       </mstyle>
#     </mrow>
#     <annotation encoding="application/x-tex">{\displaystyle p_{3}}</annotation>
#   </semantics>
# </math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/2a79626b787857474daa665c953bbc6725e7c345" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; margin-left: -0.079ex; width:2.32ex; height:2.009ex;" alt="p_{3}"></span></td>
# <td style="background:#F99;vertical-align:middle;text-align:center;" class="table-no">No</td>
# <td style="background:#F99;vertical-align:middle;text-align:center;" class="table-no">No</td>
# <td style="background:#F99;vertical-align:middle;text-align:center;" class="table-no">No</td>
# <td style="background:#9F9;vertical-align:middle;text-align:center;" class="table-yes">Yes</td>
# <td style="background:#9F9;vertical-align:middle;text-align:center;" class="table-yes">Yes</td>
# <td style="background:#9F9;vertical-align:middle;text-align:center;" class="table-yes">Yes</td>
# <td style="background:#9F9;vertical-align:middle;text-align:center;" class="table-yes">Yes</td>
# </tr>
# </tbody></table>
# 
# <center>map for (7,4) hamming encoding</center>

# In[4]:


def getMap(n,r):
    l=n+r
    maps=[]
    for i in xrange(r):
        p=int(math.pow(2,i))
        repeat=l/p+1
        map=(['_']*p+['X']*p)*repeat
        maps.append(map[1:l+1])
    return maps


# In[5]:


n=4
r=3
hmap=getMap(n,r)
print "Map for (7,4) Hamming encoding"
for row in hmap:
    print arrayTobinstr(row)


# ## Encoding phase
# 
# Input : 
# message : array of 0s and 1s 
# 
# output : 
# encoded message
# 
# Steps :
# 
# 1- Get parameters for hamming encoding
# 
# 2- Generate map 
# 
# 3- for each parity:
#     - sum the corresponding positions in the message
#     - set result mod 2 as a value for this parity 

# In[6]:


def hamming_code(message,WR=True):
    # Get parameters
    n,r,l=getHammingParameters(message,'encode',WR)
    # Generate map for encoding
    maps=getMap(n,r)
    # insert parities inside message (distinguish value 2)
    for i in range(r):
        p=int(math.pow(2,i))
        message.insert(p-1,2)
    report=arrayTobinstr(message)+'   S\n'
    # Encoding phase
    for i in range(r):
        p=int(math.pow(2,i))  # take i-th parity position
        v=0
        # sum the corresponding positions
        for j in range(l):
            if maps[i][j]=='X':
                v+=message[j]%2
        report+='%s   %d\n'%(arrayTobinstr(maps[i]),v)
        # set mod to the i-th parity
        message[p-1]=v%2
    report+='%s\n'%('-'*20)
    report+=arrayTobinstr(message)+'\n'
    logtofile(_FILENAME,report,WR)
    return message


# In[7]:


message='1101'
messageArray=binstrTOarray(message)
encoded=hamming_code(messageArray,False)


# ## Check Parity phase and decoding
# 
# Input : encoded message : binary string
# 
# output : error position
# 
# Steps :
# 
# 1- Get parameters for hamming encoding
# 
# 2- Generate map
# 
# 3- for each parity:
# - sum the corresponding positions in the message
# - if sum mod 2 !=0 add this position to errors array
# 
# 4- if errors is empty : the recieved message is correct
# 
# else : there is error in the position (sum errors array)

# In[8]:


def hamming_check(message):
    # Get parameters
    n,r,l=getHammingParameters(message,'decode')
    # Generate map for encoding
    maps=getMap(n,r)
    # paraties position
    positions=[int(math.pow(2,x)) for x in xrange(r)]
    error=[]
    report=arrayTobinstr(message)+'   S\n'
    errorcode=''
    # checking phase
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


# In[9]:


cleanFile(_FILENAME)
#Input : 
original='011001011010111'
#sending message
report='Hamming coding algorithm implementation\n'+'-'*40+'\n'
report+='Original message : %s\n'%original
logtofile(_FILENAME,report)
orgarr=binstrTOarray(original)
encoded=hamming_code(orgarr)
message_sent=arrayTobinstr(encoded)
report='Encoded message : %s\n'%message_sent
report+='Sending message ... \n'
logtofile(_FILENAME,report)


# In[10]:


recieved=message_sent
# recieved
report='-'*40+'\n'+'recieving message ...\n'
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


# In[11]:


recieved='0011111'
# recieved
report='-'*40+'\n'+'recieving message2 ...\n'
report+='Recieved message 2: %s\n'%recieved
logtofile(_FILENAME,report)

recarr=binstrTOarray(recieved)
iscorrect,errorplace=hamming_check(recarr)
    
if iscorrect:
    report='\n\nThe recieved message2 %s is correct\n'%recieved
else:
    recarr[errorplace-1]+=1
    recarr[errorplace-1]%=2
    corrected=arrayTobinstr(recarr)
    report='The recieved message2 %s contains error \nin position number %d\nThe corrected Message is %s\n'%(recieved,errorplace,corrected)
logtofile(_FILENAME,report)

