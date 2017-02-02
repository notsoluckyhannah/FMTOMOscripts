import numpy as np
import pandas as pd
import fnmatch


num_lines = sum(1 for line in open('origevent.t'))
num_linesf4=sum(1 for line in open('hypinv.sta'))
print "rows %s" %num_lines
print "stations %s" %num_linesf4
 
df=pd.DataFrame()

###takes first 4 characters of origevent.t file and saves them to a data frame
with open('origevent.t') as f1:
        for line in f1:
                ff=line[0:5]
                flines=[[ff]]
                dfm=pd.DataFrame(flines)
                df=df.append(dfm)


data=[]
e=[]
linenum=[]

###matches first 4 characters in each line to 2015 and creates a dataframe of line numbers  for each event
for j in range(num_lines):
        data=df.iat[j,0]
        if fnmatch.fnmatch(data,'2015*'):   
                e=np.append(e,data)
                linenum=np.append(linenum,j)

dfj=pd.DataFrame(e)      
linenum=np.append(linenum,num_lines)        
el=len(e)
lt=len(linenum)

f=open('origevent.t')
lines=f.readlines()

k=0

####creates each file for the number of events in the main file         
while k < lt-1:
        f1=open('EQK%s.txt' %k, 'w')
        for m in range(int(linenum[k]),int(linenum[k+1])):
                f1.write(lines[m])        
        f1.close()
        k=k+1



####calculates the lat and lon for each station stores in dataframe and prints to station file
dfi=pd.DataFrame()
dfz=pd.DataFrame()
f4=open('hypinv.sta', 'r')
for line in f4:
        staf4=line[0:6]
        staf4=staf4.strip()
        #print staf4
        latf4=line[15:17]
        #print latf4
        laminf4=line[18:23]
        if float(laminf4) > 1000:
                laminf4=float(laminf4)/1000
        #print laminf4
        lonf4=line[27:29]
        #print lonf4
        lominf4=line[30:35]
        if float(lominf4) > 1000:
                lominf4=float(lominf4)/1000
        #print lominf4
        laminf4=float(laminf4)/60
        ##print lamin
        ladegf4=int(latf4)+float(laminf4)
        #print ladegf4
        ##print lon
        lominf4=float(lominf4)/60
        ##print lomin
        lodegf4=int(lonf4)+float(lominf4)
        lodegf4=-1*float(lodegf4)
        ##print lodegf4
        depf4=line[38:42]
        depf4=float(depf4)/1000
        ##print depf4
        a=[[staf4,ladegf4,lodegf4,depf4]]
        ##print a
        dfj=pd.DataFrame(a, columns=['sta','lat','lon','dep'])
        dfi=dfi.append(dfj)
f4.close()
dfistring=dfi.to_string(header=0,index=0)
f5=open('stationinfo.t','w')
f5.write(dfistring)
f5.close()

###takes a count of the number of events recorded per station and prints to file, can be used to make histogram later
m=1
k=0
for line in f:
	while k <= num_linesf4:
 		if dfi.iat[k,0] == line[0:5]:
			m=m+1
		sc=[[dfi.iat[k,0],m]]
		dfn=pd.DataFrame(sc, columns=['sta', 'count'])
		dfz=dfz.append(dfn)
		k=k+1
dfzstring=dfz.to_string(header=0,index=0)
f7=open('stationcount.t','w')
f7.write(dfzstring)
f7.close()
	

####calculates the lat, lon and time for each station in each event file stores in data frame dfl. picked travel time is converted into seconds and compared to origin time also converted to seconds.
####also creates a new file for each event where the new information will be stored
##creates a source file for FMTOMO using certain depth parameters for ray pays
h=0
m=0
q=0
evt=[]

lm=lt-1

format1=lambda x:'%.4f'%x
format2=lambda x:'%.3f'%x
format3=lambda x:'%-5s'%x
format4=lambda x:'%.2f'%x
f6=open('sourceswa1.in', 'w')
f6.write('%s\n' %lm)
f7=open('eventlist.t', 'w')

