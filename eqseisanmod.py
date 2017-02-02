import numpy as np
import pandas as pd
import fnmatch
import shutil

num_lines = sum(1 for line in open('catalog.t'))
num_linesf4=sum(1 for line in open('hypinv.sta'))

df=pd.DataFrame()


with open('catalog.t') as f1:
        for line in f1:
                ff=line[1:6]
		ind=line[79:81]
		dep=line[38:42]
		dep=dep.replace(' ','0')
                flines=[[ff,ind,dep]]
                dfm=pd.DataFrame(flines)
                df=df.append(dfm)


data=[]
e=[]
linenum=[]

for j in range(num_lines):
        data=df.iat[j,0]
	index=df.iat[j,1]
	depth=df.iat[j,2]
        if fnmatch.fnmatch(data,'201*') and fnmatch.fnmatch(index,'*1*'):  # matches the df to the year marker
                e=np.append(e,data)
                linenum=np.append(linenum,j)

dfj=pd.DataFrame(e)       
linenum=np.append(linenum,num_lines)        
el=len(e)
lt=len(linenum)


f=open('catalog.t')
lines=f.readlines()

k=0

####creates each file for the number of events in the main file         
while k < lt-1:
        f1=open('EQ%s.txt' %k, 'w')
	for m in range(int(linenum[k]),int(linenum[k+1])):
		f1.write(lines[m])        
	f1.close()
	k=k+1


f10=open('residual1.t', 'w')
####calculates the lat and lon for each station stores in data frame dfi
dfi=pd.DataFrame()
dfz=pd.DataFrame()
f4=open('hypinv.sta', 'r')
for line in f4:
        staf4=line[0:6]
        staf4=staf4.strip()
        latf4=line[15:17]
        laminf4=line[18:23]
	laminf4=float(laminf4)
        if laminf4 > 1000:
                laminf4=float(laminf4)/1000
        lonf4=line[27:29]
        lominf4=line[30:35]
        if float(lominf4) > 1000:
                lominf4=float(lominf4)/1000
        laminf4=float(laminf4)/60
        ladegf4=int(latf4)+float(laminf4)
        lominf4=float(lominf4)/60
        lodegf4=int(lonf4)+float(lominf4)
        lodegf4=-1*float(lodegf4)
        depf4=line[38:42]
        depf4=float(depf4)/1000
        a=[[staf4,ladegf4,lodegf4,depf4]]
        dfj=pd.DataFrame(a, columns=['sta','lat','lon','dep'])
        dfi=dfi.append(dfj)
f4.close()
dfistring=dfi.to_string(header=0,index=0)
f5=open('stationinfo.t','w')
f5.write(dfistring)
f5.close()



####calculates/#prints the lat, lon and time for each station in each event file stores in data frame dfl but may need a data frame for each file??? 
 ####also creates a new file for each event where the new information will be stored 
### checks to see if event outside lat/long/dep parameters, also checks to see if tt difference is less than 0sec and more than 100sec. Will print out what event file needs to be removed from FMTOMO sources file
h=0
m=0
q=0
evt=[]
p=0
lm=lt-1
format1=lambda x:'%.4f'%x
format2=lambda x:'%.3f'%x
format3=lambda x:'%-5s'%x
format4=lambda x:'%.2f'%x
f6=open('sources.in', 'w')
f6.write('%s\n' %lm)
f7=open('eventlist.t', 'w')
f9=open('sourceswa.in','w')

for h in range(lm):
	dfl=pd.DataFrame()
	dfq=pd.DataFrame()
        f2=open('EQ%s.txt' %h)
        fl=f2.readline().strip()
	depeq=fl[38:42]
	depeq=depeq.replace(' ','0')
	#depeq=float(depeq)/100
	if depeq == '0000':
		continue
        date=fl[0:8]
        timet=fl[10:20]
        timeh=fl[10:12]
        timeh=timeh.replace(' ','0')
        timeh=float(timeh)*3600
        timem=fl[12:14]
        timem=timem.replace(' ','0')
        timem=float(timem)*60
        times=fl[14:20]
        time=float(timem)+float(timeh)+float(times)
        lat=fl[23:30]
	lat=lat.replace(' ','0')
	if lat < '15' or lat > '22':
		print 'lat'
		continue
        lon=fl[30:38]
	lon=lon.replace(' ','0')
	if lon > '100' or lon < '-64' or lon > '-78':
		print 'lon'
		continue 
        depeq=fl[38:42]
	depeq=depeq.replace(' ','0')
	#depeq=float(depeq)/100
	if depeq == '0000':
		continue
	f7.write('%s %s %s %s\n' %(h, lat, lon, depeq))
	if depeq < '1':
		f6.write('%s %s %s\n' %(lat, lon, 1.0))
	else: 	
        	f6.write('%s %s %s\n' %(lat, lon, depeq))
	p=p+1
        f6.write('1\n')
	if depeq >= '40':
		f6.write('1 1 EQF%s.txt\n' %(h))
      	else: 
        	f6.write('2 1 EQF%s.txt\n' %(h))
        f3=open('EQF%s.txt' %h, 'w')
        nl=sum(1 for line in open("EQ%s.txt" %h))
        for line in f2:
		ind=line[79:80]
		ind=ind.replace(' ','0')
                if line.strip() and fnmatch.fnmatch(ind,'0'):
                        staf2=line[0:6]
                        staf2=staf2.strip()
                        comp=line[10:11]
                        th=line[18:20]
                        th=th.replace(' ','0')
                        th=float(th)*3600              
                        tm=line[20:22]
                        tm=float(tm)*60     
                        ts=line[22:26]
                        ts=ts.replace(' ','0')
                        tf=float(th)+float(tm)+float(ts)
                        tdiff=float(tf)-float(time)
			if tdiff < 0 or tdiff > 150:
				continue
                        b=[[staf2,comp,time,tf,tdiff]]
                        dfm=pd.DataFrame(b, columns=['sta','comp','evtt','stat','oritt'])
                        dfl=dfl.append(dfm)
			f10.write('%s %s %s %s\n' %(staf2, time, tf, tdiff))
			leng=len(dfl)
			dfq=pd.DataFrame()
			dfw=pd.DataFrame()
	if dfl.empty == True:
		print 'remove EQ%s' %h 
		continue
        for m in range(leng):
                for q in range(num_linesf4):
                        if dfi.iat[q,0] == dfl.iat[m,0] and dfl.iat[m,1] == 'P':
				unc=0.15
                                d=[[dfi.iat[q,1],dfi.iat[q,2],dfi.iat[q,3],dfl.iat[m,4],unc]]
                                dfw=pd.DataFrame(d, columns=['lat','lon','dep','otime','unc'])
                                dfq=dfq.append(dfw)
                                dfstring=dfq.to_string(header=0,index=0,formatters={'lat':format1,'lon':format1,'dep':format2,'otime':format4,'unc':format4})
                        q=q+1
                m=m+1
        del dfw
	del dfl
	del dfm	
	del leng
	f2.close()

 	rows=len(dfq.index)
     	f3.write('%s\n' %rows)
        f3.write(dfstring)               
	f3.close()
        del dfq
f6.close
f6=open('sources.in','r')
print p
f6.readline() # and discard
f9.write('%s\n' %p)
shutil.copyfileobj(f6, f9)

f7.close()



