"""Modelo da memória simulada.

A memória é uma lista ordenada de blocos contíguos. Cada bloco tem um
endereço de início, um tamanho e um pid: se pid é None, é uma brecha
(espaço livre); caso contrário, é uma partição ocupada por aquele processo.

Toda operação de alocação/liberação mantém a invariante de que a soma dos
tamanhos dos blocos é igual a `memoria_total` e que blocos livres adjacentes
sempre são fundidos (coalescing).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Bloco:
    inicio: int
    tamanho: int
    pid: str | None  # None ⇒ brecha (livre)

    @property
    def fim(self) -> int:
        # Posição imediatamente após o último byte do bloco (intervalo [inicio, fim)).
        return self.inicio + self.tamanho

    @property
    def livre(self) -> bool:
        return self.pid is None


class Memoria:
    def __init__(self, tamanho_total: int) -> None:
        self.tamanho_total = tamanho_total
        self.blocos: list[Bloco] = [Bloco(inicio=0, tamanho=tamanho_total, pid=None)]
        self.fusoes = 0  # contador de fusões de brechas durante LIBERA

    def brechas(self) -> list[tuple[int, Bloco]]:
        """Lista (índice_global, bloco) para todo bloco livre."""
        return [(i, b) for i, b in enumerate(self.blocos) if b.livre]

    def alocar(self, pid: str, tamanho: int, indice_brecha: int) -> None:
        """Aloca `pid` na brecha de índice `indice_brecha`.

        A brecha precisa ter tamanho ≥ `tamanho`. Se sobrar espaço, a sobra
        vira uma nova brecha logo após a partição alocada.
        """
        brecha = self.blocos[indice_brecha]
        assert brecha.livre, "índice não aponta para uma brecha"
        assert brecha.tamanho >= tamanho, "brecha menor que o pedido"

        ocupado = Bloco(inicio=brecha.inicio, tamanho=tamanho, pid=pid)
        sobra = brecha.tamanho - tamanho

        if sobra == 0:
            self.blocos[indice_brecha] = ocupado
        else:
            nova_brecha = Bloco(inicio=brecha.inicio + tamanho, tamanho=sobra, pid=None)
            self.blocos[indice_brecha:indice_brecha + 1] = [ocupado, nova_brecha]

    def liberar(self, pid: str) -> bool:
        """Libera o bloco do processo `pid` e funde com vizinhos livres.

        Retorna True se algum bloco foi liberado, False se não havia processo
        com esse pid (caso documentado no README — apenas avisa, não trava).
        """
        idx = next((i for i, b in enumerate(self.blocos) if b.pid == pid), None)
        if idx is None:
            return False

        self.blocos[idx].pid = None
        self._fundir_em_volta(idx)
        return True

    def _fundir_em_volta(self, idx: int) -> None:
        # Funde com o vizinho à direita primeiro (não altera idx).
        if idx + 1 < len(self.blocos) and self.blocos[idx + 1].livre:
            direito = self.blocos.pop(idx + 1)
            self.blocos[idx].tamanho += direito.tamanho
            self.fusoes += 1

        # Funde com o vizinho à esquerda.
        if idx - 1 >= 0 and self.blocos[idx - 1].livre:
            esquerdo = self.blocos[idx - 1]
            esquerdo.tamanho += self.blocos[idx].tamanho
            self.blocos.pop(idx)
            self.fusoes += 1

    def ocupacao(self) -> int:
        """Soma dos tamanhos dos blocos ocupados."""
        return sum(b.tamanho for b in self.blocos if not b.livre)

    def maior_brecha(self) -> int:
        livres = [b.tamanho for b in self.blocos if b.livre]
        return max(livres) if livres else 0

    def soma_brechas(self) -> int:
        return sum(b.tamanho for b in self.blocos if b.livre)
