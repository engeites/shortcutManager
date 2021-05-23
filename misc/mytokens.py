

# GET ALL MY TOKEN SLUG FROM FILE
class TokenLoader:
    file = "settings/my_tokens.txt"

    @staticmethod
    def __load_my_tokens(file):
        token_list = []
        with open(file, 'r', encoding="utf-8") as fout:
            r = fout.readlines()
            for i in r:
                token_list.append(i.strip())
        return token_list

    def __rewrite_file(self, file, token):
        tokens = self.__load_my_tokens(self.file)
        tokens.append(token)
        with open(file, 'w', encoding="utf-8") as fout:
            for i in tokens:
                fout.write(f"{i}\n")
        return True

    def get_tokens(self):
        return self.__load_my_tokens(self.file)

    def add_token(self, token):
        return self.__rewrite_file(self.file, token)


def refresh_tokens(token):
    tokenloader = TokenLoader()
    tokenloader.add_token(token)