from flask import Flask, render_template, url_for, flash, redirect, request
import sqlite3



conn=sqlite3.connect('teste.db',check_same_thread=False)
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

    def criar_tabela(self):

        #Insere o estoque no banco de dados e cria uma tabela correspondente
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
        return c.fetchall()
    
    @staticmethod
    def mostrar_estoques():

        #Para testes: printa os estoques no banco
        c.execute("SELECT * FROM Estoques")
        return c.fetchall()

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


app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def teste():

    if request.method == "POST":
        if "add" in request.form:
            stock=Estoque(request.form.get('novo_estoque'))
            Estoque.criar_tabela(stock)
    repeat = Estoque.mostrar_estoques()
    print ("REPEAT = "+str(repeat))
    tam=len(repeat)
    print ("tam = "+str(tam))
    for i in range(tam):
        repeat[i]
        print ("repeat[i] = "+str(repeat[i]))
        if request.method == "POST":
            print ("É O METODO POST")
            print ("REQUEST.FORM ="+str(request.form))
            if  str(repeat[i]) in request.form:
                print (str(repeat[i])+"ESTA DENTRO DE REQUEST.FORM")
                estoque = repeat[i]
                print ("ESTOQUE = "+str(estoque))
                nom_estoque = estoque[1]
                print ("nom_estoque = "+nom_estoque)
                Estoque.remover_estoque(str(nom_estoque))
    
    
    repeat = Estoque.mostrar_estoques()
    return render_template('repasse3.html',len=len(repeat),repeat=repeat)

@app.route("/estoque", methods=['GET','POST'])
def home():
    return "home"

     
    # if request.method == "POST":
         #product=Produto(request.form.get('num'),request.form.get('nome'),request.form.get('quantidade'),
         #request.form.get('preço'),request.form.get('num'),stock.estoque)
         #nome=request.form.get('nome')
         #num=(request.form.get('num')
        # product.produto_novo(nome,num)


#    estoque = Estoque('estoque_teste')
#    prod1=Produto(1,'produtao', 3, 4.50,estoque.estoque)
#    prod1.produto_novo()
#    prod2=Produto(2,'produtasso', 5, 7.50,estoque.estoque)
#    prod2.produto_novo()
#    x = str(estoque.mostrar_estoque()).translate({ord(c):'' for c in "[]()'"})
    #return x 
 #   return render_template('Budstock-estoque.html')
    



         #self.estoque = request.form['novo estoque']
 #verifica se o estoque já existe, se existir aparece uma mensagem dizendo que o mesmo já existe
    #if  request.form['novo_estoque'] in Estoques:

 #    flash ('O estoque {} já existe.'.format( request.form['novo estoque'])
  #  else:
   #     #irá criar um novo etoque que o usuário pediu
     #   self.estoque,criar_estoque()
    #
    # remove o estoque
    #excluir = request.form['excluir estoque']
    #if  request.form.get['excluir estoque'] in Estoques:
    #   remover_estoque(excluir)

   #reenvia o usuário para a página com o novo estoque feito, ou com estoques deletados
    #return redirect(url_for('home'))



#@app.route("/estoque")
#def alterar():
 #   self.numero= request.form['número']
 #   self.nome=request.form['nome']
  #  self.quantidade=request.form['quantidade']
   # self.preço= request.form['preço']
  #  self.estoque_nome= request.form['nome do estoque']
    #return render_template('estoque.html',title='Produtos')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)