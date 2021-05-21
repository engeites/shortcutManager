

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

    def get_tokens(self):
        return self.__load_my_tokens(self.file)