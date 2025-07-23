from atualizador import AtualizadorPlanilhaCompras

def main():
    url = "https://fa-euld-saasfaprod1.fa.ocs.oraclecloud.com/fscmUI/faces/FuseWelcome?_adf.ctrl-state=bup08swrk_118"  # Substitua pela URL real
    bot = AtualizadorPlanilhaCompras(headless=False)

    try:
        bot.atualizar_planilha(url)
    finally:
        bot.fechar()

if __name__ == "__main__":
    main()
