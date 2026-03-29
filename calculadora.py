import tkinter as tk
from tkinter import messagebox # Para aquelas janelinhas de avisos/erro

# Função para aceitar vírgula e transformar em número
def tratar_valor(texto_digitado):
    valor_limpo = texto_digitado.replace(',', '.')
    return float(valor_limpo)

# Função para pular do Salário A para o B
def pular_para_b(event):
    entrada_b.focus()

# Função para pular do Salário B para o Nome do Gasto
def pular_para_nome_gasto(event):
    entrada_nome_gasto.focus()

# Função para pular do Nome do Gasto para o Valor
def pular_para_valor_gasto(event):
    entrada_valor_gasto.focus()

# Função para Adicionar Gasto com o Enter e voltar para o Nome (O Loop)
def enter_adicionar_gasto(event):
    adicionar_gastos() # Chama a função que você já tem
    entrada_nome_gasto.focus() # Volta o cursor para o Nome para a próxima conta

# Função para gerar relatório com a tecla TAB
def atalho_relatorio(event):
    gerar_relatorio()
    return "break" # Isso evita que o TAB mude o foco para outro lugar estranho

def calcular(event=None):
    try:
        # Pega o que está escrito
        texto_a = entrada_a.get()
        texto_b = entrada_b.get()

        # Pegando os valores das caixinhas brancas da janela
        sal_a = tratar_valor(texto_a) if texto_a != "" else 0.0
        sal_b = tratar_valor(texto_b) if texto_b != "" else 0.0

        renda_total = sal_a + sal_b
        saldo_final = renda_total - total_contas

        # Atualiza os textos na janela principal
        label_resumo_renda.config(text=f"Renda Total: R$ {renda_total: .2f}")
        
        if saldo_final >= 0:
            label_resumo_saldo.config(text=f"Saldo restante: R$ {saldo_final: .2f}", fg="green")
        else:
            label_resumo_saldo.config(text=f"Faltando: R$ {abs(saldo_final):.2f}", fg="red")
    except ValueError:
        # Aqui não precisa de erro crítico, ele só não atualiza se  não tiver número
        pass

janela = tk.Tk()
janela.title("Gestor Financeiro do Casal")
janela.geometry("450x700") #definir o tamanho da janela

def adicionar_gastos():
    global total_contas
    try:
        nome = entrada_nome_gasto.get()
        texto_valor = entrada_valor_gasto.get()
        
        # Só adiciona se o valor não estiver vazio
        if texto_valor != "":
            valor = tratar_valor(texto_valor)

            # 1. Salva na memória
            lista_gastos.append((nome, valor))
            total_contas += valor

            # 2. ATUALIZA O PAINEL AO VIVO
            nomes_exibicao = ", ".join([g[0] for g in lista_gastos])
            label_lista_nomes.config(text=f"Gastos: {nomes_exibicao}")
            
            # Chama a função calcular para atualizar o saldo na tela
            calcular() 

            # --- O SEGREDO DO LOOP ESTÁ AQUI ---
            # 3. Limpa as caixinhas AUTOMATICAMENTE
            entrada_nome_gasto.delete(0, tk.END)  # Apaga o nome que você digitou
            entrada_valor_gasto.delete(0, tk.END) # Apaga o valor que você digitou
            
            # 4. Volta o cursor para o campo de NOME para o próximo gasto
            entrada_nome_gasto.focus()
            
    except ValueError:
        messagebox.showerror("Erro", "Por favor, digite um valor válido para o gasto!")

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
    
def desfazer_ultimo_gasto():
    global total_contas
    if lista_gastos:
        # 1. remove o último item da lista e pega o valor dele
        ultimo_gasto = lista_gastos.pop() # Remove (nome, valor)
        nome_removido = ultimo_gasto[0]
        valor_removido = ultimo_gasto[1]

        # 2. subtrai do total
        total_contas -= valor_removido

        # 3. Atualiza a tela (NOVIDADE AQUI)
        nomes_exibicao = ", ".join([g[0] for g in lista_gastos])
        label_lista_nomes.config(text=f"Gastos: {nomes_exibicao if nomes_exibicao else '(Nenhum)'}")
        
        calcular() # Recalcula o saldo final

        messagebox.showinfo("Editado", f"O gasto '{nome_removido}' foi removido!")
    else:
        messagebox.showwarning("Aviso", "Não há gastos para remover!")

def resetar_tudo():
    global total_contas, lista_gastos
    if messagebox.askyesno("Confirmar", "Deseja apagar TODOS os gastos e recomeçar?"):
        lista_gastos = []
        total_contas = 0.0
        # Apagfa os testos
        label_lista_nomes.config(text="Gastos: (Nenhum)")
        entrada_a.delete(0, tk.END)
        entrada_b.delete(0, tk.END)

        # Zera o painel e volta o foco para o primeiro campo
        calcular() 
        entrada_a.focus()

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

# --- BOTÕES DE EDIÇÃO (NOVIDADE) ---
# Botão para apagar o último que você digitou errado
botao_desfazer = tk.Button(
    janela, 
    text="Desfazer Último Gasto", 
    command=desfazer_ultimo_gasto,
    bg="#ffcccb" # Um vermelhinho claro para indicar "remover"
)
botao_desfazer.pack(pady=5)

# Botão para limpar o mês todo
botao_reset = tk.Button(
    janela, 
    text="Limpar Tudo (Novo Mês)", 
    command=resetar_tudo,
    fg="red"
)
botao_reset.pack(pady=5)
# -----------------------------------

# --- BOTÃO DE RELATÓRIO ---
botao_relatorio = tk.Button(
    janela,
    text="Gerar relatório Final",
    command=gerar_relatorio,
    bg="#d1ffd1" # um verdinho suave para destacar o botão de relatório
)
botao_relatorio.pack(pady=20)

# ---  PAINEL DE RESULTADOS EM TEMPO REAL ---
tk.Label(janela, text="--- RESUMO ATUAL ---", font=("Arial", 10, "bold")).pack(pady=10)

# Mostra a soma dos dois salários
label_resumo_renda = tk.Label(janela, text="Renda Total: R$ 0.00", font=("Arial", 10))
label_resumo_renda.pack()

# Mostar a lista de nomes dos gastos
label_lista_nomes = tk.Label(janela, text="Gastos: (Nenhum)", font=("Arial", 9), fg="gray")
label_lista_nomes.pack()

# Mostra quanto sobra no final
label_resumo_saldo = tk.Label(janela, text="Saldo restante: R$0,00", font=("Arial", 12, "bold"))
label_resumo_saldo.pack()

# Atalhos do Enter (Return)
entrada_a.bind("<Return>", pular_para_b)
entrada_b.bind("<Return>", pular_para_nome_gasto)
entrada_nome_gasto.bind("<Return>", pular_para_valor_gasto)
entrada_valor_gasto.bind("<Return>", enter_adicionar_gasto)

# atualiza enquanto digita!
entrada_a.bind("<KeyRelease>", calcular)
entrada_b.bind("<KeyRelease>", calcular)

# Atalho do TAB para o Relatório (em qualquer lugar da janela)
janela.bind("<Tab>", atalho_relatorio)

# Iniciar o programa já com o cursor no Salário A
entrada_a.focus()

janela.mainloop() #manter a janela aberta