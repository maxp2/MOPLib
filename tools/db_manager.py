#!/usr/bin/python3

import logging
logger = logging.getLogger(__name__)
log_formatter = logging.Formatter('%(name)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')
logger.setLevel(logging.DEBUG) #for all messages

log_stdout_handler = logging.StreamHandler()
log_stdout_handler.setFormatter(log_formatter)
logger.addHandler(log_stdout_handler)

import sqlite3

con = sqlite3.connect("./database.db")
cur = con.cursor()

db_schema_v1 = """
CREATE TABLE parts(
part_DBID        INTEGER NOT NULL UNIQUE,
manufacturer     TEXT NOT NULL,
manufacturer_PN  TEXT NOT NULL,
PN_alt1          TEXT,
PN_alt2          TEXT,
Digikey_PN       TEXT,
Mouser_PN        TEXT,
part_status      TEXT,
description      TEXT,
packaging        TEXT,
CAD_link0        INTEGER,
CAD_link1        INTEGER,
CAD_link2        INTEGER,
CAD_link3        INTEGER,
CAD_link4        INTEGER,
CAD_link5        INTEGER,
CAD_link6        INTEGER,
CAD_link7        INTEGER,
CAD_link8        INTEGER,
CAD_link9        INTEGER,
CAD_link10       INTEGER,
CAD_link11       INTEGER,
CAD_link12       INTEGER,
CAD_link13       INTEGER,
CAD_link14       INTEGER,
CAD_link15       INTEGER,
CAD_link16       INTEGER,
CAD_link17       INTEGER,
CAD_link18       INTEGER,
CAD_link19       INTEGER,
CAD_link20       INTEGER,
CAD_link21       INTEGER,
CAD_link22       INTEGER,
CAD_link23       INTEGER,
CAD_link24       INTEGER,
CAD_link25       INTEGER,
CAD_link26       INTEGER,
CAD_link27       INTEGER,
CAD_link28       INTEGER,
CAD_link29       INTEGER,
CAD_link30       INTEGER,
CAD_link31       INTEGER,
PRIMARY KEY (part_DBID ASC));
CREATE TABLE CAD_data(
CAD_DBID            INTEGER NOT NULL UNIQUE,
full_path           TEXT NOT NULL,
author              TEXT,
file_release_ID     TEXT,
type                TEXT,
PRIMARY KEY (CAD_DBID ASC));
"""
#cur.executescript(db_schema_v1)

class part:
    def __init__(self, part_DBID):
        self.part_DBID           = part_DBID
        self.manufacturer        = ""
        self.manufacturer_PN     = ""
        self.PN_alt1             = ""
        self.PN_alt2             = ""
        self.Digikey_PN          = ""
        self.Mouser_PN           = ""
        self.part_status         = ""
        self.description         = ""
        self.packaging           = ""
        self.CAD_data            = []
    def __str__(self):
        temp_str=""
        temp_str+="\npart_DBID      :"+str(self.part_DBID)
        temp_str+="\nmanufacturer   :"+self.manufacturer   
        temp_str+="\nmanufacturer_PN:"+self.manufacturer_PN
        temp_str+="\nPN_alt1        :"+self.PN_alt1        
        temp_str+="\nPN_alt2        :"+self.PN_alt2        
        temp_str+="\nDigikey_PN     :"+self.Digikey_PN     
        temp_str+="\nMouser_PN      :"+self.Mouser_PN      
        temp_str+="\npart_status    :"+self.part_status    
        temp_str+="\ndescription    :"+self.description    
        temp_str+="\npackaging      :"+self.packaging      
        
        CAD_links=[]
        for item in self.CAD_data:
            CAD_links.append(item.CAD_DBID)
        
        temp_str+="\nCAD_data       :"+str(CAD_links)
        return temp_str
    #Support for sets not assumed across implementations
    #Hashing objects can also be vague
    def sort_CAD_data():
        #Extract IDs
        CAD_links=[]
        for item in self.CAD_data:
            CAD_links.append(item.CAD_DBID)
        #Sort by ID
        CAD_links.sort()
        us_CAD_data=self.CAD_data
        #Generate sorted list
        s_CAD_data=[]
        for link in CAD_links:
            for item in us_CAD_data:
                if(link == item.CAD_DBID):
                    s_CAD_data.append(item)
        self.CAD_data=s_CAD_data
    def eq_fields(self,other):
        if(other == None):
            return False
        if(self.manufacturer       != other.manufacturer   ):
            return False
        if(self.manufacturer_PN    != other.manufacturer_PN):
            return False
        if(self.PN_alt1            != other.PN_alt1        ):
            return False
        if(self.PN_alt2            != other.PN_alt2        ):
            return False
        if(self.Digikey_PN         != other.Digikey_PN     ):
            return False
        if(self.Mouser_PN          != other.Mouser_PN      ):
            return False
        if(self.part_status        != other.part_status    ):
            return False
        if(self.description        != other.description    ):
            return False
        if(self.packaging          != other.packaging      ):
            return False
        return True
    def eq_links(self,other):
        if(other == None):
            return False
        if(len(self.CAD_data)      != len(other.CAD_data)  ):
            return False
        for index in range(0, len(self.CAD_data)):
            if(self.CAD_data[index] != other.CAD_data[index]):
                return False
        return True
    def __eq__(self, other):
        if(other == None):
            return False
        if(self.part_DBID != other.part_DBID):
            return False
        if(not self.eq_fields(other)):
            return False
        if(not self.eq_links(other)):
            return False
        return True
    def eq_nDBID(self, other):
        if(other == None):
            return False
        if(not self.eq_fields(other)):
            return False
        if(not self.eq_links(other)):
            return False
        return True