while h < lt-1:
	dfl=pd.DataFrame()
	dfq=pd.DataFrame()
        f2=open('EQK%s.txt' %h)
        fl=f2.readline().strip()
        date=fl[0:8]
        timet=fl[8:15]
        timeh=fl[8:10]
        timeh=timeh.replace(' ','0')
        timeh=float(timeh)*3600
        timem=fl[10:12]
        timem=timem.replace(' ','0')
        timem=float(timem)*60
        times=fl[12:15]
        times=float(times)/10
        time=float(timem)+float(timeh)+float(times)
        lat=fl[16:18]
        lamin=fl[19:23]
        lamin=float(lamin)/100
        lamin=float(lamin)/60
        ladeg=int(lat)+float(lamin)
        lon=fl[24:26]
        lomin=fl[27:31]
        lomin=float(lomin)/100
        lomin=float(lomin)/60
        lodeg=int(lon)+float(lomin)
	lodeg=-1*lodeg
        depeq=fl[31:36]
	depeq=depeq.replace(' ','0')
	depeq=float(int(depeq))/100
	f7.write('%s %s %s %s\n' %(h, ladeg, lodeg, depeq))	
        f6.write('%s %s %s\n' %(ladeg, lodeg, depeq))
        f6.write('1\n')
      	if depeq > 40: 
        	f6.write('1 1 EQM%s.txt\n' %(h))
	else:
		f6.write('2 1 EQM%s.txt\n' %(h))
        f3=open('EQM%s.txt' %h, 'w')
        nl=sum(1 for line in open("EQK%s.txt" %h))
        nl=nl-2
        for line in f2:
                if line.strip():
                        staf2=line[0:6]
                        staf2=staf2.strip()
                        comp=line[14:15]
                        th=line[25:27]
                        th=th.replace(' ','0')
                        th=float(th)*3600              
                        tm=line[27:29]
                        tm=float(tm)*60     
                        ts=line[30:34]
                        ts=ts.replace(' ','0')
                        ts=float(ts)/100
                        tf=float(th)+float(tm)+float(ts)
                        tdiff=float(tf)-float(time)
                        b=[[staf2,comp,time,tf,tdiff]]
                        dfm=pd.DataFrame(b, columns=['sta','comp','evtt','stat','oritt'])
                        dfl=dfl.append(dfm)
			dfq=pd.DataFrame()
        for m in range(nl): 
                for q in range(num_linesf4):
                        if dfi.iat[q,0] == dfl.iat[m,0] and dfl.iat[m,1] == 'P':
				unc=0.15
                                d=[[dfi.iat[q,1],dfi.iat[q,2],dfi.iat[q,3],dfl.iat[m,4],unc]]
                                dfw=pd.DataFrame(d, columns=['lat','lon','dep','otime','unc'])
                                dfq=dfq.append(dfw)
                                dfstring=dfq.to_string(header=0,index=0,formatters={'lat':format1,'lon':format1,'dep':format2,'otime':format4,'unc':format4})
                                
                        q=q+1
                m=m+1
        #del dfw
	del dfl
	del dfm	
	f2.close()
        h=h+1

 	rows=len(dfq.index)
     	f3.write('%s\n' %rows)
       # f3.write('%.4f %.4f\n' %(ladeg, lodeg))
        f3.write(dfstring)               
	f3.close()
        del dfq
f7.close()
####check and make sure events have different locations, if not, print events with same lat and lon

data=[]
with open('eventlist.t') as el:
	for line in el:
		line=line.split()
		if len(line)==4: 
			data.append(line)
#print data
data.sort(key=lambda s:(s[1],s[2]))
dfp=pd.DataFrame(data)
dfstring1=dfp.to_string(header=0,index=0)

f8=open('eventlistt.t','w')
f8.write(dfstring1)

#f6=open('sourceswa1.in','r')
#f9=open('sourceswa2.in','w')
#print p
#f6.readline() # and discard
#f9.write('%s\n' %p)
#shutil.copyfileobj(f6, f9)






