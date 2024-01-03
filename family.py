# For family system
from connectdb import *
from refugee import *
import sqlite3


def get_family():
    familyList = []
    with setup_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT familyID FROM refugee")
        familyIDs = cursor.fetchall()
        for familyID in familyIDs:
            if str(familyID[0]) not in familyList:
                familyList.append(str(familyID[0]))
    return familyList


# get_Family()
