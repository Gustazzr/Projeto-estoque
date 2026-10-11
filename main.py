from produtos import cadastrar_produtos
import os
from dotenv import load_dotenv
load_dotenv()
import flet as ft
import mysql.connector 

def main(page: ft.Page):
    page.title = "Estoque"
    page.window_width = 800
    page.window_height = 600
    
   
    page.bgcolor = "grey900"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    
    Titulo = ft.Text("Cadastro dos produtos", size=30, color="white", weight=ft.FontWeight.BOLD)
    page.add(Titulo)
    
    # Campo Nome
    campo_nome = ft.TextField(
        label="Digite o nome: ", 
        width=400, 
        bgcolor="purple900", 
        color="white", 
        label_style=ft.TextStyle(color="white"), 
        border_color="purple300", 
        border_radius= 30,
        error_style=ft.TextStyle(color="red")
    )
    page.add(campo_nome)

    #Campo Preço
    campo_preco = ft.TextField(
        label="Digite o preço: ", 
        keyboard_type=ft.KeyboardType.NUMBER,
        width=400,
        bgcolor="purple900",
        color="white",
        label_style=ft.TextStyle(color="white"),
        border_color="purple300",
        border_radius= 30,
        error_style=ft.TextStyle(color="red")
    )
    page.add(campo_preco)

    #Campo Quantidade
    campo_quantidade = ft.TextField(
        label="Digite a quantidade: ", 
        keyboard_type=ft.KeyboardType.NUMBER,
        width=400,
        bgcolor="purple900",
        color="white",
        label_style=ft.TextStyle(color="white"),
        border_color="purple300",
        border_radius= 30,
        error_style=ft.TextStyle(color="red")
    )
    page.add(campo_quantidade)

    def salvar_produto(e):

        campo_nome.error_text = None
        campo_preco.error_text = None
        campo_quantidade.error_text = None

        nome = (campo_nome.value or "").strip()
        preco = (campo_preco.value or "").replace(",", ".").strip()
        quantidade = (campo_quantidade.value or "").strip()

        
        # verificação 
        tem_erro = False
        if nome == "":
            campo_nome.label = "ERRO: DIGITE O NOME!"
            campo_nome.label_style = ft.TextStyle(color="red500")
            tem_erro = True
            print("NOME ESTÁ VAZIO")
        else:
            campo_nome.label = "Digite o nome:"
            campo_nome.label_style = ft.TextStyle(color="white")

    
        if preco == "":
            campo_preco.label = "ERRO: DIGITE O PREÇO!"
            campo_preco.label_style = ft.TextStyle(color="red500")
            tem_erro = True
            print("PREÇO ESTÁ VAZIO")
        else:
            campo_preco.label = "Digite o preço:"
            campo_preco.label_style = ft.TextStyle(color="white")

            
        if quantidade == "":
            campo_quantidade.label = "ERRO: DIGITE A QUANTIDADE!"
            campo_quantidade.label_style = ft.TextStyle(color="red500")
            tem_erro = True
            print("QUANTIDADE ESTÁ VAZIA")
        else:
            campo_quantidade.label = "Digite a quantidade:"
            campo_quantidade.label_style = ft.TextStyle(color="white")

            
        if tem_erro:
            page.update()
            return

        
       # Tenta converter para número
        try:
            preco = float(preco)
            quantidade = int(quantidade)
        except ValueError:
            texto_status.value = "ERRO: Preço ou quantidade devem ser números!"
            texto_status.color = "red500"
            page.update()
            return
        

        try:
            conexao = mysql.connector.connect(
            host=os.getenv("DB_HOST"), 
            user=os.getenv("DB_USER"), 
            password=os.getenv("DB_PASS"), 
            database=os.getenv("DB_NAME"))
            cursor = conexao.cursor()
            comando = "INSERT INTO produtos (nome, preco, quantidade) VALUES (%s, %s, %s)"
            valores = (nome, preco, quantidade)
            cursor.execute(comando, valores)
            conexao.commit()

            # Limpa os campos
            campo_nome.value = ""
            campo_preco.value = ""
            campo_quantidade.value = ""
            
            # Retorna as labels para o normal
            campo_nome.label = "Digite o nome:"
            campo_preco.label = "Digite o preço:"
            campo_quantidade.label = "Digite a quantidade:"

            cursor.close()
            conexao.close()
            
            texto_status.value = f"Produto {nome} cadastrado com sucesso!"
            texto_status.color = "green500"
            print(f"Salvo: {nome}, R${preco}, {quantidade}")

        except mysql.connector.Error as err:
            texto_status.value = f"Erro no banco de dados: {err}"
            texto_status.color = "red500"
            print(f"Erro MySQL: {err}")

        page.update()


    botao1 = ft.ElevatedButton(
        "Cadastrar produto", 
        on_click=salvar_produto,
        bgcolor="purple700",
        color="white"
    )
    texto_status = ft.Text("", color="green500", size=16, weight=ft.FontWeight.BOLD)

    page.add(botao1, texto_status)

ft.app(main)