# Importações das bibliotecas necessárias
from tkinter import END, Label, StringVar, Entry, Listbox, Scrollbar, Button
from tkinter.ttk import OptionMenu
from tkinter import messagebox
import backend
import os

# Obtém o diretório atual do código
current_dir = os.path.dirname(os.path.abspath(__file__))
CAMINHO_ICONE = os.path.join(current_dir, 'icone.ico')


# Classe para a janela principal da aplicação
class MainWindow:
    # Inicialização da instância da janela
    def __init__(self, root):
        self.root = root
        self.root.title("SISTEMA DE CADASTRO LOJA DE GAMES")
        # Inicialize a plataforma com uma opção vazia
        self.plataforma = StringVar()
        self.plataforma.set("")  # Define a plataforma como vazia
        try:
            self.root.iconbitmap(CAMINHO_ICONE)
        except FileNotFoundError:
            pass  # Lidar com o erro se o ícone não for encontrado

        # Configuração da janela
        width = 680
        height = 560
        sc_width = self.root.winfo_screenwidth()
        sc_height = self.root.winfo_screenheight()
        x = (sc_width / 2) - (width / 2)
        y = (sc_height / 2) - (height / 2)
        self.root.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.root.resizable(0, 0)
        self.root.config(bg='#47465e')
        # Rótulo do título
        title_label = Label(root, text="Sistema de Cadastro de Jogos da Loja", font=("Helvetica", 20),
                            bg='#47465e', fg='black')
        title_label.grid(row=0, columnspan=6, padx=10, pady=40)

        # Rótulos para os campos
        l1 = Label(root, text="Título", bg='#47465e', fg='black', font=("Helvetica", 12))
        l1.grid(row=1, column=0)
        l2 = Label(root, text="Plataforma", bg='#47465e', fg='black', font=("Helvetica", 12))
        l2.grid(row=2, column=0)
        l3 = Label(root, text="Estoque", bg='#47465e', fg='black', font=("Helvetica", 12))
        l3.grid(row=3, column=0)
        l4 = Label(root, text="Preço", bg='#47465e', fg='black', font=("Helvetica", 12))
        l4.grid(row=4, column=0)
        l5 = Label(root, text="Código", bg='#47465e', fg='black', font=("Helvetica", 12))
        l5.grid(row=5, column=0, pady=(0, 30))

        # Entradas dos campos
        entry_width = 25
        self.titulo = StringVar()
        self.e1 = Entry(root, textvariable=self.titulo)
        self.e1.grid(row=1, column=1)
        self.e1.config(width=entry_width)
        self.e2 = StringVar()
        plataformas = ["-Escolha uma Opção-", "Playstation", "Xbox", "Nintendo"]
        self.e2 = OptionMenu(root, self.plataforma, *plataformas)
        self.e2.config(width=20)
        self.e2.grid(row=2, column=1)
        self.estoque = StringVar()
        self.e3 = Entry(root, textvariable=self.estoque)
        self.e3.grid(row=3, column=1)
        self.e3.config(width=entry_width)
        self.valor = StringVar()
        self.e4 = Entry(root, textvariable=self.valor)
        self.e4.grid(row=4, column=1)
        self.e4.config(width=entry_width)
        self.codigo = StringVar()
        self.e5 = Entry(root, textvariable=self.codigo)
        self.e5.grid(row=5, column=1, pady=(0, 30))
        self.e5.config(width=entry_width)

        # Lista para exibição dos registros
        self.list1 = Listbox(root, height=8, width=95)
        self.list1.grid(row=12, column=0, rowspan=12, columnspan=2)

        # Scrollbar da lista acima
        sb1 = Scrollbar(root, command=self.list1.yview)
        sb1.grid(row=12, column=2, rowspan=12, sticky='ns')

        self.list1.configure(yscrollcommand=sb1.set)
        sb1.configure(command=self.list1.yview)

        # Associação de eventos de seleção da lista a uma função
        self.list1.bind('<<ListboxSelect>>', self.get_selected_row)

        # Botões das operaões dos bancos de dados
        b1 = Button(root, text="Visualizar", width=22,
                    bg="grey", command=self.view_command)
        b1.grid(row=6, column=0)

        b3 = Button(root, text="Adicionar", width=22,
                    bg="green", command=self.add_command)
        b3.grid(row=7, column=0, pady=(5, 30))

        b4 = Button(root, text="Atualizar", width=22,
                    bg="grey", command=self.update_command)
        b4.grid(row=6, column=1)

        b5 = Button(root, text="Excluir",
                    bg="red", width=22, command=self.delete_command)
        b5.grid(row=7, column=1, pady=(5, 30))

        b6 = Button(root, text="Sair", width=22,
                    bg="firebrick4", command=self.root.destroy)
        b6.grid(row=30, column=0, padx=(250, 0), pady=20)

    # Função para obter uma linha selecionada da lista
    def get_selected_row(self, _):
        if self.list1.curselection():
            index = self.list1.curselection()[0]
            selected_tuple = self.list1.get(index)
            self.e1.delete(0, END)
            self.e1.insert(END, selected_tuple[1])
            self.plataforma.set(selected_tuple[2])  # Atualizar a opção selecionada no OptionMenu
            self.e3.delete(0, END)
            self.e3.insert(END, selected_tuple[3])
            self.e4.delete(0, END)
            self.e4.insert(END, selected_tuple[4])
            self.e5.delete(0, END)
            self.e5.insert(END, selected_tuple[5])
        else:
            print("Nenhum item selecionado para visualização.")

    # Função para visualizar todos os registros no banco de dados
    def view_command(self):
        rows = backend.load_file()
        self.list1.delete(0, END)
        for row in backend.view():
            formatted_row = list(row)
            formatted_row[3] = formatted_row[3]

            # Verifica se o valor começa com 'R$' e se é possível convertêr para float
            if isinstance(formatted_row[4], str) and formatted_row[4].startswith('R$'):
                formatted_row[4] = f'R${float(formatted_row[4][2:]):.2f}'

            formatted_row[5] = formatted_row[5]
            self.list1.insert(END, formatted_row)

    # Função para adicionar um novo registro ao banco de dados
    def add_command(self):
        titulo = self.titulo.get()
        plataforma = self.plataforma.get()
        estoque = self.estoque.get()
        valor = self.valor.get()
        codigo = self.codigo.get()

        # Verificar se o código já existe no banco de dados
        if not backend.code_exists(codigo):
            # Se código não existe, pode adicionar
            if titulo and plataforma != "-Escolha uma Opção-" and estoque and valor and codigo:
                backend.insert(titulo, plataforma, estoque, valor, codigo)
                self.view_command()  # Atualiza a lista após a inserção
                self.clear_input_fields()
        else:
            # Código já existe, exibir mensagem ou realizar ação apropriada
            messagebox.showwarning("AVISO!", "Código já existe. Não é possível adicionar um item com o mesmo código")
        backend.save_file()

    # Função para limpa os campos de entrada
    def clear_input_fields(self):
        self.titulo.set("")  # Limpa o campo de entrada do título
        self.plataforma.set("-Escolha uma Opção-")  # Redefine o OptionMenu para a primeira opção
        self.estoque.set("")  # Limpa o campo de entrada de estoque
        self.valor.set("")  # Limpa o campo de entrada de valor
        self.codigo.set("")  # Limpa o campo de entrada de código

    # Função para excluir um registro do banco de dado
    def delete_command(self):
        if self.list1.curselection():
            selected_tuple = self.list1.get(self.list1.curselection())
            backend.delete(selected_tuple[0])
            self.clear_input_fields()  # Limpa os campos de entrada após a exclusão
            self.view_command()
        else:
            messagebox.showwarning("AVISO!", "Selecione um item para excluir!")
        backend.save_file()

    # Função para atualizar um registro no banco de dados
    def update_command(self):
        # Verificar se há um item selecionado
        if self.list1.curselection():
            # Obter o índice de seleção atual
            index = self.list1.curselection()[0]
            selected_tuple = self.list1.get(index)
            backend.update(selected_tuple[0], self.titulo.get(), self.plataforma.get(), self.estoque.get(),
                           self.valor.get(), self.codigo.get())
            self.clear_input_fields()  # Limpar os campos de entrada após a atualização
            self.view_command()
        else:
            # Se nenhum item estiver selecionado, exibir uma mensagem ou tome outra ação adequada
            messagebox.showwarning("AVISO!", "Nenhum item selecionado para atualização.")
        backend.save_file()
