import sqlite3

conn=sqlite3.connect('teste.db')
conn.execute("PRAGMA foreign_keys = 1")
c=conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS Estoques(
    codEstoque INTEGER PRIMARY KEY,
    nome TEXT
)""")

conn.commit()

class Estoque:
# 1 ATRIBUTO ; 1 METODOS   

    def __init__(self, estoque):

        #estoque = nome do estoque; 
        self.estoque=estoque

        #Automaticamente insere o estoque no banco de dados e cria uma tabela correspondente
        #Não é possível inserir o estoque se o nome já estiver ocupado
        c.execute("SELECT * FROM Estoques WHERE nome=?",(self.estoque,))
        check = c.fetchone()
        if not check:
            with conn:
                c.execute("INSERT INTO Estoques (nome) VALUES (?)", (self.estoque,))
            with conn:
                c.execute("""CREATE TABLE IF NOT EXISTS """+self.estoque+"""(
            numero INTEGER,
            nome TEXT,
            quantidade INTEGER,
            preço REAL,
            estoque INTEGER NOT NULL,
            FOREIGN KEY (estoque) REFERENCES Estoques(codEstoque) ON DELETE CASCADE
            )""")  

    @staticmethod
    def remover_estoque(nome_estoque):

        #Recebe o nome do estoque
        #Remove o estoque do Banco e os produtos contidos nesse estoque
        with conn:
            c.execute("DELETE FROM Estoques WHERE nome=?",(nome_estoque,))
        

    def mostrar_estoque(self):

        #Para testes: printa o estoque
        with conn:
            c.execute("SELECT * FROM "+self.estoque)
        print (c.fetchall())
    
    @staticmethod
    def mostrar_estoques():

        #Para testes: printa os estoques no banco
        c.execute("SELECT * FROM Estoques")
        print (c.fetchall())


class Produto:
# 5 ATRIBUTOS; 3 METODOS

    def __init__(self, numero, nome, quantidade, preço, estoque_nome):

        #O ultimo atributo recebe o nome do estoque ao qual o produto pertence
        self.numero=numero
        self.nome=nome
        self.quantidade=quantidade
        self.preço=preço
        self.estoque_nome=estoque_nome
    
    def produto_novo(self):

        #Insere o produto na tabela correspondente ao seu estoque
        #Caso o Numero OU o Nome já estejam ocupados, o metodo não insere o produto
        c.execute("SELECT * FROM "+self.estoque_nome+" WHERE nome=? OR numero=? ",(self.nome,self.numero))
        check = c.fetchone()
        if not check:
                c.execute("SELECT * FROM Estoques WHERE nome = ?",(self.estoque_nome,))
                lista=c.fetchone()
                c.execute("INSERT INTO "+self.estoque_nome+" VALUES (?, ?, ?, ?, ?)",(self.numero, self.nome,
                self.quantidade, self.preço, lista[0]))
                conn.commit()

    def alterar_produto(self, nro_prod):

        #Atualiza todas as informações do produto com o Numero equivalente a "nro_prod"
        #Metodo criado a fim do objeto utilizado possuir 1 ou mais atributos a serem atualizados
        #Caso o Numero OU o Nome já estejam ocupados, o metodo não atualiza o produto
        c.execute("SELECT * FROM "+self.estoque_nome+" WHERE nome=? OR numero=? ",(self.nome,self.numero))
        check = c.fetchone()
        if not check:
            c.execute("UPDATE "+self.estoque_nome+" SET numero=?, nome=?, quantidade=?, preço=?  WHERE numero=?",
            (self.numero, self.nome, self.quantidade, self.preço, nro_prod))
            conn.commit()
      
    def remover_produto(self):

        #Remove o produto de sua tabela/estoque correspondente
        with conn:
            c.execute("DELETE FROM "+self.estoque_nome+" WHERE numero=?",(self.numero,))

stq = Estoque('nome_estoque1')
stq2 = Estoque('nome_estoque2')
stq3 = Estoque('nome_estoque3')
Estoque.mostrar_estoques()
prod1 = Produto(1, "produtao", 3, 4.30, stq.estoque)
prod1.produto_novo()
stq.mostrar_estoque()
prod1 =Produto(3,"produtasso", 5, 6.30,stq.estoque)
prod1.alterar_produto(1)
stq.mostrar_estoque()
prod2 = Produto(2,"produtin", 2, 1.99, stq.estoque)
prod2.produto_novo()
stq.mostrar_estoque()
prod2.remover_produto()
stq.mostrar_estoque()
Estoque.remover_estoque(stq.estoque)
stq.mostrar_estoque()
Estoque.mostrar_estoques()
