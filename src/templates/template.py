from src.models.password import Password
from src.views.passord_views import FernetHasher


def app():
    action = input("Digite A (adiconar) ou P (Pesquisar) para uma senha:")
    match action:
        case "A":
            if len(Password.get()) == 0:
                key, path = FernetHasher.create_key(archive=True)
                print("Chave criada com sucesso! Guarde com CUIDADO!")
                print(f"Chave: {key.decode('utf-8')}")
                if path:
                    print(
                        "Chave salva no arquivo, lembre-se de remover o arquivo apos o transferir de local!"
                    )
                    print(f"Caminho: {path}")
            if len(Password.get()) > 0:
                key = input(
                    "Digite sua chave usada para criptografia, use sempre a mesma chave: "
                )

            domain = input("Domínio: ")
            password = input("Digite a senha: ")
            fernet = FernetHasher(key)
            password_model = Password(
                domain=domain, password=fernet.encrypt(password).decode("utf-8")
            )
            password_model.save()
        case "P":
            domain = input("Domínio: ")
            key = input("Key: ")
            fernet = FernetHasher(key)
            data = Password.get()
            password = ""
            for i in data:
                if domain in i["domain"]:
                    password = fernet.decrypt(i["password"])
                if password:
                    print(f"Sua senha: {password.decode()}")
                else:
                    print("Nenhuma senha encontrada para esse domínio.")
