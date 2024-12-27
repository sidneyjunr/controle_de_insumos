from tkinter import *
import pyodbc
from datetime import datetime
from tkinter import messagebox, ttk
from decimal import Decimal
dados_conexao = (
    "Driver={MySQL ODBC 9.1 ANSI Driver};"  # Ou "MySQL ODBC 8.0 Unicode Driver" dependendo da sua versão
    "Server=localhost;"  # IP ou nome do servidor MySQL
    "Database=estoquementoria;"  # Nome do banco de dados
    "User=root;"  # Seu usuário MySQL
    "Password=mysql;"  # Sua senha
)
conexao = pyodbc.connect(dados_conexao)
cursor = conexao.cursor()


#Procurar Insumo
def btn_clicked0():
    nome_insumo = entry1.get()
         
    comando = f"""SELECT * from insumos
        WHERE nome_insumo = '{nome_insumo}';
        """
    cursor.execute(comando)
    entry0.delete("1.0", END) 
    for row in cursor.fetchall():
        texto = f"Item: {row.nome_insumo}\n Quantidade: {row.qtde}\n Lote:{row.lote}\n Validade:{row.data_validade}\n"
        entry0.insert("1.0", texto) 
    

#Deletar Insumo    
def btn_clicked1():
    nome_insumo = entry1.get()
    comando = f"""DELETE from insumos
            WHERE nome_insumo = '{nome_insumo}';
            """
    cursor.execute(comando)
    cursor.commit()
    print("Deletar Insumo")
    messagebox.showinfo(title='Aviso Uso Excluído', message=f"{nome_insumo} foi excluído do Banco de Dados")
    
    
#Registrar Uso Insumo    
def btn_clicked2():
    nome_insumo = entry1.get()
    qtde_usada =entry4.get()
    comando = f"""UPDATE insumos
        SET qtde = qtde - {qtde_usada}
        WHERE nome_insumo = '{nome_insumo}';
        """
    cursor.execute(comando)
    cursor.commit()
    messagebox.showinfo(title='Aviso Uso Insumo', message=f"{qtde_usada} Unidades do {nome_insumo} foram usadas")
    
    print("Usar Insumo")
    
#Adicionar Insumo    
def btn_clicked3():
    nome_insumo = entry1.get()
    data_validade = entry2.get()
    try:
        data_formatada = datetime.strptime(data_validade, '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Erro", "Data inválida. Use o formato DD/MM/AAAA.")
        return
    
    # data_formatada = datetime.strptime(data_validade, '%d/%m/%Y').strftime('%Y-%m-%d')
    lote = entry3.get()
    qtde =entry4.get()
    procurar = f"""SELECT * from insumos
        WHERE nome_insumo = '{nome_insumo}';
        """
    cursor.execute(procurar)
    resultados = cursor.fetchall()
    if resultados:
        # nome_resultados = resultados[0][1]
        qtde_resultados = resultados[0][4]
        if isinstance(qtde_resultados, Decimal):
            qtde_resultados = Decimal(qtde_resultados)  # Garante que seja Decima
        atualizar_qtd = f"""UPDATE insumos
        SET qtde = qtde + {qtde}
        WHERE nome_insumo = '{nome_insumo}';
        """
        cursor.execute(atualizar_qtd)
        cursor.commit()
        qtde = int(qtde)
        messagebox.showinfo(title='Aviso de Atualização', message=f"{nome_insumo.capitalize()} já existe \nNova Quantidade: {qtde_resultados+qtde}")
    else:
        comando = f"""INSERT INTO insumos(nome_insumo, data_validade, lote, qtde)
        VALUES
            ('{nome_insumo}', '{data_formatada}', '{lote}', '{qtde}')"""
        cursor.execute(comando)
        cursor.commit()
        messagebox.showinfo(title='Aviso Adicionar Produto', message="Produto Adicionado Com Sucesso")
    
    # entry1.delete()
    # entry2.delete()
    # entry3.delete()
    # entry4.delete()
    
    
# print(entry0.get("1.0", END)) -> campo para exibir o produto do banco de dados
# print(entry1.get()) -> nome insumo
# print(entry2.get()) -> data validade
# print(entry3.get()) -> lote 
# print(entry4.get()) -> quantidade


window = Tk()

window.geometry("711x646")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 646,
    width = 711,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = "janela/background.png")
background = canvas.create_image(
    355.5, 323.0,
    image=background_img)

img0 = PhotoImage(file = f"janela/img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked0,
    relief = "flat")

b0.place(
    x = 479, y = 195,
    width = 178,
    height = 38)

img1 = PhotoImage(file = f"janela/img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked1,
    relief = "flat")

b1.place(
    x = 247, y = 197,
    width = 178,
    height = 36)

img2 = PhotoImage(file = f"janela/img2.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked2,
    relief = "flat")

b2.place(
    x = 479, y = 123,
    width = 178,
    height = 35)

img3 = PhotoImage(file = f"janela/img3.png")
b3 = Button(
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked3,
    relief = "flat")

b3.place(
    x = 247, y = 125,
    width = 178,
    height = 34)

entry0_img = PhotoImage(file = f"janela/img_textBox0.png")
entry0_bg = canvas.create_image(
    455.0, 560.0,
    image = entry0_img)

entry0 = Text(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry0.place(
    x = 250, y = 502,
    width = 410,
    height = 114)

entry1_img = PhotoImage(file = f"janela/img_textBox1.png")
entry1_bg = canvas.create_image(
    517.0, 294.5,
    image = entry1_img)

entry1 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry1.place(
    x = 377, y = 278,
    width = 280,
    height = 31)

entry2_img = PhotoImage(file = f"janela/img_textBox2.png")
entry2_bg = canvas.create_image(
    517.0, 340.5,
    image = entry2_img)

entry2 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry2.place(
    x = 377, y = 324,
    width = 280,
    height = 31)

entry3_img = PhotoImage(file = f"janela/img_textBox3.png")
entry3_bg = canvas.create_image(
    517.0, 388.5,
    image = entry3_img)

entry3 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry3.place(
    x = 377, y = 372,
    width = 280,
    height = 31)

entry4_img = PhotoImage(file = f"janela/img_textBox4.png")
entry4_bg = canvas.create_image(
    517.0, 436.5,
    image = entry4_img)

entry4 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry4.place(
    x = 377, y = 420,
    width = 280,
    height = 31)

window.resizable(False, False)
window.mainloop()
