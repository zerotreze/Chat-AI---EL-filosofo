import sqlite3

#Conectar ao banco de dados ou criar banco de dados
def connect(db_name='db.sqlite3'):
    conn = sqlite3.connect(db_name)
    return conn

# Função para deletar uma linha
def delete_row(id, table_name='auth_user'):
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (id,))
        conn.commit()
        print(f"Linha com id {id} removida com sucesso.")
    except sqlite3.Error as err:
        print(f"Erro: {err}")
    finally:
        cursor.close()
        conn.close()

# Exemplo de uso
delete_row(id=7)
delete_row(id=8)
delete_row(id=9)
delete_row(id=10)
delete_row(id=11)