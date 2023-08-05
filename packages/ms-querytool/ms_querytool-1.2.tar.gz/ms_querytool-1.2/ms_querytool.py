'''
Author: Marc Stumbo
Version: 1.2
Origin Date: 12-07-2017
Last Update Date: 05-07-2019  Improved error handling, added log to console, added start_from for re-run
'''
import re
import pyodbc
import pandas as pd
import logging
import datetime
import os
import sys

def parse_sql(filenm):
    '''
    filenm: string containing the location of the file with the SQL text
    '''
    sqlFile = open(file=filenm, mode='r')
    sqlTXT = sqlFile.read()
    sqlFile.close()
    sqlTXT = re.sub(r'(--.*?\n)',repl='', string=sqlTXT)
    sqlTXT = sqlTXT.replace('\n', ' ')
    sqlTXT = sqlTXT.replace('\t', ' ')
    sqlTXT = re.sub(pattern=r'/\*.*?\*/',repl='', string=sqlTXT)
    sqlTXT = re.sub(pattern=' {2,}', repl=' ', string=sqlTXT)
    sqlTXT= re.sub(pattern='( ,)', repl=',', string=sqlTXT)
    sqlTXT= re.sub(pattern='( ;)', repl=';', string=sqlTXT)
    sqlTXT= re.sub(pattern='(; )', repl=';', string=sqlTXT)
    sqlTXT= re.sub(pattern=';$', repl='', string=sqlTXT)
    statement_list = sqlTXT.split(';')

    sql_statements = []
    sql_types = []
    statement_index = 0
    sql_category = {r'(CREATE.*?TABLE.*?AS )':'CREATE', r'^(COLLECT )':'COLLECT', r'^(GRANT )':'GRANT', r'^(WITH )':'WITH', 
                    r'^(UPDATE )':'UPDATE', r'^(DELETE )':'DELETE', r'^(INSERT )':'INSERT', r'^(DROP )':'DROP', r'^(COMMENT )':'COMMENT',
                    r'^(SEL )':'SELECT', r'^(SELECT )':'SELECT'}

    for statement in statement_list:
        statement = statement.upper()
        for cat in sql_category:
            if cat == '(CREATE.*?TABLE.*?AS )':
                if re.findall(pattern=cat, string=statement):
                    createNew = re.findall(pattern=cat, string=statement)
                    createNew = re.sub(r'(, NO FALLBACK, NO BEFORE JOURNAL, NO AFTER JOURNAL)', ' ', createNew[0])
                    createNew = re.sub(' AS','',createNew)
                    createNew = re.sub(r'(CREATE.*?TABLE )','',createNew)
                    createNew = 'DROP TABLE {t}'.format(t=createNew)
                    sql_statements.insert(statement_index,createNew+';')
                    sql_types.insert(statement_index, 'DROP (auto)')
                    statement_index +=1
                    sql_statements.insert(statement_index, statement+';')
                    sql_types.insert(statement_index, sql_category[cat])
                    statement_index +=1
                         
            elif re.findall(pattern=cat, string=statement):
                sql_statements.insert(statement_index, statement+';')
                sql_types.insert(statement_index, sql_category[cat])
                statement_index +=1
        if statement+';' not in sql_statements:
            sql_statements.insert(statement_index, statement+';')
            sql_types.insert(statement_index, 'OTHER')
            statement_index +=1
            
    return (sql_statements, sql_types)

