# FMTOMOscripts
Set of python scripts written to convert various pick file formats, ie SEISAN and PRSN, to pick and source files for input into FMTOMO.
eqseisanmod.py -- takes SEISAN phase pick input catalog and outputs seperated event files, one with the input event/station information (ie EQ1.txt), the second the pick format used in FMTOMO (ie EQF1.txt). It also outputs the sourceswa.in file that points to the pick files in FMTOMO. A little prep still needs to be done before feeding into FMTOMO - the EQF text files need to be moved to the picks folder. The python script also outputs   
