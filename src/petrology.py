import math


def color_index(m):
    try:
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
    lam = (math.log(2)) / hl
    age = (1 / lam) * math.log(1 + (daughter / parent))
    return age