class CAD_datum:
    def __init__(self, CAD_DBID):
        self.CAD_DBID           =CAD_DBID
        self.full_path          =""
        self.author             =""
        self.file_release_ID    =""
        self.type               =""
    def diff(self, other):
        temp_str=""
        if(self.CAD_DBID != other.CAD_DBID):
            temp_str+"CAD_DBID"+str(self.CAD_DBID) +"!="+ str(other.CAD_DBID)+"\n"
        if(self.full_path != other.full_path):
            temp_str+"full_path"+str(self.full_path) +"!="+ str(other.full_path)+"\n"
        if(self.full_path != other.full_path):
            temp_str+"author"+str(self.author) +"!="+ str(other.author)+"\n"
        if(self.file_release_ID != other.file_release_ID):
            temp_str+"file_release_ID"+str(self.file_release_ID) +"!="+ str(other.file_release_ID)+"\n"
        if(self.type != other.type):
            temp_str+"type"+str(self.type) +"!="+ str(other.type)+"\n"
    
    def __str__(self):
        temp_str=""
        temp_str+="\nCAD_DBID       :"+str(self.CAD_DBID)
        temp_str+="\nfull_path      :"+self.full_path
        temp_str+="\nauthor         :"+self.author
        temp_str+="\nfile_release_ID:"+self.file_release_ID
        temp_str+="\ntype           :"+self.type
        return temp_str
    
    def eq_fields(self,other):
        if(other == None):
            return False
        if(self.full_path       != other.full_path):
            return False
        if(self.author          != other.author):
            return False
        if(self.file_release_ID != other.file_release_ID):
            return False
        if(self.type            != other.type):
            return False
        return True
    
    def __eq__(self, other):
        if(other == None):
            return False
        if(self.CAD_DBID        != other.CAD_DBID):
            return False
        if(not self.eq_fields(other)):
            return False
        return True
    
    def eq_nDBID(self, other):
        if(other == None):
            return False
        if(not self.eq_fields(other)):
            return False
        return True
"""
-- Useful search queries
SELECT * FROM parts WHERE remote_datasheet IS NOT NULL"
SELECT * FROM CAD_data WHERE full_path LIKE '%OPA%' AND type LIKE 'Siemens%'
SELECT part_DBID, manufacturer, manufacturer_PN, description FROM parts WHERE description LIKE '%res%'

--For manual deduplicating
SELECT manufacturer FROM parts GROUP BY manufacturer
SELECT manufacturer_PN, description FROM parts GROUP BY manufacturer_PN
"""

