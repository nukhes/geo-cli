import math


def color_index(m):
    try:
        if m < 0 or m > 1:
            raise ValueError("o índice de cor deve estar entre 0 e 1.")
        if m <= 0.1:
            return "hololeucocrática"
        elif m <= 0.3:
            return "leucocrática"
        elif m <= 0.6:
            return "mesocrática"
        elif m <= 0.9:
            return "hipocrática"
        else:
            return "ultramáfica"

    except Exception as e:
        raise ValueError(f"erro ao calcular o índice de cor: {e}")


def rock_age(parent, daughter, hl):
    for param in [parent, daughter, hl]:
        if param < 0:
            raise ValueError("os parâmetros parent, daughter e hl devem ser positivos.")
    if hl == 0:
        raise ValueError("o tempo de meia-vida (hl) não pode ser zero.")
    
    lam = (math.log(2)) / hl
    age = (1 / lam) * math.log(1 + (daughter / parent))
    return age
