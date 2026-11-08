# 🔐 Neon Login — Tela de Login Moderna com CustomTkinter

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-1f6feb)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)

Sistema de **login e cadastro** com visual moderno em modo escuro, feito com **CustomTkinter**, com usuários salvos em **SQLite** e senhas protegidas por **hash**.

Serve de base para qualquer aplicativo desktop em Python que precise de autenticação.

## ✨ Funcionalidades

- 🌙 Interface moderna em **dark mode**
- 📝 **Cadastro de usuários** e **login** na mesma tela
- 🔒 Senhas com **PBKDF2-SHA256 + salt**: nunca ficam em texto puro
- ✅ Validações: campos obrigatórios, tamanho mínimo da senha e formato de e-mail
- 👁️ Opção **"Mostrar senha"**
- ⌨️ **Enter** faz o login
- 🚪 Tela de boas-vindas com botão **Sair**

## 🚀 Como executar

```bash
pip install -r requirements.txt
python login_app.py
```

Clique em **"Não tem conta? Cadastre-se"**, crie um usuário e depois faça o login.

## 🧠 Como a senha é protegida

```python
salt = secrets.token_hex(16)
hash = hashlib.pbkdf2_hmac("sha256", senha.encode(), bytes.fromhex(salt), 200_000)
```

Cada usuário tem um *salt* diferente, então duas senhas iguais geram hashes diferentes no banco.

## 👨‍💻 Autor

**Walace Soares Vidigal Junior** · [GitHub](https://github.com/walacevdgicm-ops)

Licença [MIT](LICENSE)