#Returns None on failure and a CAD_datum object on success
def CAD_datum_from_db(CAD_DBID):
    if(CAD_datum == None):
        logger.error("Bad input")
        return None
    temp_str="SELECT * FROM CAD_data WHERE CAD_DBID=?"
    #for index in CAD_indices[1:]:
    #    temp_str+=" OR CAD_index="+str(index)
    
    logger.debug(temp_str +str(CAD_DBID))
    db_res = cur.execute(temp_str, (CAD_DBID,)).fetchone()
    
    if(db_res == None):
        logger.error("Bad CAD_DBID="+str(CAD_DBID))
        return None
    
    result = CAD_datum(db_res[0])
    result.full_path          =db_res[1]
    result.author             =db_res[2]
    result.file_release_ID    =db_res[3]
    result.type               =db_res[4]
        
    return result

#Returns True on success
def CAD_datum_to_db(CAD_datum, overwrite=False):
    #No "UPDATE parts SET column1 = value1, column2 = value2, ... WHERE condition; " since no delta algorithm implemented
    
    if(CAD_datum == None):
        logger.error("Bad input")
        return False
    
    exists = (CAD_datum_from_db(CAD_datum.CAD_DBID) != None)
    if(exists):
        temp_str="CAD_datum with CAD_DBID="+str(CAD_datum.CAD_DBID)+" already exists."
        if(not overwrite):
            logger.warning(temp_str+" Overwrite blocked.")
            return False
        else:
            logger.warning(temp_str+" Overwriting.")
            statement = "DELETE FROM CAD_data WHERE CAD_DBID=?"
            data=(CAD_datum.CAD_DBID,)
            logger.debug(statement+str(data))
            cur.execute(statement, data)
            
    columns="""(
    CAD_DBID            ,
    full_path           ,
    author              ,
    file_release_ID     ,
    type) 
    """
    qms="(?,?,?,?,?)"
    statement = "INSERT INTO CAD_data "+columns+" VALUES "+qms
    data=(CAD_datum.CAD_DBID,
    CAD_datum.full_path,
    CAD_datum.author,
    CAD_datum.file_release_ID,
    CAD_datum.type,)
    
    logger.debug(statement + str(data))
    cur.execute(statement, data)
    con.commit()
    return True

def part_from_db(part_DBID, keep_bad_CAD_links=True, keep_duplicate_links=True):
    if(part_DBID == None):
        logger.error("Bad input")
        return None
    
    temp_str="SELECT * FROM parts WHERE part_DBID=?"
    #for index in CAD_indices[1:]:
    #    temp_str+=" OR CAD_index="+str(index)
    
    logger.debug(temp_str + str(part_DBID))
    
    db_res = cur.execute(temp_str, (part_DBID,)).fetchone()
    if(db_res == None):
        logger.error("Bad part_DBID="+str(part_DBID))
        return None
    else:
        result = part(db_res[0])
        result.manufacturer     =db_res[1 ]
        result.manufacturer_PN  =db_res[2 ]
        result.PN_alt1          =db_res[3 ]
        result.PN_alt2          =db_res[4 ]
        result.Digikey_PN       =db_res[5 ]
        result.Mouser_PN        =db_res[6 ]
        result.part_status      =db_res[7 ]
        result.description      =db_res[8 ]
        result.packaging        =db_res[9 ]
    
    result.CAD_data=[]
    links=db_res[10:42]
    
    if(not keep_duplicate_links):
        links=list(set(links))
    
    for link in links:
        if(link == '' or link == 0):
            pass
        else:
            datum=CAD_datum_from_db(link)
            if (datum == None and keep_bad_CAD_links):
                result.CAD_data.append(CAD_datum(link))
            else:
                result.CAD_data.append(datum)    
   
    return result

