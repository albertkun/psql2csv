#import modules
import psycopg2, csv, sys,os

#connect to the server
try:
    conn = psycopg2.connect("host='ENTERHOST dbname='ENTERDATABASE'"
                            "user='ENTERUSERNAME' password='ENTERDATABASEPASSWORD'")
except:
    print "Unable to connect to database, please check your internet connection settings."
#cursor for the data
cur = conn.cursor()

#ask the user to apply any queries
sqlFlag = raw_input("Will you apply a SQL query? [y/n] \n")

#handler for sql queries
if sqlFlag == 'y':
    userSQL = raw_input("Please put your valid SQL here: \n")
    userQuery = "("+userSQL+")"
else:
    print "Warning: You will be downloading the whole data table."
    userQuery = raw_input("Please put the name of the table \n")

#holder for the query                      
copy_sql = """
            COPY """+userQuery+""" TO STDOUT WITH CSV HEADER
            DELIMITER as ','
            """
#ask for file name
filename = str(raw_input("What do you want the output file name to be?\n"))

#choose the csv file
theFile = "./"+filename+'.csv'
f = open(theFile,'w+')

#try to execute the copy
try:  
    cur.copy_expert(copy_sql,f)
    print "Query successful"
except:
    raw_input("There was an issue. Press enter to exit.")
    f.close()
    os.remove(theFile)
    sys.exit(0) # exit the script

#close out the connections
conn.commit()
cur.close()
f.close()
conn.close()

print "CSV file exported as " + theFile
print "Task completed."
