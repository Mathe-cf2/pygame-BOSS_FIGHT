
import pygame
import random

from settings import *


class PowerUp:

    TIPOS = [
        "triple",
        "rapid",
        "shield",
        "health"
    ]

    CORES = {
        "triple": AZUL_NEON,
        "rapid": ROSA_NEON,
        "shield": ROXO_NEON,
        "health": VERDE_NEON
    }

    def __init__(self, x, y):

        self.tipo = random.choice(self.TIPOS)

        self.rect = pygame.Rect(x - 18, y - 18, 36, 36)

        self.velocidade = 2
        self.tempo = 0

    def atualizar(self):

        self.rect.y += self.velocidade
        self.tempo += 0.1

    def coletar(self, jogador):

        agora = pygame.time.get_ticks()

        if self.tipo == "triple":
            jogador.triple_shot = agora + DURACAO_POWERUP

        elif self.tipo == "rapid":
            jogador.rapid_fire = agora + DURACAO_POWERUP

        elif self.tipo == "shield":
            jogador.shield = agora + DURACAO_POWERUP

        elif self.tipo == "health":
            jogador.vida = min(
                JOGADOR_VIDA,
                jogador.vida + RECUPERACAO_VIDA
            )

    def desenhar(self, tela):

        cor = self.CORES[self.tipo]

        pygame.draw.circle(
            tela,
            cor,
            self.rect.center,
            19
        )

        pygame.draw.circle(
            tela,
            BRANCO,
            self.rect.center,
            8
        )


class PowerUpManager:

    def __init__(self):

        self.powerups = []
        self.ultimo = pygame.time.get_ticks()

    def atualizar(self, jogador):

        agora = pygame.time.get_ticks()

        if agora - self.ultimo >= INTERVALO_POWERUP:

            self.ultimo = agora

            x = random.randint(40, LARGURA - 40)

            self.powerups.append(
                PowerUp(x, -20)
            )

        for bonus in self.powerups[:]:

            bonus.atualizar()

            if bonus.rect.top > ALTURA:
                self.powerups.remove(bonus)

            elif bonus.rect.colliderect(jogador.rect):

                bonus.coletar(jogador)
                self.powerups.remove(bonus)

    def desenhar(self, tela):

        for bonus in self.powerups:
            bonus.desenhar(tela)
