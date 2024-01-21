import requests
from bs4 import BeautifulSoup
import customtkinter
import os
import smtplib
from email.message import EmailMessage
from time import sleep
import webbrowser

#configurar email e senha
EMAIL_ADDRESS = 'your_email_adress_here'
EMAIL_PASSWORD = 'your_pass_word_here'

#criar um email
def mandar_email(mensagem, destinatario):
    msg = EmailMessage()
    msg['Subject'] = "Informacoes acao solicitada"
    msg['From'] = "your_email_adress_here"
    msg['To'] = destinatario
    msg.set_content(mensagem)
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
urlindice = 'https://www.google.com/search?q=ibovespa&oq=ibo&gs_lcrp=EgZjaHJvbWUqDwgAECMYJxidAhiABBiKBTIPCAAQIxgnGJ0CGIAEGIoFMhIIARBFGDkYgwEYsQMYgAQYigUyEggCEAAYQxiDARixAxiABBiKBTINCAMQABiDARixAxiABDIMCAQQABhDGIAEGIoFMgwIBRAAGEMYgAQYigUyDQgGEAAYgwEYsQMYgAQyDQgHEAAYgwEYsQMYgAQyDQgIEAAYgwEYsQMYgAQyDQgJEAAYgwEYsQMYgATSAQc5ODdqMWo3qAIAsAIA&sourceid=chrome&ie=UTF-8'
siteindice = requests.get(urlindice,headers=headers)
soup2 = BeautifulSoup(siteindice.content,'html.parser')
cotacao_da_bolsa = soup2.find('span',class_='IsqQVc NprOob wT3VGc').get_text()
janela = customtkinter.CTk()
janela.geometry("500x300")
janela.title("O acionista programador")
titulo = customtkinter.CTkLabel(janela,text="O acionista programador",font=("Arial",20))
titulo.pack(padx=10,pady=10)
variacao_diaria = soup2.find('span',class_="WlRRw IsqQVc fw-price-dn").get_text()
if variacao_diaria[0] =='−':
    color = "red"
else:
    color = "green"
print(variacao_diaria[0])
bolsa_nodia = customtkinter.CTkLabel(janela,text="Resumo da bolsa no dia: {} pontos \n variação de:".format(cotacao_da_bolsa))
bolsa_nodia.pack(padx=10,pady=5)
bolsa_nodia2 = customtkinter.CTkLabel(janela,text="{}".format(variacao_diaria[0:19]),text_color=color)
bolsa_nodia2.pack()
texto_consultar = customtkinter.CTkLabel(janela,text="CONSULTAR AÇÃO",font=("Arial",15))
texto_consultar.pack()
entrada = customtkinter.CTkEntry(janela,placeholder_text="Ticker da ação ")
entrada.pack()
contagem_de_erro = 0


def consultar():
    try:
        ticker = entrada.get()
        if len(ticker) == 0 and contagem_de_erro ==0:
           bolsa_nodia = customtkinter.CTkLabel(janela,text="Digite um ticker válido")
           bolsa_nodia.pack()
           contagem_de_erro =1
        else:
            urlstatusinvest = f'https://statusinvest.com.br/acoes/{ticker}'  
            sitestatusinvest = requests.get(urlstatusinvest,headers=headers) 
            soup = BeautifulSoup(sitestatusinvest.content,'html.parser')  
            lista = []
            valor_atual = soup.find_all('strong',class_="value")
            for itens in valor_atual:
                texto = itens.get_text()
                lista.append(itens.get_text())
                if len(lista) >=5:
                    break

            valores = {'valor_dia':lista[0],
                    'minimo_52_semanas':lista[1],
                    'maximo_52_semanas':lista[2],
                    'dy':lista[3],
                    'variacao':lista[4]}
            print(lista)
            janela2 = customtkinter.CTk()
            janela2.geometry("400x300")
            janela2.title("O acionista programador")
            nomedaacao = customtkinter.CTkLabel(janela2,text="Ação consultada: {}".format(ticker.upper()))
            nomedaacao.pack(padx=10,pady=10)
            resumo = customtkinter.CTkLabel(janela2,text="Valor atual: R${}\n Mínimo 52 semanas: R${}\n Máximo 52 semanas: R${}\n DY: {}%\n Variação nos ultimos 12 meses: {}".format(valores['valor_dia'], valores['minimo_52_semanas'], valores['maximo_52_semanas'],valores['dy'],valores['variacao']))
            resumo.pack(padx=10,pady=10)
            def telaemail():
                janelaemail = customtkinter.CTk()
                janelaemail.geometry("300x100")
                janelaemail.title("O acionista programador")
                textoemeail = customtkinter.CTkLabel(janelaemail,text="Digite o E-mail que recebera as informacões")
                textoemeail.pack()
                entradaemail = customtkinter.CTkEntry(janelaemail,placeholder_text="E-mail")
                entradaemail.pack()
                def botao_enviar():
                    try:
                        email_adress = entradaemail.get()
                        mandar_email("ACÃO CONSULTADA: {}\n Valor atual: R${}\n Mínimo 52 semanas: R${}\n Máximo 52 semanas: R${}\n DY: {}%\n Variação nos ultimos 12 meses: {}".format(ticker.upper(),valores['valor_dia'], valores['minimo_52_semanas'], valores['maximo_52_semanas'],valores['dy'],valores['variacao']), email_adress)
                        janela_confirmacao = customtkinter.CTk()
                        janela_confirmacao.geometry("200x70")
                        janela_confirmacao.title("O acionista programador")
                        texto_confirmacao = customtkinter.CTkLabel(janela_confirmacao,text="E-mail enviado com sucesso!")
                        texto_confirmacao.pack()
                        janelaemail.destroy()
                        janela_confirmacao.mainloop()
                        with open("leads.txt","a") as aqruivo:
                            aqruivo.write("\n{}".format(email_adress))
                    except:
                        print("erro ao enviar o email")
                botao_enviar_email = customtkinter.CTkButton(janelaemail,text="Enviar",command=botao_enviar)
                botao_enviar_email.pack(padx=10,pady=10)
                janelaemail.mainloop()
            botaoemail = customtkinter.CTkButton(janela2,text="Enviar informações por E-mail",command=telaemail)
            botaoemail.pack(padx=7,pady=7)
            botao_enviar_telegram = customtkinter.CTkButton(janela2,text="Enviar informações por Telegram")
            botao_enviar_telegram.pack(padx=7,pady=7)
            def abrirnoticias():
                url = f"https://finance.yahoo.com/quote/{ticker.upper()}.SA/"
                webbrowser.open(url)
            botaoconsultarnoticias = customtkinter.CTkButton(janela2,text="Consultar mais informações",command=abrirnoticias)
            botaoconsultarnoticias.pack(padx=7,pady=7)
            janela2.mainloop()
            bolsa_nodia = customtkinter.CTkLabel(janela,text="")
            bolsa_nodia.pack()
    except:
        bolsa_nodia = customtkinter.CTkLabel(janela,text="Digite um ticker válido")
        bolsa_nodia.pack()
botao = customtkinter.CTkButton(janela,text="Consultar",command=consultar)
botao.pack(padx=10,pady=10)
janela.mainloop()

