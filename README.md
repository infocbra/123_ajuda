# 123 Ajuda: Chatbot de Suporte em Saúde Mental

## Introdução

Este guia destina-se a facilitar o desenvolvimento e a implantação do chatbot "123 Ajuda", um projeto para suporte em saúde mental. Utilizando a plataforma Rasa Open Source, este documento orienta na configuração do ambiente, instalação, clonagem do repositório e expansão das funcionalidades do bot. Serve como um recurso para pesquisadores e desenvolvedores interessados em colaborar no aprimoramento deste instrumento de apoio psicológico.

## Tabela de Conteúdos

1. [Requisitos do Sistema](#requisitos-do-sistema)
2. [Instalação de Dependências](#instalação-de-dependências)
   - [Python](#python)
   - [Instalação do Visual Studio Code](#instalação-do-visual-studio-code)
3. [Configuração do Ambiente Rasa](#configuração-do-ambiente-rasa)
   - [Ambiente Virtual](#ambiente-virtual)
   - [Clonagem e Configuração do Repositório](#clonagem-e-configuração-do-repositório)
4. [Treinamento e Testes do Chatbot](#treinamento-e-testes-do-chatbot)

## Requisitos do Sistema

- **Sistema Operacional**: Windows 10 Pro ou superior, Linux, macOS
- **Processador**: Intel Core i3 ou superior (recomendado: Intel Core i3-10100T)
- **Memória RAM**: Mínimo de 4 GB, recomendado 8 GB ou mais (16 GB)
- **Espaço em Disco**: Pelo menos 5 GB de espaço livre
- **Python**: Versão 3.6 até 3.10
- **Outros**: Acesso à internet, Git

## Instalação de Dependências

### Python

1. Baixe e instale a versão mais recente compatível com o Windows:
   [Python Downloads](https://www.python.org/downloads/)
2. Selecione "Add Python to PATH" durante a instalação.
3. Verifique a instalação no PowerShell (ou o terminal de sua preferência):
   ```bash
   python --version
   ```
   - Saída esperada: Python 3.x.x
### Instalação do Visual Studio Code
- Baixe e instale o Visual Studio Code: [VS Code Downloads](https://code.visualstudio.com/download)
- Abra o VS Code após a instalação.
- Instale as seguintes extensões:
  - Python (para suporte de linguagem)
  - GitLens
  - Docker (se usar contêineres)
  - Git
  - Rasa (se disponível)
- Baixe e instale o Git: [Git Downloads](https://git-scm.com/downloads)
- Durante a instalação, configure o VS Code como editor padrão.
- Configuração do Terminal no Visual Studio Code:
  - Abra o terminal integrado no VS Code.
  - Altere para o shell desejado (por exemplo, Git Bash, se estiver no Windows).


## Configuração do Ambiente Rasa
### Ambiente Virtual
- Crie um diretório para o projeto:
 ```bash
mkdir projeto_123_ajuda
cd projeto_123_ajuda
 ```
- Crie e ative o ambiente virtual:
   
   - Windows
      ```bash
      py -3.10 -m venv venv  
      venv\Scripts\activate  
      ```
   - Linux/MacOS
      ```bash
      python3 -m venv venv 
      source venv/bin/activate 
      ```

- Atualize o pip e instale o Rasa:
```bash
python -m pip install --upgrade pip
pip install rasa
```
### Clonagem e Configuração do Repositório
- Clone o repositório:
```bash
git clone https://github.com/infocbra/123_ajuda.git
cd 123_ajuda
```
- Crie e ative o ambiente virtual:
   - Windows
      ```bash
      py -3.10 -m venv venv  
      venv\Scripts\activate  
      ```
   - Linux/MacOS
      ```bash
      python3 -m venv venv 
      source venv/bin/activate 
      ```
- Instale as dependências:
```bash
pip install -r requirements.txt
```
### Treinamento e Testes do Chatbot
Siga a documentação do Rasa para treinar o modelo, criar intenções e realizar testes:
[Rasa Documentation](https://rasa.com/docs/rasa/)
