class View():
    def start(self):
        return self.menu()

    def menu(self):
        print("Menu:")
        print("1. Popular a tabela 'Usuários'")
        print("2. Popular a tabela 'Canais'")
        print("3. Popular a tabela 'Categories'")
        print("4. Popular a tabela 'Streams'")
        print("5. Popular a tabela 'Videos'")
        print("6. Sair")

        # Pegar escolha do usuário
        opcao = int(input("\nDigite o número da opção desejada: "))
        return opcao
