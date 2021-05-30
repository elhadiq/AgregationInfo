import codecs
import mysql.connector
from mysql.connector.fabric import connect
def se_connecter():
    connection=mysql.connector.connect(
    host = "localhost " ,
    user = "root",
    password="root",
    auth_plugin='mysql_native_password'
    )
    return connection
def creationDb(connection):        
    cursor=connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS TP_SQL;")
    cursor.execute("use TP_SQL")
    cursor.close()

def creationTables(connection):
    cursor=connection.cursor()
    cursor.execute("""create table if not exists dept(
        ND int primary key, nom varchar(20), ville varchar(20))
        """)
    cursor.execute(
    """ create table if not exists emp(
        NE int primary key,
        nom varchar(20),
        fonction varchar(20),
        NEchef int,
        dateEmb date,
        sal float check(sal between 0 and 100000),
        comm float check(comm >0 OR comm=NULL),
        ND int ,
        foreign key (ND) references dept(ND)
        )
    """)
    cursor.execute("alter table emp add constraint foreign key(NEchef) references emp(NE)")
    cursor.close()

dataDept=[(10,'Comptabilite','RABAT'),
(20,'Recherche','MARRAKECH'),
(30,'Vente','CASABLANCA'),
(40,'Operations','AGADIR')
]
dataEmp=[
(7839,'YASSINE','PRESIDENT',None,"2006/11/17",5000,None,10),
(7698,'JAOUAD','MANAGER',7839, '2006/05/01',2850,None,30),
(7782,'MOHAMED','MANAGER',7839, '2006/06/09',2450,None,10),
(7566,'ABDELKARIM','MANAGER',7839,'2006/04/02',2975,None,20),
(7654,'IDRISS','VENDEUR',7698, '2006/09/28',1250,1400,30),
(7499,'KAMAL','VENDEUR',7698,'2006/02/20',1600,300,30),
(7844,'TOURIYA','VENDEUR',7698,'2006/09/08',1500,0,30),
(7900,'SANA','SECRITAIRE',7698,'2006/12/03', 950,None,30),
(7521,'SOAD','VENDEUR',7698,'2006/02/22',1250,500,30),
(7902,'MUSTAPHA','ANALYSTE',7566,'2006/03/12',3000,None,20),
(7369,'ABDELILAH','SECRITAIRE',7902,'2005/02/17',800,None,20),
(7788,'ABDESSAMAD','ANALYSTE',7566,'2007/09/12',3000,None,20),
(7876,'JAMAL','SECRITAIRE',7788,'2008/01/12',1100,None,20)
]
def insertionToDept(connection,data):  
    cursor=connection.cursor() 
    insertToDept="""insert into dept(ND, nom ,ville) values (%s,%s,%s)"""
    cursor.executemany(insertToDept,data)
    cursor.close()
def insertIntoEmp(connection,data):
    cursor=connection.cursor() 
    insertIntoEmp="""insert into emp(NE, nom, fonction, NEchef, dateEmb, sal, comm, ND) values (%s,%s,%s,%s,%s,%s,%s,%s)"""
    cursor.executemany(insertIntoEmp,data)
    cursor.close()
def dropTables(connection):
    cursor=connection.cursor()
    cursor.execute("use TP_SQL")
    cursor.execute("drop table if exists emp")
    cursor.execute("drop table if exists dept")
    cursor.close()
def affiche_employe(connection,NE):
    cursor=connection.cursor()
    print("select * from emp where NE={}".format(NE))
    cursor.execute("select * from emp INNER JOIN dept on emp.ND=dept.ND where NE={}".format(NE))
    print(cursor.fetchall())
    cursor.close()
connection=se_connecter()
dropTables(connection)
creationTables(connection)
insertionToDept(connection,dataDept)
insertIntoEmp(connection,dataEmp)
affiche_employe(connection,7900)
connection.commit()
connection.close()