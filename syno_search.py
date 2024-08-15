cyrillic_key = "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"

encoded_key = "%C0%E0%C1%E1%C2%E2%C3%E3%C4%E4%C5%E5%A8%B8%C6%E6%C7%E7%C8%E8%C9%E9%CA%EA%CB%EB%CC%EC%CD%ED%CE%EE%CF%EF%D0%F0%D1%F1%D2%F2%D3%F3%D4%F4%D5%F5%D6%F6%D7%F7%D8%F8%D9%F9%DA%FA%DB%FB%DC%FC%DD%FD%DE%FE%DF%FF"

def encode_char(char):
    if type(char) != str or len(char) != 1:
        print("char_to_marc8 received invalid input")
    ind = cyrillic_key.index(char)
    return encoded_key[3*ind:3*ind+3]

def encode(string):
    ret = ""
    for char in string:
        ret = ret + encode_char(char)
    return ret

print(encode("тест"))
    
