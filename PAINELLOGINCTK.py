import customtkinter as ctk
#########################################################################
#CONFIGURAÇÃO DE CORES
#########################################################################
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
###################################################################
# FUNÇÕES
###################################################################
def fazer_login():
    usuario = entrar_usuario.get()
    senha = entrar_senha.get()

    print(f'Usuário: {usuario}')
    print(f'Senha: {senha}')
##################################################################
# CRIANDO A JANELA
###################################################################
janela = ctk.CTk()
janela.title("Login do Sistema")
janela.geometry("350x300")

janela.grid_rowconfigure(0, weight=1)
janela.grid_columnconfigure(0, weight=1)
#######################################################################
#####################################################################
#   CRIANDO FRAME
############################################################################
painel_login = ctk.CTkFrame(
    master=janela,
    fg_color="transparent"
)
  
painel_login.grid(
    row=0,
    column=0
)

#   PEIMEIRA LABEL
#####################################################################
label_usuario = ctk.CTkLabel(
    painel_login,
    text="Usuário",
    font=("Arial",20,"bold"),
    text_color="white"   
)
label_usuario.pack(pady=5)
###########################################################################
#   CRIANDO A PRIMEIRA ENTRY
#######################################################################
entrar_usuario = ctk.CTkEntry(
    master=painel_login,
    width=250,
    placeholder_text="Digite seu e-mail ou Usuário",
    justify="center"        
)
entrar_usuario.pack(pady=10)
##################################################################
#   CRIANDO A SEGUNDA LABEL
##################################################################
label_senha = ctk.CTkLabel(
    painel_login,
    text="Senha",
    font=("Arial",20,"bold"),
    text_color="white"

)
label_senha.pack(pady=5)
######################################################################
#   CRIANDO A SEGUNDA ENTRY
#####################################################################
entrar_senha = ctk.CTkEntry(
    master=painel_login,
    width=250,
    placeholder_text="Digite a sua Senha",
    justify="center",
    show="*"
)
entrar_senha.pack(pady=10)
###################################################################
#   CRIANDO BOTÃO
###################################################################
botao_login = ctk.CTkButton(
    painel_login,
    text=("LOGIN"),
    font=("Arial",15,"bold"),
    command=fazer_login
    

)
botao_login.pack(pady=10)


janela.mainloop()