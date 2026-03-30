import json
import os
import tkinter as tk
from tkinter import messagebox
import ctypes
myappid = 'meu.projeto.casal.financeiro' 
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# Função para aceitar vírgula e transformar em número
def tratar_valor(texto_digitado):
    if texto_digitado == "": # Se estiver vazio, considera como zero
        return 0.0
    valor_limpo = texto_digitado.replace(',', '.')
    return float(valor_limpo)

# --- FUNÇÕES DE ATALHO DE TECLADO ---
def pular_para_b(event):
    entrada_b.focus()

def pular_para_nome_gasto(event):
    entrada_nome_gasto.focus()

def pular_para_valor_gasto(event):
    entrada_valor_gasto.focus()

def enter_adicionar_gasto(event):
    adicionar_gastos()
    entrada_nome_gasto.focus()

def atalho_relatorio(event):
    gerar_relatorio()
    return "break"

# --- FUNÇÕES DE CÁLCULO E LÓGICA ---
def calcular(event=None):
    try:
        # 1. Pega os salários das caixinhas
        sal_a = tratar_valor(entrada_a.get())
        sal_b = tratar_valor(entrada_b.get())
        renda_total = sal_a + sal_b

        # 2. SOMA TUDO QUE ESTÁ NA LISTA AGORA
        # Isso ignora variáveis externas e olha direto para o que você vê na tela
        total_dos_gastos = sum(g[1] for g in lista_gastos)
        
        # 3. Faz a conta final
        saldo_final = renda_total - total_dos_gastos

        # 4. Atualiza os textos na tela
        label_resumo_renda.config(text=f"Renda Total: R$ {renda_total:.2f}")
        
        if saldo_final >= 0:
            label_resumo_saldo.config(text=f"Saldo restante: R$ {saldo_final:.2f}", fg="green")
        else:
            label_resumo_saldo.config(text=f"Faltando: R$ {abs(saldo_final):.2f}", fg="red")
    except:
        # Se o usuário apagar tudo na caixinha, ele não dá erro
        pass
    salvar_dados()

def salvar_dados():
    dados = {
        "renda_a": entrada_a.get(),
        "renda_b": entrada_b.get(),
        "gastos": lista_gastos
    }
    with open("dados_financeiros.json", "w") as arquivos:
        json.dump(dados, arquivos)

def carregar_dados():
    if os.path.exists("dados_financeiros.json"):
        with open("dados_financeiros.json", "r") as arquivos:
            dados = json.load(arquivos)
            
            # 1. Limpa o que estiver nas caixinhas para não amontoar número
            entrada_a.delete(0, tk.END)
            entrada_b.delete(0, tk.END)
            
            # 2. Coloca os valores que estavam salvos
            entrada_a.insert(0, dados.get("renda_a", ""))
            entrada_b.insert(0, dados.get("renda_b", ""))
            
            # 3. Puxa a lista de gastos
            global lista_gastos, total_contas
            lista_gastos = dados.get("gastos", [])
            total_contas = sum(g[1] for g in lista_gastos)
            
            # 4. Atualiza a tela (Usa o nome 'calcular' que é o que você tem)
            atualizar_lista_tela()
            calcular()