#Linked CAD datums must already exist in the database - users responsibility
def part_to_db(part, overwrite=False):
    exists = (cur.execute("SELECT * FROM parts WHERE part_DBID=?", (part.part_DBID,)).fetchone() != None)
    if(exists):
        temp_str="Part with part_DBID="+str(part.part_DBID)+" already exists."
        if(not overwrite):
            logger.warning(temp_str+" Overwrite blocked.")
            return False
        else:
            logger.warning(temp_str+" Overwriting.")
            statement = "DELETE FROM parts WHERE part_DBID=?"
            data=(part.part_DBID,)
            logger.debug(statement+str(data))
            cur.execute(statement, data)
    
    for item in part.CAD_data:
        if (cur.execute("SELECT * FROM CAD_data WHERE CAD_DBID=?", (item.CAD_DBID,)).fetchone() == None):
            logger.error("Linked CAD_datum with CAD_DBID="+str(item.CAD_DBID)+" does not exist")
            return False
    
    #Prepare
    db_links=[]
    for item in part.CAD_data:
        db_links.append(item.CAD_DBID)
    db_links.sort()
    
    if(len(db_links)>32):
        logger.error("Too many CAD links")
        return False
    
    for i in range(len(db_links),32):
        db_links.append(0)
    
    columns="""(
    part_DBID      ,
    manufacturer   ,
    manufacturer_PN,
    PN_alt1        ,
    PN_alt2        ,
    Digikey_PN     ,
    Mouser_PN      ,
    part_status    ,
    description    ,
    packaging      ,
    CAD_link0      ,
    CAD_link1      ,
    CAD_link2      ,
    CAD_link3      ,
    CAD_link4      ,
    CAD_link5      ,
    CAD_link6      ,
    CAD_link7      ,
    CAD_link8      ,
    CAD_link9      ,
    CAD_link10     ,
    CAD_link11     ,
    CAD_link12     ,
    CAD_link13     ,
    CAD_link14     ,
    CAD_link15     ,
    CAD_link16     ,
    CAD_link17     ,
    CAD_link18     ,
    CAD_link19     ,
    CAD_link20     ,
    CAD_link21     ,
    CAD_link22     ,
    CAD_link23     ,
    CAD_link24     ,
    CAD_link25     ,
    CAD_link26     ,
    CAD_link27     ,
    CAD_link28     ,
    CAD_link29     ,
    CAD_link30     ,
    CAD_link31     ) 
    """
    qms="(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    data=(
    part.part_DBID      ,
    part.manufacturer   ,
    part.manufacturer_PN,
    part.PN_alt1        ,
    part.PN_alt2        ,
    part.Digikey_PN     ,
    part.Mouser_PN      ,
    part.part_status    ,
    part.description    ,
    part.packaging      ,
    db_links[0]         ,
    db_links[1]         ,
    db_links[2]         ,
    db_links[3]         ,
    db_links[4]         ,
    db_links[5]         ,
    db_links[6]         ,
    db_links[7]         ,
    db_links[8]         ,
    db_links[9]         ,
    db_links[10]        ,
    db_links[11]        ,
    db_links[12]        ,
    db_links[13]        ,
    db_links[14]        ,
    db_links[15]        ,
    db_links[16]        ,
    db_links[17]        ,
    db_links[18]        ,
    db_links[19]        ,
    db_links[20]        ,
    db_links[21]        ,
    db_links[22]        ,
    db_links[23]        ,
    db_links[24]        ,
    db_links[25]        ,
    db_links[26]        ,
    db_links[27]        ,
    db_links[28]        ,
    db_links[29]        ,
    db_links[30]        ,
    db_links[31]        ,)
    statement = "INSERT INTO parts "+columns+" VALUES "+qms
    logger.debug(statement + str(data))
    cur.execute(statement, data)
    con.commit()

def pretty_print_CAD_data(CAD_data):
    temp_str="\n"
    for item in CAD_data:
        temp_str+=str(item.CAD_DBID)    + " | "
        temp_str+=str(item.type)        + " | "
        temp_str+=str(item.full_path)   + " | \n"
    logger.info(temp_str)

#0 reserved as placeholder
def new_CAD_DBID():
    db_res = cur.execute("SELECT MAX(CAD_DBID) FROM CAD_data").fetchone()[0]
    if (db_res == None):
        db_res = 0
    return db_res + 1

#0 reserved as placeholder
def new_part_DBID():
    db_res = cur.execute("SELECT MAX(part_DBID) FROM parts").fetchone()[0]
    if (db_res == None):
        db_res = 0
    return  db_res + 1

