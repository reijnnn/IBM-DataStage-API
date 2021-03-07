def encode_string(s_value):
    return s_value.encode("utf-8")


def decode_bytes(b_value):
    return b_value.decode("cp1251", errors="ignore")


def convert_char_p_to_list(char_p):
    words_list = []

    if not char_p:
        return words_list

    start_word_pos = 0
    it = 0
    while True:
        if char_p[it] == b'\x00':
            if it - 1 >= 0 and char_p[it - 1] == b'\x00':
                break
            words_list.append(char_p[start_word_pos:it])
            start_word_pos = it + 1
        it = it + 1

    return words_list
