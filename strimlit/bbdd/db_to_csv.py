import pandas as pd
import sqlite3 as db

con = db.connect('shark_attacks.db')
df = pd.read_sql_query('select * from shark_attackdatos;', con)

df.to_csv('SharkAttacks.csv', index=False)