def import_from_old_db():
    
    old_con = sqlite3.connect("./old_database.db")
    cur2 = old_con.cursor()
    cur3 = old_con.cursor()
    
    script="\n--Rereference\n"
    temp_str="""
    ALTER TABLE CAD_data ADD COLUMN new_CAD_DBID INTEGER;
    ALTER TABLE parts ADD COLUMN new_part_DBID INTEGER;
    """
    old_con.executescript(temp_str)
    CAD_DBID = new_CAD_DBID()
    logger.debug(CAD_DBID)
    input()
    for db_res in cur2.execute("SELECT CAD_index FROM CAD_data"):
        script+="UPDATE CAD_data SET new_CAD_DBID="+str(CAD_DBID)+" WHERE CAD_index="+str(db_res[0])+";\n"
        for linki in range(0,32):
            script+="UPDATE parts SET CAD_link"+str(linki)+"="+str(CAD_DBID)+" WHERE CAD_link"+str(linki)+"="+str(db_res[0])+";\n"
        CAD_DBID+=1
    
    part_DBID = new_part_DBID()
    for db_res in cur2.execute("SELECT part_index FROM parts"):
        script+="UPDATE parts SET new_part_DBID="+str(part_DBID)+" WHERE part_index="+str(db_res[0])+";\n"
        part_DBID+=1
    logger.debug(script)
    f=open("./remapscript.sql","w")
    f.write(script)
    f.close()
    logger.debug(script)
    input("Verify DBID remap script. Press enter to continue")
    old_con.executescript(script)
    input("Verify new DBIDs. Press enter to continue")
    
    #Remap and copy CAD_data
    debug_flag=True
    for db_res in cur3.execute("SELECT * from CAD_data"):
            d = CAD_datum(db_res[5])
            d.full_path          =db_res[1]
            d.author             =db_res[2]
            d.file_release_ID    =db_res[3]
            d.type               =db_res[4]
            
            if(debug_flag):
                logger.debug(d)
                input("Verify CAD_datum mapping. Press enter to continue")
                debug_flag=False
            CAD_datum_to_db(d)
    
    #Remap and copy parts
    debug_flag=True
    for db_res in cur2.execute("SELECT * from parts"):
        p = part(db_res[42])
        p.manufacturer     =db_res[1 ]
        p.manufacturer_PN  =db_res[2 ]
        p.PN_alt1          =db_res[3 ]
        p.PN_alt2          =db_res[4 ]
        p.Digikey_PN       =db_res[5 ]
        p.Mouser_PN        =db_res[6 ]
        p.part_status      =db_res[7 ]
        p.description      =db_res[8 ]
        p.packaging        =db_res[9 ]
    
        p.CAD_data=[]
        links=db_res[10:42]
    
        for link in links:
            if(link == '' or link == 0):
                pass
            else:
                #Full CAD_datum creaion not needed for part
                #links already updated to new indices
                p.CAD_data.append(CAD_datum(link))
        if(debug_flag):
            logger.debug(p)
            input("Verify part data mapping. Press enter to continue")
            debug_flag=False
        part_to_db(p)
        
    temp_str="""
    ALTER TABLE CAD_data DROP COLUMN new_CAD_DBID;
    ALTER TABLE parts DROP COLUMN new_part_DBID;
    """
    old_con.executescript(temp_str)


#Current implementation loads the entire database into RAM
def find_part_duplicates():
    marked_rows=[]
    for db_res in cur.execute("SELECT part_DBID FROM parts").fetchall():
        marked_rows.append({'obj':part_from_db(db_res[0]),'dupe_group':0})
    for marked_row1 in marked_rows:
        if(marked_row1['dupe_group']!=0):
            pass #Already checked and matched
        else:
            marked_row1['dupe_group']=marked_row1['obj'].part_DBID
            for marked_row2 in marked_rows:
                if(marked_row2['dupe_group']!=0):
                    pass #Already checked and matched
                else:
                    if(marked_row1['obj'].eq_nDBID(marked_row2['obj'])):
                        marked_row2['dupe_group']=marked_row1['obj'].part_DBID
    temp_str="\n--start of exact matches\n"
    for marked_row in marked_rows:
        if(marked_row['dupe_group']==marked_row['obj'].part_DBID):
            temp_str+="--keep "+str(marked_row['obj'].part_DBID)+"\n"
        else:
            temp_str+="DELETE from parts WHERE part_DBID="+str(marked_row['obj'].part_DBID)+" -- duplicate of "+str(marked_row['dupe_group'])+"\n"
            
    #temp_str+="--start of part data duplicates"
    
    logger.info(temp_str)
    return temp_str

