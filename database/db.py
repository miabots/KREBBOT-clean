import psycopg2
import os
from dotenv import load_dotenv
from discord.ext import commands
from cns import *


class Db(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        #self.name = 'dbcog'

    # Load Secrets via Environment Variables in .env
    path = './'
    load_dotenv()

    global DB_PASSWORD
    DB_PASSWORD = os.getenv('DB_PASSWORD')

    global con

    global hotsql
    hotsql = ""

    global testsql
    testsql = "INSERT INTO TESTO (SOMETHING) VALUES ('NEWVALUEFROMDISCORD')"

    def initdb(self):
        global con
        global DB_PASSWORD
        con = psycopg2.connect(database="KREBBOTDB", user="postgres",
                               password=DB_PASSWORD, host="127.0.0.1", port="5432")
        print("Database opened successfully")

    def insertdb():
        cur = con.cursor()
        global testsql
        cur.execute(testsql)

        con.commit()
        print("Record Inserted.")

    def insertdb2(sql):
        global con
        cur = con.cursor()
        global testsql
        cur.execute(sql)

        con.commit()
        print("Record Inserted.")

    def selectdb(table):
        global con
        cur = con.cursor()
        table = table
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
        return rows
        # for row in rows:

    # def parseinsertsql(tablename, columns, values):
    # |parsetest TESTO SOMETHING 'NEWVALUEFROMDISCORD'

    def updatesql(tablename, columns, values):
        global testsql
        print('Current SQL:')
        print(testsql)
        table = tablename
        columnlist = columns
        valuelist = values
        newsql = f"INSERT INTO {table} ({columnlist}) VALUES ({valuelist})"
        testsql = newsql
        print('SQL UPDATED SUCCESSFULLY TO:')
        print(testsql)

    def parseinsertsql(incoming):
        print('Beep Boop You are inside Parse')
        raw = incoming
        raws = str(raw)
        rawsa = raws.split('|')
        tablename = rawsa[0]
        columns = rawsa[1]
        values = rawsa[2]
        print('You have sent me:')
        print(raws)
        print('Tablename:')
        print(tablename)
        print('Columns:')
        print(columns)
        print('Values:')
        print(values)
        Db.updatesql(tablename, columns, values)

    def dangerset(sql):
        global hotsql
        hotsql = sql
        print('SQL UPDATED SUCCESSFULLY TO:')
        print(hotsql)

    def dangerexecute():
        global hotsql
        sql = hotsql
        print('NOW EXECUTING:')
        print(sql)
        global con
        cur = con.cursor()
        cur.execute(sql)
        print(cur.statusmessage)
        if "SELECT" in str(cur.statusmessage):
            rows = cur.fetchall()
            return rows
        else:
            return "Nothing to Return"

    def registerdb():
        pass


async def setup(bot):
    await bot.add_cog(Db(bot))
