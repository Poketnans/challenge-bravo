from typing import Callable, Iterable


def gen_unique(initials: Iterable, genfunc: Callable):
    """
    Valida a unicidade de um recurso gerado pela `genfunc` a partir da lista\n
    de valores `initials`. Caso o recurso esteja na lista, a função geradora\n
    é novamente executada.
    """
    generated = ""
    while True:
        generated = genfunc()
        if generated not in initials:
            break
    return generated
