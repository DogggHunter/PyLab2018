def convert_to_dec(letter):
    if len(letter) != 1:
        return
    return ord(letter)


def convert_to_letter(dec, shift, _type):
    cod = 0
    if _type == 'encode':
        cod = 1
    elif _type == 'decode':
        cod = -1

    new_dec = dec
    if 48 <= dec <= 57:
        new_dec += (shift % 10) * cod
        if new_dec > 57:
            return chr(new_dec - 10)
        elif new_dec < 48:
            return chr(new_dec + 10)
        return chr(new_dec)
    elif 65 <= dec <= 90:
        new_dec += (shift % 26) * cod
        if new_dec > 90:
            return chr(new_dec - 26)
        elif new_dec < 65:
            return chr(new_dec + 26)
        return chr(new_dec)
    elif 97 <= dec <= 122:
        new_dec += (shift % 26) * cod
        if new_dec > 122:
            return chr(new_dec - 26)
        elif new_dec < 97:
            return chr(new_dec + 26)
    else:
        return chr(dec)
    return chr(new_dec)


def encode(text, shift):
    new_text = ''
    for letter in text:
        new_text += convert_to_letter(convert_to_dec(letter), shift, 'encode')
    return new_text


def decode(text, shift):
    new_text = ''
    for letter in text:
        new_text += convert_to_letter(convert_to_dec(letter), shift, 'decode')
    return new_text


def main():
    text = 'abcdd fsfds 123456 *'
    print(text)
    enc_text = encode(text, 10)
    print(enc_text)
    dec_text = decode(enc_text, 10)
    print(dec_text)


if __name__ == "__main__":
    main()
