
import pygame
import os
import math

from settings import *
from projectiles import Projectile


class MiniBoss:

    CONFIGS = {
        "drone": {
            "imagem": "mini_drone.png",
            "vida": DRONE_VIDA,
            "velocidade": DRONE_VELOCIDADE,
            "tamanho": (85, 85),
            "intervalo": 1400
        },
        "destroyer": {
            "imagem": "mini_destroyer.png",
            "vida": DESTROYER_VIDA,
            "velocidade": DESTROYER_VELOCIDADE,
            "tamanho": (140, 140),
            "intervalo": 1800
        },
        "hunter": {
            "imagem": "mini_hunter.png",
            "vida": HUNTER_VIDA,
            "velocidade": HUNTER_VELOCIDADE,
            "tamanho": (100, 100),
            "intervalo": 1000
        }
    }

    def __init__(self, tipo, x, y, multiplicador=1.0):

        self.tipo = tipo
        config = self.CONFIGS[tipo]

        caminho = os.path.join(
            "assets", "images", config["imagem"]
        )

        imagem = pygame.image.load(caminho).convert_alpha()

        self.image = pygame.transform.smoothscale(
            imagem, config["tamanho"]
        )

        self.rect = self.image.get_rect(center=(x, y))

        # Atributos escalados conforme a fase
        self.vida_maxima = int(config["vida"] * multiplicador)
        self.vida = self.vida_maxima

        self.velocidade = config["velocidade"] * multiplicador

        self.intervalo = max(
            350,
            int(config["intervalo"] / multiplicador)
        )

        self.ultimo_tiro = pygame.time.get_ticks()
        self.direcao = 1

        self.tempo = 0
        self.entrada = True

        self.base_x = x
        self.projeteis = []

    def movimentar(self, jogador):

        self.tempo += 0.05

        if self.entrada:

            self.rect.y += 2

            if self.rect.top >= 50:
                self.entrada = False

            return

        # DRONE: movimento horizontal
        if self.tipo == "drone":

            self.rect.x += int(self.velocidade * self.direcao)

            if self.rect.right >= LARGURA or self.rect.left <= 0:
                self.direcao *= -1

        # DESTROYER: movimento lateral em ondas
        elif self.tipo == "destroyer":

            deslocamento = math.sin(self.tempo) * 150

            self.rect.centerx = int(
                self.base_x + deslocamento
            )

            self.rect.clamp_ip(
                pygame.Rect(0, 0, LARGURA, ALTURA)
            )

        # HUNTER: persegue o jogador
        elif self.tipo == "hunter":

            if self.rect.centerx < jogador.rect.centerx - 10:
                self.rect.x += int(self.velocidade)

            elif self.rect.centerx > jogador.rect.centerx + 10:
                self.rect.x -= int(self.velocidade)

            self.rect.clamp_ip(
                pygame.Rect(0, 0, LARGURA, ALTURA)
            )

    def atirar(self, jogador):

        agora = pygame.time.get_ticks()

        if agora - self.ultimo_tiro >= self.intervalo:

            self.ultimo_tiro = agora

            if self.tipo == "destroyer":

                # Rajada de três tiros
                for deslocamento in [-35, 0, 35]:

                    self.projeteis.append(
                        Projectile(
                            self.rect.centerx + deslocamento,
                            self.rect.bottom,
                            direcao=1,
                            inimigo=True
                        )
                    )

            else:

                direcao = (
                    pygame.Vector2(jogador.rect.center)
                    - pygame.Vector2(self.rect.center)
                )

                if direcao.length() > 0:
                    direcao = direcao.normalize()

                self.projeteis.append(
                    Projectile(
                        self.rect.centerx,
                        self.rect.bottom,
                        direcao=direcao,
                        inimigo=True
                    )
                )

    def atualizar(self, jogador):

        if self.vida <= 0:
            return

        self.movimentar(jogador)
        self.atirar(jogador)

        for tiro in self.projeteis[:]:

            tiro.atualizar()

            if (
                tiro.rect.top > ALTURA
                or tiro.rect.left > LARGURA
                or tiro.rect.right < 0
                or tiro.rect.bottom < 0
            ):
                self.projeteis.remove(tiro)

    def receber_dano(self, dano):

        self.vida = max(0, self.vida - dano)

    def desenhar(self, tela):

        if self.vida <= 0:
            return

        tela.blit(self.image, self.rect)

        # Barra de vida
        largura = self.rect.width
        x = self.rect.x
        y = self.rect.y - 12

        pygame.draw.rect(
            tela,
            CINZA_ESCURO,
            (x, y, largura, 7)
        )

        pygame.draw.rect(
            tela,
            ROSA_NEON,
            (
                x,
                y,
                int(largura * self.vida / self.vida_maxima),
                7
            )
        )

        for tiro in self.projeteis:
            tiro.desenhar(tela)
