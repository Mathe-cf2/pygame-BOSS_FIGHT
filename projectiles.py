
import pygame
from settings import *


class Projectile:

    def __init__(self, x, y, direcao=-1, inimigo=False):

        self.posicao = pygame.Vector2(x, y)
        self.inimigo = inimigo

        # Permite tiros verticais ou em qualquer direção
        if isinstance(direcao, pygame.Vector2):

            if direcao.length() > 0:
                self.direcao = direcao.normalize()
            else:
                self.direcao = pygame.Vector2(0, 1)

        else:
            self.direcao = pygame.Vector2(0, direcao)

        self.velocidade = 5 if inimigo else VELOCIDADE_PROJETIL

        self.dano = MINI_BOSS_DANO if inimigo else DANO_PROJETIL

        self.rect = pygame.Rect(x - 5, y - 12, 10, 24)

    def atualizar(self):

        self.posicao += self.direcao * self.velocidade

        self.rect.center = (
            int(self.posicao.x),
            int(self.posicao.y)
        )

    def desenhar(self, tela):

        cor = ROSA_NEON if self.inimigo else AZUL_NEON

        pygame.draw.ellipse(
            tela,
            cor,
            self.rect.inflate(10, 10)
        )

        pygame.draw.ellipse(
            tela,
            BRANCO,
            self.rect.inflate(-4, -8)
        )


class ProjectileManager:

    def __init__(self):

        self.projeteis = []

    def adicionar(self, x, y, direcao=-1, inimigo=False):

        self.projeteis.append(
            Projectile(x, y, direcao, inimigo)
        )

    def atualizar(self):

        for projetil in self.projeteis[:]:

            projetil.atualizar()

            if (
                projetil.rect.bottom < 0
                or projetil.rect.top > ALTURA
                or projetil.rect.right < 0
                or projetil.rect.left > LARGURA
            ):

                self.projeteis.remove(projetil)

    def desenhar(self, tela):

        for projetil in self.projeteis:
            projetil.desenhar(tela)
