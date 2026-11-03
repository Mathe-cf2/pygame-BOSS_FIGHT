
import pygame
import os
import math

from settings import *
from projectiles import Projectile


class Boss:

    def __init__(self, multiplicador=1.0):

        caminho = os.path.join(
            "assets", "images", "boss.png"
        )

        imagem = pygame.image.load(
            caminho
        ).convert_alpha()

        self.image = pygame.transform.smoothscale(
            imagem,
            (BOSS_LARGURA, BOSS_ALTURA)
        )

        self.rect = self.image.get_rect(
            center=(LARGURA // 2, 170)
        )

        # Dificuldade da fase
        self.multiplicador = multiplicador

        self.vida_maxima = int(
            BOSS_VIDA * multiplicador
        )

        self.vida = self.vida_maxima

        # Movimento
        self.direcao = 1
        self.tempo = 0

        # Disparos
        self.ultimo_tiro = pygame.time.get_ticks()
        self.projeteis = []

    # =====================================
    # ATUALIZAÇÃO DO CHEFÃO
    # =====================================

    def atualizar(self, jogador):

        if self.vida <= 0:
            return

        self.tempo += 0.04

        # Porcentagem de vida
        porcentagem = (
            self.vida / self.vida_maxima
        )

        # FASES DE COMBATE DO CHEFÃO
        if porcentagem > 0.6:

            velocidade = BOSS_VELOCIDADE
            intervalo = BOSS_INTERVALO_TIRO

        elif porcentagem > 0.3:

            velocidade = BOSS_VELOCIDADE * 1.5
            intervalo = 850

        else:

            velocidade = BOSS_VELOCIDADE * 2
            intervalo = 550

        # Multiplicador da fase
        velocidade *= self.multiplicador

        intervalo = max(
            250,
            int(intervalo / self.multiplicador)
        )

        # =================================
        # MOVIMENTO HORIZONTAL
        # =================================

        self.rect.x += max(
            1,
            int(velocidade)
        ) * self.direcao

        if self.rect.right >= LARGURA - 20:

            self.direcao = -1

        elif self.rect.left <= 20:

            self.direcao = 1

        # =================================
        # MOVIMENTO VERTICAL
        # =================================

        self.rect.y = 100 + int(
            math.sin(self.tempo) * 35
        )

        # =================================
        # DISPARO DIRECIONADO
        # =================================

        agora = pygame.time.get_ticks()

        if agora - self.ultimo_tiro >= intervalo:

            self.ultimo_tiro = agora

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

        # =================================
        # ATUALIZAR PROJÉTEIS
        # =================================

        for projetil in self.projeteis[:]:

            projetil.atualizar()

            if (
                projetil.rect.bottom < 0
                or projetil.rect.top > ALTURA
                or projetil.rect.right < 0
                or projetil.rect.left > LARGURA
            ):

                self.projeteis.remove(projetil)

    # =====================================
    # RECEBER DANO
    # =====================================

    def receber_dano(self, dano):

        self.vida = max(
            0,
            self.vida - dano
        )

    # =====================================
    # DESENHAR CHEFÃO
    # =====================================

    def desenhar(self, tela):

        # Projéteis
        for projetil in self.projeteis:

            projetil.desenhar(tela)

        if self.vida <= 0:
            return

        # Imagem
        tela.blit(
            self.image,
            self.rect
        )

        # Barra de vida
        largura = 350
        x = LARGURA // 2 - largura // 2
        y = 25

        pygame.draw.rect(
            tela,
            CINZA_ESCURO,
            (x, y, largura, 18),
            border_radius=8
        )

        preenchimento = (
            self.vida / self.vida_maxima
        )

        pygame.draw.rect(
            tela,
            VERMELHO_NEON,
            (
                x,
                y,
                int(largura * preenchimento),
                18
            ),
            border_radius=8
        )
