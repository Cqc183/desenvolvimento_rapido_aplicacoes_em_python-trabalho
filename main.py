from tkinter import Tk
from frontend import MainWindow
import backend

#Verifica se o código está sendo excutado diretamente
if __name__ == "__main__":
    # Conecta ao banco de dados chamando a função connect do módulo backend
    backend.connect()
    # Cria uma instância da classe Tk para representar a janela principal do progrma
    root = Tk()
    # Cria uma instância da classe MainWindow, passando a janela principal como argumento
    app = MainWindow(root)
    # Começa loop principal da interface gráfica, aguardando eventos do usuário
    root.mainloop()
