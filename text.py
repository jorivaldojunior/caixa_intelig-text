import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os

class SistemaMercadinho:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Mercadinho 📦")
        self.root.attributes('-fullscreen', True)  # Abrir em tela cheia

        self.produtos = []
        self.total_compra = 0

        style = ttk.Style()
        style.configure("Green.TButton", foreground="green", font=("Arial", 15, "bold"))
        style.configure("Yellow.TButton", foreground="yellow", font=("Arial", 15, "bold"))
        style.configure("Blue.TButton", foreground="blue", font=("Arial", 15, "bold"))
        style.configure("Red.TButton", foreground="red", font=("Arial", 15, "bold"))
        style.configure("Orange.TButton", foreground="orange", font=("Arial", 15, "bold"))
        style.configure("Brown.TButton", foreground="brown", font=("Arial", 15, "bold"))

        # Título do Mercadinho
        self.titulo_label = ttk.Label(self.root, text="Controle Todas As Despesas Da Sua Loja, Com Um Sistema De Caixa Inteligente 📦", font=("Arial", 20, "bold"))
        self.titulo_label.pack(pady=10)

        self.criar_interface()

    def adicionar_produto(self):
        nome = self.nome_entry.get().title()
        quantidade = self.quantidade_entry.get()
        preco = self.preco_entry.get()

        # Verificar se todos os campos estão preenchidos
        if nome and quantidade and preco:
            quantidade = int(quantidade)
            preco = float(preco.replace(',', '.'))

            # Verificar se há produtos na lista
            if self.produtos:
                # Obter o último ID dos produtos
                ultimo_id = int(self.produtos[-1][0])
                novo_id = f"{ultimo_id + 1:02d}"  # Formatando o novo ID com zero na frente
            else:
                novo_id = "01"

            # Verificar se o novo ID já existe
            while any(produto[0] == novo_id for produto in self.produtos):
                ultimo_id += 1
                novo_id = f"{ultimo_id:02d}"  # Formatando o novo ID com zero na frente

            preco_total = quantidade * preco
            self.produtos.append((novo_id, nome, quantidade, preco, preco_total))
            self.atualizar_lista_produtos()
            self.calcular_total_compra()
            self.limpar_campos()

        else:
            messagebox.showerror("Erro", "Preencha todos os campos.")

    def excluir_produto(self):
        if self.produtos_tree.selection():
            item_selecionado = self.produtos_tree.selection()[0]
            indice = self.produtos_tree.index(item_selecionado)
            del self.produtos[indice]
            self.atualizar_lista_produtos()
            self.calcular_total_compra()
            self.limpar_campos()
        else:
            messagebox.showinfo("Aviso", "Selecione um produto para excluir.")

    def atualizar_produto(self):
        if self.produtos_tree.selection():
            item_selecionado = self.produtos_tree.selection()[0]
            indice = self.produtos_tree.index(item_selecionado)
            nome = self.nome_entry.get().title()
            quantidade = int(self.quantidade_entry.get())
            preco = float(self.preco_entry.get().replace(',', '.'))
            preco_total = quantidade * preco
            self.produtos[indice] = (self.produtos[indice][0], nome, quantidade, preco, preco_total)
            self.atualizar_lista_produtos()
            self.calcular_total_compra()
            self.limpar_campos()
        else:
            messagebox.showinfo("Aviso", "Selecione um produto para atualizar.")

    def calcular_total_compra(self):
        self.total_compra = sum(produto[4] for produto in self.produtos)
        self.total_label.config(text=f"Total da Compra: {self.formatar_valor(self.total_compra)}")

    def formatar_valor(self, valor):
        if valor < 1000:
            return f"R${valor:,.2f}".replace('.', ',')
        else:
            valor_str = f"{valor:,.2f}"
            parte_inteira, parte_decimal = valor_str.split('.')
            parte_inteira = parte_inteira.replace(',', '.')
            return f"R${parte_inteira},{parte_decimal}"

    def atualizar_lista_produtos(self):
        self.produtos_tree.delete(*self.produtos_tree.get_children())
        for produto in self.produtos:
            self.produtos_tree.insert('', 'end', values=produto)

    def limpar_campos(self):
        self.nome_entry.delete(0, tk.END)
        self.quantidade_entry.delete(0, tk.END)
        self.preco_entry.delete(0, tk.END)
        self.dinheiro_entry.delete(0, tk.END)

    def on_select(self, event):
        item_selecionado = self.produtos_tree.focus()
        if item_selecionado:
            item = self.produtos_tree.item(item_selecionado)
            values = item.get('values')
            if values:
                self.nome_entry.delete(0, tk.END)
                self.quantidade_entry.delete(0, tk.END)
                self.preco_entry.delete(0, tk.END)
                self.dinheiro_entry.delete(0, tk.END)
                self.nome_entry.insert(0, values[1])
                self.quantidade_entry.insert(0, values[2])
                self.preco_entry.insert(0, values[3])

    def gerar_nota_fiscal(self):
        if not self.produtos:
            messagebox.showinfo("Aviso", "Você precisa inserir produtos.")
            return None

        data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        dinheiro_recebido = self.dinheiro_entry.get()
        if not dinheiro_recebido:
            messagebox.showwarning("Aviso", "Não foi encontrada nenhuma compra.")
            return None

        dinheiro_recebido = float(dinheiro_recebido)
        troco = dinheiro_recebido - self.total_compra

        nota = f"Extrato Detalhado Do Seu Cupom Fiscal:\n"
        nota += f"{'-'*94}\nRazão Social: JDaS.Azevedo Junior\nCNPJ: 546780001/01\n"
        nota += f"{'-'*94}\n"
        nota += f"N° Cupom Fiscal: 0000AEEB123\n"
        nota += f"{'-'*94}\n"
        
        nota += f"Data e Hora da Compra: {data_hora_atual}\n"
        nota += f"{'-'*94}\n"
        nota += f"Dinheiro Recebido: {self.formatar_valor(dinheiro_recebido)}\n"
        nota += f"Troco: {self.formatar_valor(troco)}\n\n"
        nota += f"ID Nome do Produto Quantidade Preço Unid. Preço Total\n"

        for produto in self.produtos:
            id_produto = produto[0]
            nome_produto = produto[1]
            quantidade = produto[2]
            preco_unitario = self.formatar_valor(produto[3])
            preco_total = self.formatar_valor(produto[4])
            nota += f"{id_produto}\t{nome_produto}\t{quantidade}x\t{preco_unitario}\t{preco_total}\n"

        nota += f"{'-'*94}\n"
        nota += f"Valor Total da Compra: {self.formatar_valor(self.total_compra)}"

        return nota

    def criar_pagina_nota_fiscal(self):
        nota_fiscal = self.gerar_nota_fiscal()
        if nota_fiscal:
            temp_file = "temp_cupom_fiscal.txt"
            with open(temp_file, 'w') as file:
                file.write(nota_fiscal)

            os.system(f'notepad.exe {temp_file}')
            os.remove(temp_file)
            self.limpar_campos()  # Limpar campos após fechar o bloco de notas
            self.produtos.clear()
            self.atualizar_lista_produtos()
            self.calcular_total_compra()
        else:
            messagebox.showwarning("Aviso", "Não foi possível gerar o cupom fiscal.")

    def criar_interface(self):
        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.pack(fill="both", expand=True)

        self.nome_label = ttk.Label(self.frame, text="Nome do Produto:", font=("Arial", 14, "bold"))
        self.nome_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.nome_entry = ttk.Entry(self.frame)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        self.quantidade_label = ttk.Label(self.frame, text="Quantidade:", font=("Arial", 14, "bold"))
        self.quantidade_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.quantidade_entry = ttk.Entry(self.frame)
        self.quantidade_entry.grid(row=1, column=1, padx=5, pady=5)

        self.preco_label = ttk.Label(self.frame, text="Preço Unidade:", font=("Arial", 14, "bold"))
        self.preco_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.preco_entry = ttk.Entry(self.frame)
        self.preco_entry.grid(row=2, column=1, padx=5, pady=5)

        self.adicionar_btn = ttk.Button(self.frame, text="Adicionar Produto", command=self.adicionar_produto, style="Green.TButton")
        self.adicionar_btn.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        
        self.excluir_btn = ttk.Button(self.frame, text="Excluir Produto", command=self.excluir_produto, style="Yellow.TButton")
        self.excluir_btn.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.atualizar_btn = ttk.Button(self.frame, text="Atualizar Produto", command=self.atualizar_produto, style="Blue.TButton")
        self.atualizar_btn.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.produtos_tree = ttk.Treeview(self.frame, columns=("ID","Nome","Quantidade","Preco Unid.","Preco Total")) # Corrigido para "Preco"
        self.produtos_tree.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.produtos_tree.column('#0', width=0, stretch=tk.NO)
        self.produtos_tree.column('ID', width=60, anchor='center')  # Adicionado largura e âncora para o ID
        self.produtos_tree.column('Nome', width=200)  # Ajustado para maior espaço
        self.produtos_tree.column('Quantidade', width=100)
        self.produtos_tree.column('Preco Unid.', width=120)  # Corrigido para 'Preco'
        self.produtos_tree.column('Preco Total', width=120)  # Adicionado coluna para o preço total
        self.produtos_tree.heading('ID', text='ID')
        self.produtos_tree.heading('Nome', text='Nome')
        self.produtos_tree.heading('Quantidade', text='Quantidade')
        self.produtos_tree.heading('Preco Unid.', text='Preço Unid.')
        self.produtos_tree.heading('Preco Total', text='Preço Total')  # Adicionado cabeçalho para o preço total
        
        self.produtos_tree.bind("<<TreeviewSelect>>", self.on_select)

        self.total_label = ttk.Label(self.frame, text="Total da Compra: R$ 0,00", font=("Arial", 14, "bold"))
        self.total_label.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        self.dinheiro_label = ttk.Label(self.frame, text="Dinheiro Recebido:", font=("Arial", 14, "bold"))
        self.dinheiro_label.grid(row=8, column=0, padx=5, pady=5, sticky="w")
        self.dinheiro_entry = ttk.Entry(self.frame)
        self.dinheiro_entry.grid(row=8, column=1, padx=5, pady=5)

        ttk.Button(self.frame, text="Visualizar Cupom Fiscal", command=self.criar_pagina_nota_fiscal, style="Brown.TButton").grid(row=10, column=0, columnspan=2, padx=5, pady=5)
        
        ttk.Button(self.frame, text="Informações, Como usar", command=self.mostrar_instrucoes, style="Orange.TButton").grid(row=11, column=0, columnspan=2, padx=5, pady=5)
        ttk.Button(self.frame, text="Sair ou Minimizar a Sua Tela", command=self.sair, style="Red.TButton").grid(row=12, column=0, columnspan=2, padx=5, pady=5)

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

    def sair(self):
        escolha = messagebox.askquestion("Sair Ou Minimizar", "Sair Aperte Sim!\nMinimizar Aperte Não!")
        if escolha == 'yes':
            self.root.destroy()
        else:
            self.root.iconify()

    def mostrar_instrucoes(self):
        instrucoes = """Aprenda a Usar o Aplicativo Passo a Passo:

Passo 1 - Insira o nome do produto;
Passo 2 - Insira a quantidade do produto.
Passo 3 - Insira o preço da unidade.
Passo 4 - Aperte o botão "Adicionar Produto".

Passo 5 - Se precisar atualizar o produto, selecione-o.
O produto aparecerá na caixa de texto e, depois de modificá-lo, 
aperte "Atualizar Produto".

Passo 6 - Para excluir da lista, 
basta selecioná-lo e apertar "Excluir Produto".

Passo 7 - Feito isso, você deve inserir o valor em dinheiro
e apertar "Visualizar Cupom Fiscal". 
De imediato, será aberto um bloco de notas
com seu cupom fiscal atualizado, onde você poderá imprimir,
salvar, gerar PDF e compartilhar seu cupom fiscal.

Passo 8 - OBS: Para limpar os campos e iniciar outras compras
basta apenas fechar o cupom fiscal que esteja aberto e todos
campos ficaram limpos e podera inserir novos produtos.

Contato: (55+)81991152307
Email: jorivaldoazevedo@hotmail.com

Obrigado e aproveite o app Atenciosamente, Jorivaldo Junior!"""

        temp_file = "instrucoes.txt"
        with open(temp_file, 'w') as file:
            file.write(instrucoes)

        os.system(f'notepad.exe {temp_file}')
        os.remove(temp_file)


if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaMercadinho(root)
    root.mainloop()
