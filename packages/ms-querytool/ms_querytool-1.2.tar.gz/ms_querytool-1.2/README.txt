MS_QueryTool

The purpose of this package is to compile a set of functions to mirror the QueryTool built in Excel.
The script has 2 inputs:
	1) a python dictionary of txt files containing SQL {'location of txt file': 'DSN=ODBC_name'}
	2) the location of the log file to use in logging, default is a .log file of the same name as input file in same folder

The script has multiple outputs:
	1) querytool - outputs a python dictionary containing the results of the SELECT statements in the txt files supplied
	2) qt_to_excel - saves the results of the querytool dictionary to an excel file
