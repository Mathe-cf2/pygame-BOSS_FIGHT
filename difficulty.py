
import pygame
import random

from settings import *
from mini_boss import MiniBoss


class Difficulty:

    def __init__(self):

        self.inicio = pygame.time.get_ticks()

        self.fase = 1
        self.inimigos = []

        self.inimigos_criados = 0
        self.inimigos_derrotados = 0
        self.derrotados_ids = set()

        self.ultimo_spawn = pygame.time.get_ticks()

        self.max_simultaneos = 3

    @property
    def total_inimigos(self):
        return 2 * self.fase + 1

    @property
    def boss_liberado(self):
        return (
            self.inimigos_criados >= self.total_inimigos
            and self.inimigos_derrotados >= self.total_inimigos
        )

    def multiplicador(self):
        return 1 + (self.fase - 1) * 0.25

    def tempo_sobrevivencia(self):

        tempo = pygame.time.get_ticks() - self.inicio

        return tempo // 1000

    def registrar_derrotas(self):

        for inimigo in self.inimigos:

            if inimigo.vida <= 0 and id(inimigo) not in self.derrotados_ids:

                self.derrotados_ids.add(id(inimigo))
                self.inimigos_derrotados += 1

    def atualizar(self):

        self.registrar_derrotas()

        # Todos os mini-bosses foram derrotados
        if self.boss_liberado:
            return

        # Quantos inimigos ainda estão vivos?
        vivos = [
            inimigo
            for inimigo in self.inimigos
            if inimigo.vida > 0
        ]

        agora = pygame.time.get_ticks()

        # Intervalo diminui a cada fase
        intervalo = max(
            500,
            1300 - (self.fase - 1) * 100
        )

        # Cria novos mini-bosses
        if (
            self.inimigos_criados < self.total_inimigos
            and len(vivos) < self.max_simultaneos
            and agora - self.ultimo_spawn >= intervalo
        ):

            self.ultimo_spawn = agora

            if self.fase == 1:
                tipos = ["drone", "hunter"]

            elif self.fase == 2:
                tipos = ["drone", "hunter", "destroyer"]

            else:
                tipos = [
                    "drone",
                    "hunter",
                    "destroyer",
                    "destroyer"
                ]

            tipo = random.choice(tipos)

            x = random.randint(100, LARGURA - 100)

            novo_inimigo = MiniBoss(
                tipo,
                x,
                -100,
                multiplicador=self.multiplicador()
            )

            self.inimigos.append(novo_inimigo)

            self.inimigos_criados += 1

    def iniciar_proxima_fase(self):

        self.fase += 1

        self.inimigos = []

        self.inimigos_criados = 0
        self.inimigos_derrotados = 0
        self.derrotados_ids = set()

        self.ultimo_spawn = pygame.time.get_ticks()

    def dificuldade_atual(self):

        if self.fase == 1:
            return "INICIANTE"

        elif self.fase == 2:
            return "DIFICIL"

        elif self.fase == 3:
            return "EXTREMO"

        else:
            return "APOCALIPSE"
