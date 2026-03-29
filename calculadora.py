import tkinter as tk
from tkinter import messagebox # Para aquelas janelinhas de avisos/erro

# Função para aceitar vírgula e transformar em número
def tratar_valor(texto_digitado):
    valor_limpo = texto_digitado.replace(',', '.')
    return float(valor_limpo)

def calcular():
    try:
        # Pegandio os valores das caixinhas brancas da janela
        sal_a = tratar_valor(entrada_a.get())
        sal_b = tratar_valor(entrada_b.get())

        renda_total = sal_a + sal_b

        # Mostrando o resultado numa janelinha de alerta
        messagebox.showinfo("Resultado", f"Renda Total: R$ {renda_total:.2f}")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, digite apenas números nos salários!")
janela = tk.Tk()
janela.title("Gestor Financeiro do Casal")
janela.geometry("400x500") #definir o tamanho da janela

def adicionar_gastos():
    global total_contas # Avisa que vamos mexer no total que está lá fora
    try:
        nome = entrada_nome_gasto.get()
        valor = tratar_valor(entrada_valor_gasto.get())

        # Salva na lista e soma no total
        lista_gastos.append((nome, valor))
        total_contas += valor

        # Limpa as caixinhas para você digitar o próximo gasto
        entrada_nome_gasto.delete(0, tk.END)
        entrada_valor_gasto.delete(0, tk.END)

        messagebox.showinfo("Sucesso", f"Gasto '{nome}' acionado!")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, digite um valor valido para o gasto!")

def gerar_relatorio():
    try:
        # 1. Pega a renda total 
        sal_a = tratar_valor(entrada_a.get())
        sal_b = tratar_valor(entrada_b.get())
        renda_total = sal_a + sal_b

        # 2. Calcular o Saldo
        # total_contras é aquela variável que fomos somando no 'adicionar_gastos'
        saldo_final = renda_total - total_contas

        # 3. Resumo do texto do relatório
        resumo = f"Renda Total: R$ {renda_total:.2f}\n"
        resumo += f"Total de Contas: R$ {total_contas:.2f}\n"
        resumo += "-"*20 + "\n"

        if saldo_final >= 0:
            resumo += f"SOBRA FINAL: R$ {saldo_final:.2f} ✅"
        else:
            resumo += f"FALTANDO: R$ {abs(saldo_final):.2f} ❌"  
        
        # 4. Mostra tudo na tela
        messagebox.showinfo("Relatório Mensal", resumo)
    
    except ValueError:
        messagebox.showerror("Erro", "Certifique-se de que os salários estão preenchidos!")
# 1. ENTRADA DE SALÁRIO A
label_a = tk.Label(janela, text="Salário da Pessoa A (R$):")
label_a.pack()
entrada_a = tk.Entry(janela) #caixinha branca para digitar o salário da pessoa A
entrada_a.pack(pady=5)

# 2. ENTRADA DE SALÁRIO B
label_b = tk.Label(janela, text="Salário da Pessoa B (R$):")
label_b.pack()
entrada_b = tk.Entry(janela) #caixinha branca para digitar o salário da pessoa B
entrada_b.pack(pady=5)

# 3. BOTÃO DE CÁLCULO
botao_calcular = tk.Button(janela, text="Calcular Renda Total", command=calcular)
botao_calcular.pack(pady=26)

#--- MEMÓRIA ---
lista_gastos = [] 
total_contas = 0.0

# --- CAMPOS DE GASTOS ---
tk.Label(janela, text="--- CADASTRO DE GASTOS ---", font=("Arial", 10, "bold")).pack(pady=10) 

tk.Label(janela, text="Nome da Conta:").pack()
entrada_nome_gasto = tk.Entry(janela)
entrada_nome_gasto.pack()

tk.Label(janela, text="Valor da Conta (R$):").pack()
entrada_valor_gasto = tk.Entry(janela)
entrada_valor_gasto.pack()

botao_add = tk.Button(janela, text="Adicionar Gasto", command=adicionar_gastos)
botao_add.pack(pady=10)

# --- BOTÃO DE RELATÓRIO ---
botao_relatorio = tk.Button(
    janela,
    text="Gerar relatório Final",
    command=gerar_relatorio,
    bg="#d1ffd1" # um verdinho suave para destacar o botão de relatório
)
botao_relatorio.pack(pady=20)

janela.mainloop() #manter a janela aberta