# --- 1: FUNÇÃO PARA DESENHAR A LISTA COM O "X" ---
def atualizar_lista_tela():
    # Limpa o que já existe
    for widget in frame_lista_interna.winfo_children():
        widget.destroy()

    # 2. Desenha cada gasto com o nome, valor e o botão X
    for i, gasto in enumerate(lista_gastos):
        nome, valor = gasto[0], gasto[1]
        linha = tk.Frame(frame_lista_interna)
        linha.pack(fill="x", pady=2)

        tk.Label(linha, text=f"• {nome}: R$ {valor:.2f}").pack(side="left")
        tk.Button(linha, text=" X ", fg="white", bg="#ff4d4d", bd=0, 
                  command=lambda idx=i: excluir_gasto_especifico(idx)).pack(side="right")
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# --- 2: FUNÇÃO PARA EXCLUIR UM ITEM ESPECÍFICO ---
def excluir_gasto_especifico(index):
    global total_contas
    gasto_removido = lista_gastos.pop(index) 
    total_contas -= gasto_removido[1]        
    atualizar_lista_tela() 
    
    # --- ATUALIZA O SALDO NA MARRA (Sem usar o calcular) ---
    texto_a = entrada_a.get().replace('.', '') # Limpa pontos para evitar erro oculto
    texto_b = entrada_b.get().replace('.', '')
    renda = tratar_valor(texto_a) + tratar_valor(texto_b)
    saldo = renda - sum(g[1] for g in lista_gastos)
    
    if saldo >= 0:
        label_resumo_saldo.config(text=f"Saldo restante: R$ {saldo:.2f}", fg="green")
    else:
        label_resumo_saldo.config(text=f"Faltando: R$ {abs(saldo):.2f}", fg="red")
    salvar_dados()

def adicionar_gastos():
    global total_contas
    try:
        nome = entrada_nome_gasto.get()
        texto_valor = entrada_valor_gasto.get()
        
        if texto_valor != "":
            valor = tratar_valor(texto_valor)

            lista_gastos.append((nome, valor))
            total_contas += valor

            atualizar_lista_tela() 

            # --- ATUALIZA O SALDO NA MARRA (Sem usar o calcular) ---
            texto_a = entrada_a.get().replace('.', '')
            texto_b = entrada_b.get().replace('.', '')
            renda = tratar_valor(texto_a) + tratar_valor(texto_b)
            saldo = renda - sum(g[1] for g in lista_gastos)
            
            if saldo >= 0:
                label_resumo_saldo.config(text=f"Saldo restante: R$ {saldo:.2f}", fg="green")
            else:
                label_resumo_saldo.config(text=f"Faltando: R$ {abs(saldo):.2f}", fg="red")

            entrada_nome_gasto.delete(0, tk.END)
            entrada_valor_gasto.delete(0, tk.END)
            entrada_nome_gasto.focus()
            
    except ValueError:
        messagebox.showerror("Erro", "Por favor, digite um valor válido!")
    salvar_dados()

def gerar_relatorio():
    try:
        sal_a = tratar_valor(entrada_a.get())
        sal_b = tratar_valor(entrada_b.get())
        renda_total = sal_a + sal_b
        
        
        total_de_contas_da_lista = sum(g[1] for g in lista_gastos)
        saldo_final = renda_total - total_de_contas_da_lista

        resumo = f"Renda Total: R$ {renda_total:.2f}\n"
        resumo += f"Total de Contas: R$ {total_de_contas_da_lista:.2f}\n"
        resumo += "-"*30 + "\n"
        
        # --- NOVIDADE 3: MOSTRAR A LISTA DE GASTOS NO RELATÓRIO ---
        resumo += "DETALHAMENTO DOS GASTOS:\n"
        if len(lista_gastos) == 0:
            resumo += "Nenhum gasto cadastrado.\n"
        else:
            for gasto in lista_gastos:
                resumo += f" - {gasto[0]}: R$ {gasto[1]:.2f}\n"
        
        resumo += "-"*30 + "\n"

        if saldo_final >= 0:
            resumo += f"SOBRA FINAL: R$ {saldo_final:.2f} ✅"
        else:
            resumo += f"FALTANDO: R$ {abs(saldo_final):.2f} ❌"  
        
        messagebox.showinfo("Relatório Mensal", resumo)
    
    except ValueError:
        messagebox.showerror("Erro", "Certifique-se de que os salários estão preenchidos!")
    