def find_CAD_duplicates():
    marked_rows=[]
    for db_res in cur.execute("SELECT CAD_DBID FROM CAD_data").fetchall():
        marked_rows.append({'obj':CAD_datum_from_db(db_res[0]),'dupe_group':0})
    for marked_row1 in marked_rows:
        if(marked_row1['dupe_group']!=0):
            pass #Already checked and matched
        else:
            marked_row1['dupe_group']=marked_row1['obj'].CAD_DBID
            for marked_row2 in marked_rows:
                if(marked_row2['dupe_group']!=0):
                    pass #Already checked and matched
                else:
                    if(marked_row1['obj'].eq_nDBID(marked_row2['obj'])):
                        marked_row2['dupe_group']=marked_row1['obj'].CAD_DBID
    temp_str="\n--start of exact matches\n"
    for marked_row in marked_rows:
        if(marked_row['dupe_group']==marked_row['obj'].CAD_DBID):
            temp_str+="--keep "+str(marked_row['obj'].CAD_DBID)+"\n"
        else:
            temp_str+="DELETE from CAD_data WHERE CAD_DBID="+str(marked_row['obj'].CAD_DBID)+" -- duplicate of "+str(marked_row['dupe_group'])+"\n"
            temp_str2="part_DBID,CAD_link0"
            temp_str3="CAD_link0="+str(marked_row['obj'].CAD_DBID)
            for i in range(1,32):
                temp_str2+= ",CAD_link"+str(i)
                temp_str3+=" OR CAD_link"+str(i)+"="+str(marked_row['obj'].CAD_DBID)
            query="SELECT "+temp_str2+" FROM parts WHERE "+temp_str3
            #logger.debug(query)
            for db_res in cur.execute(query):
                db_links=list(db_res[1:len(db_res)])
                for linki in range(0,len(db_links)):
                    if(db_links[linki] == marked_row['obj'].CAD_DBID):
                        temp_str+="UPDATE parts SET CAD_link"+str(linki)+"="+str(marked_row['dupe_group'])+" WHERE part_DBID="+str(db_res[0])+" -- from CAD_link"+str(linki)+"="+str(db_links[linki])+"\n"
    #Simpler solution: UPDATE parts SET CAD_link0=new_value WHERE CAD_link0=old_value
    #temp_str+="--start of part data duplicates"
    
    logger.info(temp_str)
    return temp_str

def clean_db():
    return False
    #Reindex to fill index gaps
    #Remove broken CAD_links
    #Remove duplicate CAD_links
    #Reorder CAD_links to acending
    #Remove gaps in CAD_links
    #Check that files referenced in CAD_data actually exist
    #Suggest deduplication
    #Optional auto execute changes

def demo_and_test():
    logger.info("Start of tests")
    db_part_search("manufacturer_PN LIKE 'CL32X107MQVNN%'")
    db_part_search("part_DBID=34")
    part_DBID=new_part_DBID()
    CAD_DBID=new_CAD_DBID()
    logger.debug("New indices   "+str(part_DBID)+"  "+str(CAD_DBID))
    myp = part(part_DBID)
    myCd=CAD_datum(CAD_DBID)
    logger.debug("Objects created")
    
    myp.manufacturer="mfg1655"
    myp.manufacturer_PN="000001"
    myCd.full_path="C:\lib"
    
    myp.CAD_data.append(myCd)
    logger.debug("CAD datum linked")
    
    logger.info("Expect missing CAD data")
    part_to_db(myp)
    CAD_datum_to_db(myCd)
    part_to_db(myp)
    
    mynp = part_from_db(part_DBID)
    logger.info("Readback:"+str(mynp))
    
    pretty_print_CAD_data(mynp.CAD_data)
    
    find_part_duplicates()
    find_CAD_duplicates()

import_from_old_db()
