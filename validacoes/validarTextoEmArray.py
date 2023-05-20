def validarTextoEmArray(texto, array):
    for elemento in array:
        if elemento.upper() in texto.upper():
            return True
    return False