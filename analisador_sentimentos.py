from bianca.parametros import obter_parametros
from bianca.modelo import ModeloIA


# Obtém a instância de parâmetros
parametros = obter_parametros()
modelo = ModeloIA("gpt-4o", parametros)


lista_de_produtos = ["Camisetas de algodão orgânico",
                     "Jeans feitos com materiais reciclados", "Maquiagem mineral"]


def carrega_arquivo(arquivo_produto) -> str:
    try:
        with open(f"./dados/avaliacoes-{arquivo_produto}.txt", "r", encoding="utf-8") as f:
            dados_arquivo = f.read()
    except FileNotFoundError:
        print(
            f"Arquivo de avaliações para o produto '{arquivo_produto}' não encontrado.")
        return ""

    return dados_arquivo


def salvando_arquivo(arquivo_produto, dados_arquivo):
    try:
        with open(f"./dados/analise-{arquivo_produto}.txt", "w", encoding="utf-8") as f:
            f.write(dados_arquivo)
    except Exception as e:
        raise e


def analisar_sentimentos(produto):
    prompt_sistema = f"""
    Analise o sentimento das avaliações do produto {produto} e retorne um resumo das avaliações.
    """
    for produto in lista_de_produtos:
        prompt_usuario = carrega_arquivo(produto)
        print(f"Iniciou a análise de sentimentos do produto {produto}")

        lista_mensagens = [
            {
                "role": "system",
                "content": prompt_sistema
            },
            {
                "role": "user",
                "content": prompt_usuario
            }
        ]

        resposta = modelo.cliente.chat.completions.create(
            model=modelo.modelo,
            messages=lista_mensagens
        )
        texto_resposta = resposta.choices[0].message.content
        salvando_arquivo(produto, texto_resposta)


# print(f"Iniciou a análise de sentimentos do produto {arquivo_produto}")
# Adicione aqui o código para análise de sentimentos usando 'modelo' e 'prompt_usuario'
# Exemplo:
# resultado = modelo.analisa_sentimentos(prompt_usuario)
# print(resultado)
