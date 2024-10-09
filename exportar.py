import sqlite3
from openpyxl import Workbook

# Conecte ao banco de dados SQLite
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Execute o SELECT na tabela
cursor.execute("SELECT * FROM chat_manual")

# Pegue os nomes das colunas
column_names = [description[0] for description in cursor.description]

# Crie uma nova pasta de trabalho do Excel
wb = Workbook()
ws = wb.active
ws.title = "Chat Manual"

# Escreva os nomes das colunas na primeira linha do Excel
ws.append(column_names)

# Escreva todas as linhas da tabela no Excel
for row in cursor.fetchall():
    ws.append(row)

# Salve o arquivo Excel
wb.save("chat_manual_export.xlsx")

# Feche a conexão com o banco de dados
conn.close()

print("Exportação para Excel concluída!")
