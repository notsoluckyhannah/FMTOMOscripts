# FMTOMOscripts
Set of python scripts written to convert various pick file formats, ie SEISAN and PRSN, to pick and source files for input into FMTOMO.
eqseisanmod.py -- takes SEISAN phase pick input catalog (ie catalog.t) and outputs seperated event files, one with the input event/station information (ie EQ1.txt), the second the pick format used in FMTOMO (ie EQF1.txt). It also outputs the sources file that is used when running obsdata in FMTOMO (ie sourceswa.in). A little prep still needs to be done before feeding into FMTOMO - the EQF text files need to be moved to the picks folder. The python script also outputs the travel time calculations for each station. 
eqmakemod.py -- takes PRSN phase pick input catalog (ie origevent.t) and outputs seperated event files, one with the input event/station information (ie EQK1.txt), the second the pick format used in FMTOMO (ie EQM1.txt). It also outputs the sources file that is used when running obsdata in FMTOMO (ie sourceswa1.in). A little prep still needs to be done before feeding into FMTOMO - the EQM text files need to be moved to the picks folder. The python script also outputs the station information, number of events per station, and 2 event files. 
Both scripts currently read in station files with locations in degrees decimal minute format with direction denoted by N or W (see hypinv.sta and/or stations.t). 
Currently, both scripts also have a Moho fixed at 40km. 
Also included is a python script to generate a depth histogram from the sourceswa.in file.


FUTURE WORK:
Prompt for user input on Moho depth and input/output filenames.
Create pick folder for picks. 
