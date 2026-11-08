import customtkinter as ctk
import sqlite3
import hashlib
import hmac
import secrets
import os
import re

#########################################################################
# CONFIGURAÇÃO DE CORES
#########################################################################
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

COR_ERRO = "#ff6b6b"
COR_SUCESSO = "#51cf66"

#########################################################################
# BANCO DE DADOS (SQLite) E SEGURANÇA
# As senhas NUNCA são salvas em texto puro: usamos PBKDF2-SHA256 com salt.
#########################################################################
CAMINHO_BD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "usuarios.db")


def conectar():
    return sqlite3.connect(CAMINHO_BD)


def criar_tabela():
    with conectar() as conexao:
        conexao.execute(
            """CREATE TABLE IF NOT EXISTS usuarios (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   usuario TEXT UNIQUE NOT NULL,
                   senha_hash TEXT NOT NULL
               )"""
        )


def gerar_hash(senha):
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", senha.encode(), bytes.fromhex(salt), 200_000).hex()
    return f"{salt}${digest}"


def senha_confere(senha, armazenado):
    salt, digest = armazenado.split("$")
    calculado = hashlib.pbkdf2_hmac("sha256", senha.encode(), bytes.fromhex(salt), 200_000).hex()
    return hmac.compare_digest(calculado, digest)


def cadastrar_usuario(usuario, senha):
    try:
        with conectar() as conexao:
            conexao.execute(
                "INSERT INTO usuarios (usuario, senha_hash) VALUES (?, ?)",
                (usuario, gerar_hash(senha)),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def autenticar(usuario, senha):
    with conectar() as conexao:
        linha = conexao.execute(
            "SELECT senha_hash FROM usuarios WHERE usuario = ?", (usuario,)
        ).fetchone()
    return linha is not None and senha_confere(senha, linha[0])


###################################################################
# FUNÇÕES DA TELA
###################################################################
modo_cadastro = False


def mostrar_mensagem(texto, cor):
    label_mensagem.configure(text=texto, text_color=cor)


def validar_campos(usuario, senha):
    if not usuario or not senha:
        return "Preencha usuário e senha."
    if modo_cadastro:
        if len(senha) < 6:
            return "A senha precisa ter pelo menos 6 caracteres."
        if "@" in usuario and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", usuario):
            return "E-mail inválido."
    return None


def fazer_login(event=None):
    usuario = entrar_usuario.get().strip().lower()
    senha = entrar_senha.get()

    erro = validar_campos(usuario, senha)
    if erro:
        mostrar_mensagem(erro, COR_ERRO)
        return

    if modo_cadastro:
        if cadastrar_usuario(usuario, senha):
            mostrar_mensagem("Conta criada! Agora faça o login.", COR_SUCESSO)
            alternar_modo()
        else:
            mostrar_mensagem("Esse usuário já existe.", COR_ERRO)
        return

    if autenticar(usuario, senha):
        abrir_painel(usuario)
    else:
        mostrar_mensagem("Usuário ou senha incorretos.", COR_ERRO)
        entrar_senha.delete(0, "end")


def alternar_modo():
    global modo_cadastro
    modo_cadastro = not modo_cadastro
    botao_login.configure(text="CRIAR CONTA" if modo_cadastro else "LOGIN")
    botao_alternar.configure(
        text="Já tenho conta? Entrar" if modo_cadastro else "Não tem conta? Cadastre-se"
    )


def alternar_ver_senha():
    entrar_senha.configure(show="" if check_ver_senha.get() else "*")


def abrir_painel(usuario):
    painel_login.grid_forget()
    painel_boas_vindas = ctk.CTkFrame(master=janela, fg_color="transparent")
    painel_boas_vindas.grid(row=0, column=0)
    ctk.CTkLabel(
        painel_boas_vindas, text=f"Bem-vindo, {usuario}! 👋", font=("Arial", 20, "bold")
    ).pack(pady=20)
    ctk.CTkButton(
        painel_boas_vindas, text="SAIR", fg_color="#c92a2a", hover_color="#a51111",
        command=lambda: sair(painel_boas_vindas),
    ).pack(pady=10)


def sair(painel_boas_vindas):
    painel_boas_vindas.destroy()
    entrar_senha.delete(0, "end")
    mostrar_mensagem("", COR_SUCESSO)
    painel_login.grid(row=0, column=0)


##################################################################
# CRIANDO A JANELA
###################################################################
criar_tabela()

janela = ctk.CTk()
janela.title("Login do Sistema")
janela.geometry("380x420")
janela.resizable(False, False)

janela.grid_rowconfigure(0, weight=1)
janela.grid_columnconfigure(0, weight=1)

############################################################################
#   CRIANDO FRAME
############################################################################
painel_login = ctk.CTkFrame(master=janela, fg_color="transparent")
painel_login.grid(row=0, column=0)

#####################################################################
#   USUÁRIO
#####################################################################
label_usuario = ctk.CTkLabel(painel_login, text="Usuário", font=("Arial", 20, "bold"), text_color="white")
label_usuario.pack(pady=5)

entrar_usuario = ctk.CTkEntry(
    master=painel_login, width=250, placeholder_text="Digite seu e-mail ou Usuário", justify="center"
)
entrar_usuario.pack(pady=10)

##################################################################
#   SENHA
##################################################################
label_senha = ctk.CTkLabel(painel_login, text="Senha", font=("Arial", 20, "bold"), text_color="white")
label_senha.pack(pady=5)

entrar_senha = ctk.CTkEntry(
    master=painel_login, width=250, placeholder_text="Digite a sua Senha", justify="center", show="*"
)
entrar_senha.pack(pady=10)

check_ver_senha = ctk.CTkCheckBox(painel_login, text="Mostrar senha", command=alternar_ver_senha)
check_ver_senha.pack(pady=5)

###################################################################
#   BOTÕES E MENSAGENS
###################################################################
botao_login = ctk.CTkButton(painel_login, text="LOGIN", font=("Arial", 15, "bold"), command=fazer_login)
botao_login.pack(pady=10)

botao_alternar = ctk.CTkButton(
    painel_login, text="Não tem conta? Cadastre-se", fg_color="transparent",
    hover_color="#1f2937", command=alternar_modo,
)
botao_alternar.pack(pady=2)

label_mensagem = ctk.CTkLabel(painel_login, text="", font=("Arial", 12))
label_mensagem.pack(pady=5)

# ENTER também faz login
janela.bind("<Return>", fazer_login)
entrar_usuario.focus()

janela.mainloop()