def runTheSQL(odbc, sql_txt, logFile, start_from):
    '''
    odbc: string containing the name of the ODBC connection to use (ex: DSN=NTL_PRD_ALLVM)
    sql_txt: string on where the text file is located with the SQL text
    logFile: string where the log file will be saved
         '{pathToFile}\{logName}.log'.format(pathToFile=os.getcwd(), logName=os.path.basename(sys.argv[0][:-3]))
    '''
    
    logging.info('Getting the SQL file.')
    sql_results = {}
    logging.info('Parsing the SQL text')
    sql_list = parse_sql(sql_txt)
    logging.info('{n} statements found or generated.'.format(n=len(sql_list[1])))
    conn = pyodbc.connect(odbc)
    logging.info("Connected to {o}".format(o=odbc))

    if start_from == 0:
        start_from_sql = 0
    else:
        start_from_sql = start_from-1
    
    select_num = 1
    for i in range(start_from_sql, len(sql_list[0])):
        with conn.cursor() as cur:
            logging.info('Running SQL Statement {n}: {s} statement {spaces}--> {sql_detail}'.format(n=str(i+1).zfill(2), s=sql_list[1][i], spaces=' '*(15 - len(str(i+1).zfill(2)) - len(sql_list[1][i])), sql_detail=sql_list[0][i]))
            
            if sql_list[1][i][:4] == 'DROP':
                try:
                    cur.execute(sql_list[0][i])
                except pyodbc.Error as ex:
                    sqlstate = ex.args[0]
                    if sqlstate == '42S02':
                        logging.info("    Table does not exist, safe to CREATE")
                    elif sqlstate == 'HY000':
                        logging.error('    Error: No more spool space')
                        sys.exit('Error running SQL, see log file for details.')
                    else:
                        logging.error('    Error running SQL Statement')
                        sys.exit('Error running SQL, see log file for details.')
                except Exception as e:
                    logging.error('    Error running SQL Statement')
                    sys.exit('Error running SQL, see log file for details.')
            elif sql_list[1][i] != 'SELECT':
                try:
                    cur.execute(sql_list[0][i])
                except pyodbc.Error as ex:
                    sqlstate = ex.args[0]
                    logging.error('    Error: {x}'.format(x=ex))
                    sys.exit('Error running SQL, see log file for details.')
                except Exception as e:
                    logging.error('    Error running SQL Statement')
                    sys.exit('Error running SQL, see log file for details.')
                    
            else:
                sql_results['SELECT {num}'.format(num=str(select_num).zfill(2))] = pd.read_sql(sql_list[0][i], conn)
                select_num +=1

    conn.close()
    logging.info('All SQL Statements Processed.')
    return sql_results

def queryTool(sql_dict, logFileNm=os.getcwd()+'\\default_log_file.log', start=0):
    '''
    queryTool:
        1. Parses the txt file for all SQL statements, then runs them sequentially
        2. returns a dictionary of all SELECT statements found in the SQL text files passed to it
    INPUTS
    sql_dict: Dictionary in the format {'full file path location of SQL txt file': 'DSN=ODBC connection name'}
    logFileNm: location of the log file being used
    start: SQL statement in the file you wish to start from, if not 0 or the beginning (mostly for re-running a script without duplicating work)
    '''
    logging.basicConfig(level=logging.DEBUG, filename=logFileNm, filemode="a+", format="%(asctime)-15s %(levelname)-8s %(message)s", datefmt='%Y-%m-%d %H:%M:%S %p')
    console = logging.StreamHandler()
    console.flush()
    console.setFormatter(logging.Formatter('%(asctime)-15s: %(levelname)-8s %(message).50s', datefmt='%Y-%m-%d %H:%M:%S %p'))
    logging.getLogger('').addHandler(console)
    
    sql_results = {}
    for key, value in sql_dict.items():
        result_set = 1
        logging.info('Running SQL Text File from: {f}'.format(f=key))
        sql_results[os.path.splitext(os.path.basename(key))[0]] = runTheSQL(odbc=value, sql_txt=key, logFile=logFileNm, start_from=start)
        result_set += 1
        logging.info('SQL Completed: SELECT Results saved to dictionary object')

    sql_output = {}
    for k1, v1 in sql_results.items():
        if type(sql_results[k1]) == dict:
            for k2, v2 in sql_results[k1].items():
                sql_output['{sql} {select}'.format(sql=k1, select=k2[-2:])] = v2
        else:
            sql_output['{sql} {select}'.format(sql=k1, select=k1[-2:])] = v1
    logging.info('SQL Output: SQL dictionary reformatted to 1 tier')
    logging.getLogger('').removeHandler(console)
    return sql_output

def qt_to_excel(sql_output, xlFileNm):
    try:
        xl_file = xlFileNm
        logging.info('Saving the new data set to Excel file: {xl}'.format(xl=xl_file))
        writer = pd.ExcelWriter(xl_file, engine='openpyxl')
        for k, v in list(sql_output.items())[::-1]:
            sql_output[k].to_excel(writer, index=False, engine='openpyxl', sheet_name=k)
        writer.save()
        writer.close()
        logging.info('Excel file saved: {f}'.format(f=xlFileNm))
        return True
    except Exception as e:
        logging.info('    Error writing to Excel: {ex}'.format(ex=e))
        return False
    
