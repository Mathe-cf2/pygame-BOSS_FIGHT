
import pygame
import os

from settings import *
from projectiles import ProjectileManager


class Player:

    def __init__(self):

        caminho = os.path.join(
            "assets", "images", "player.png"
        )

        imagem = pygame.image.load(caminho).convert_alpha()

        self.image = pygame.transform.smoothscale(
            imagem,
            (JOGADOR_LARGURA, JOGADOR_ALTURA)
        )

        self.rect = self.image.get_rect(
            center=(LARGURA // 2, ALTURA - 100)
        )

        self.vida = JOGADOR_VIDA
        self.velocidade = JOGADOR_VELOCIDADE

        self.ultimo_tiro = 0

        self.rapid_fire = 0
        self.triple_shot = 0
        self.shield = 0

    def movimentar(self):

        teclas = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            dx -= 1

        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            dx += 1

        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            dy -= 1

        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            dy += 1

        if dx and dy:
            dx *= 0.7071
            dy *= 0.7071

        self.rect.x += int(dx * self.velocidade)
        self.rect.y += int(dy * self.velocidade)

        self.rect.clamp_ip(
            pygame.Rect(0, 0, LARGURA, ALTURA)
        )

    def atirar(self, tiros):

        teclas = pygame.key.get_pressed()
        agora = pygame.time.get_ticks()

        intervalo = 100 if self.rapid_fire > agora else INTERVALO_TIRO

        if teclas[pygame.K_SPACE]:

            if agora - self.ultimo_tiro >= intervalo:

                self.ultimo_tiro = agora

                if self.triple_shot > agora:

                    tiros.adicionar(
                        self.rect.centerx,
                        self.rect.top
                    )

                    tiros.adicionar(
                        self.rect.centerx - 25,
                        self.rect.top + 10
                    )

                    tiros.adicionar(
                        self.rect.centerx + 25,
                        self.rect.top + 10
                    )

                else:

                    tiros.adicionar(
                        self.rect.centerx,
                        self.rect.top
                    )

    def receber_dano(self, dano):

        agora = pygame.time.get_ticks()

        if self.shield > agora:
            return

        self.vida = max(0, self.vida - dano)

    def atualizar_poderes(self):

        agora = pygame.time.get_ticks()

        for atributo in ["rapid_fire", "triple_shot", "shield"]:

            if getattr(self, atributo) < agora:
                setattr(self, atributo, 0)

    def desenhar(self, tela):

        tela.blit(self.image, self.rect)

        if self.shield > pygame.time.get_ticks():

            pygame.draw.circle(
                tela,
                AZUL_NEON,
                self.rect.center,
                65,
                3
            )
