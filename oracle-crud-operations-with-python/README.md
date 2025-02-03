### ORACLE CONNECTION CLASS EXAMPLE OF USE ###

# importing
from oracleConnection import OracleConnection

# initializing database connection
db = OracleConnection('system/oracle@localhost:1521/xe')

# opening database connection
db.open_connection()

# executing single insert
db.execute('insert into contato (id, nome, telefone)  values (:1, :2, :3)', (7, 'Viuva Negra', '55556666'), True, True, True)

# executing many insert example
db.execute('insert into contato (id, nome, telefone)  values (:1, :2, :3)', [(8, 'Capitao America', '55556666'), (9, 'Thor', '55556666')], True, True, True)

# getting data with parameters
rs = db.execute_query('select * from contato where nome=:nome', {'nome': 'Tony Stark'}, True, True)

# getting data without parameters
rs = db.execute_query('select * from contato', {}, True, True)

# deleting data
db.execute('delete from contato where nome=:nome',{'nome': 'Thiago Mendes'}, True, True, True)

# updating data
db.execute('update contato set nome=:novo_nome where nome=:nome_antigo',{'novo_nome': 'Joao da Silva', 'nome_antigo': 'Joao'}, True, True, True)

# closing database connection
db.close_connection()