def resetar_tudo():
    global total_contas, lista_gastos
    if messagebox.askyesno("Confirmar", "Deseja apagar TODOS os gastos e recomeçar?"):
        lista_gastos = []
        total_contas = 0.0
        
        atualizar_lista_tela() # Limpa a lista visual
        entrada_a.delete(0, tk.END)
        entrada_b.delete(0, tk.END)

        calcular() 
        entrada_a.focus()

# --- INÍCIO DA INTERFACE ---
janela = tk.Tk()
janela.title("Gestor Financeiro do Casal")
janela.geometry("450x700")
# --- CONFIGURAÇÃO DO ÍCONE ---
try:
    import os
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_icone = os.path.join(diretorio_atual, "icone.png")

    foto_icone = tk.PhotoImage(file=caminho_icone)
    janela.iconphoto(False, foto_icone)
except Exception as e:
    print(f"Erro ao carregar ícone: {e}")

# 1. ENTRADA DE SALÁRIO A
label_a = tk.Label(janela, text="Salário da Pessoa A (R$):")
label_a.pack()
entrada_a = tk.Entry(janela)
entrada_a.pack(pady=5)

# 2. ENTRADA DE SALÁRIO B
label_b = tk.Label(janela, text="Salário da Pessoa B (R$):")
label_b.pack()
entrada_b = tk.Entry(janela)
entrada_b.pack(pady=5)

# 3. BOTÃO DE CÁLCULO
botao_calcular = tk.Button(janela, text="Calcular Renda Total", command=calcular)
botao_calcular.pack(pady=10)

# --- MEMÓRIA ---
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

# --- BOTÕES DE EDIÇÃO ---

botao_reset = tk.Button(janela, text="Limpar Tudo (Novo Mês)", command=resetar_tudo, fg="red")
botao_reset.pack(pady=5)

botao_relatorio = tk.Button(janela, text="Gerar relatório Final", command=gerar_relatorio, bg="#d1ffd1")
botao_relatorio.pack(pady=10)

# --- PAINEL DE RESULTADOS EM TEMPO REAL ---
tk.Label(janela, text="--- RESUMO ATUAL ---", font=("Arial", 10, "bold")).pack(pady=10)

label_resumo_renda = tk.Label(janela, text="Renda Total: R$ 0.00", font=("Arial", 10))
label_resumo_renda.pack()
label_resumo_saldo = tk.Label(janela, text="Saldo restante: R$ 0.00", font=("Arial", 12, "bold"))
label_resumo_saldo.pack(pady=10)

# --- NOVIDADE 4: O "QUADRO" ONDE A LISTA COM O 'X' VAI APARECER ---
# 1. container para segurar a lista e a barra juntas
container_lista = tk.Frame(janela)
container_lista.pack(fill="both", expand=True, padx=20)

# 2. Canvas (a área que desliza) e a Scrollbar (a barra)
canvas = tk.Canvas(container_lista, height=200) # Altura da área visível
scrollbar = tk.Scrollbar(container_lista, orient="vertical", command=canvas.yview)

# 3. o Frame INTERNO (onde os gastos realmente moram)
frame_lista_interna = tk.Frame(canvas)

# 4. Conectamos um no outro
canvas.configure(yscrollcommand=scrollbar.set)

# 5. Colocamos na tela: barra na direita, lista na esquerda
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# 6. Criamos a "janela" dentro do canvas para mostrar o frame interno
canvas.create_window((0,0), window=frame_lista_interna, anchor="nw", width=380)

# Atalhos do Enter e Tab
entrada_a.bind("<Return>", pular_para_b)
entrada_b.bind("<Return>", pular_para_nome_gasto)
entrada_nome_gasto.bind("<Return>", pular_para_valor_gasto)
entrada_valor_gasto.bind("<Return>", enter_adicionar_gasto)
entrada_a.bind("<KeyRelease>", calcular)
entrada_b.bind("<KeyRelease>", calcular)
janela.bind("<Tab>", atalho_relatorio)

entrada_a.focus()
carregar_dados()
janela.mainloop()