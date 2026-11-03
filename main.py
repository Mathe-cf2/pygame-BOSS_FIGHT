
import pygame
import sys
import os
import random

from settings import *
from player import Player
from boss import Boss
from projectiles import ProjectileManager
from powerups import PowerUp, PowerUpManager
from difficulty import Difficulty


# =====================================
# INICIALIZAÇÃO
# =====================================

pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(TITULO)

relogio = pygame.time.Clock()

fonte_titulo = pygame.font.SysFont("Arial", 42, bold=True)
fonte_hud = pygame.font.SysFont("Arial", 20, bold=True)
fonte_final = pygame.font.SysFont("Arial", 55, bold=True)
fonte_botao = pygame.font.SysFont("Arial", 25, bold=True)


# =====================================
# BACKGROUND
# =====================================

caminho_background = os.path.join(
    "assets", "images", "background.png"
)

imagem_background = pygame.image.load(
    caminho_background
).convert()

background = pygame.transform.smoothscale(
    imagem_background,
    (LARGURA, ALTURA)
)


# =====================================
# AVISOS ANIMADOS
# =====================================

aviso_texto = ""
aviso_inicio = 0

DURACAO_AVISO = 3200
TEMPO_FADE = 700


def mostrar_aviso(texto):

    global aviso_texto, aviso_inicio

    aviso_texto = texto
    aviso_inicio = pygame.time.get_ticks()


def desenhar_aviso():

    if not aviso_texto:
        return

    agora = pygame.time.get_ticks()
    passado = agora - aviso_inicio

    if passado >= DURACAO_AVISO:
        return

    if passado < TEMPO_FADE:

        alpha = int(255 * passado / TEMPO_FADE)

    elif passado > DURACAO_AVISO - TEMPO_FADE:

        alpha = int(
            255 * (DURACAO_AVISO - passado) / TEMPO_FADE
        )

    else:

        alpha = 255

    alpha = max(0, min(255, alpha))

    sombra = fonte_titulo.render(
        aviso_texto,
        True,
        ROXO_NEON
    )

    texto = fonte_titulo.render(
        aviso_texto,
        True,
        BRANCO
    )

    sombra.set_alpha(alpha)
    texto.set_alpha(alpha)

    posicao = texto.get_rect(
        center=(LARGURA // 2, ALTURA // 2 - 40)
    )

    tela.blit(sombra, posicao.move(3, 3))
    tela.blit(texto, posicao)


# =====================================
# CRIAR / REINICIAR JOGO
# =====================================

def reiniciar_jogo():

    global jogador
    global boss
    global boss_ativo
    global tiros_jogador
    global powerups
    global dificuldade
    global pontuacao
    global estado
    global ultimo_dano_jogador

    jogador = Player()

    boss = None
    boss_ativo = False

    tiros_jogador = ProjectileManager()

    powerups = PowerUpManager()

    dificuldade = Difficulty()

    pontuacao = 0

    estado = "jogando"

    ultimo_dano_jogador = 0

    mostrar_aviso(TITULO)


# =====================================
# OBJETOS INICIAIS
# =====================================

ultimo_dano_jogador = 0

INTERVALO_DANO_JOGADOR = 700

reiniciar_jogo()


# =====================================
# CONTROLE DE DANO
# =====================================

def causar_dano_jogador(dano):

    global ultimo_dano_jogador

    agora = pygame.time.get_ticks()

    if (
        agora - ultimo_dano_jogador
        >= INTERVALO_DANO_JOGADOR
    ):

        jogador.receber_dano(dano)

        ultimo_dano_jogador = agora


# =====================================
# INTERFACE
# =====================================

def desenhar_interface():

    # Fase
    texto_fase = fonte_hud.render(
        f"FASE: {dificuldade.fase}",
        True,
        ROXO_NEON
    )

    tela.blit(texto_fase, (LARGURA // 2 - 50, 15))

    # Vida
    texto_vida = fonte_hud.render(
        f"VIDA: {jogador.vida}/{JOGADOR_VIDA}",
        True,
        VERDE_NEON
    )

    tela.blit(texto_vida, (20, 60))

    pygame.draw.rect(
        tela,
        CINZA_ESCURO,
        (20, 88, 200, 12)
    )

    largura_vida = int(
        200 * max(0, jogador.vida) / JOGADOR_VIDA
    )

    pygame.draw.rect(
        tela,
        VERDE_NEON,
        (20, 88, largura_vida, 12)
    )

    # Pontuação
    texto_pontos = fonte_hud.render(
        f"PONTUAÇÃO: {pontuacao}",
        True,
        BRANCO
    )

    tela.blit(
        texto_pontos,
        (LARGURA - 230, 60)
    )

    # Tempo
    tempo = dificuldade.tempo_sobrevivencia()

    minutos = tempo // 60
    segundos = tempo % 60

    texto_tempo = fonte_hud.render(
        f"TEMPO: {minutos:02}:{segundos:02}",
        True,
        AZUL_NEON
    )

    tela.blit(texto_tempo, (20, 115))

    # Dificuldade
    texto_dificuldade = fonte_hud.render(
        dificuldade.dificuldade_atual(),
        True,
        ROSA_NEON
    )

    tela.blit(
        texto_dificuldade,
        (LARGURA - 230, 90)
    )

    # Progresso dos mini-bosses
    if not boss_ativo:

        progresso = fonte_hud.render(
            f"MINI-BOSSES: {dificuldade.inimigos_derrotados}/{dificuldade.total_inimigos}",
            True,
            AZUL_NEON
        )

        tela.blit(
            progresso,
            (LARGURA // 2 - 100, 45)
        )

    else:

        texto_boss = fonte_hud.render(
            "CHEFAO PRINCIPAL",
            True,
            VERMELHO_NEON
        )

        tela.blit(
            texto_boss,
            (LARGURA // 2 - 100, 45)
        )

    # Poderes
    agora = pygame.time.get_ticks()

    poderes = []

    if jogador.triple_shot > agora:
        poderes.append("TRIPLE SHOT")

    if jogador.rapid_fire > agora:
        poderes.append("RAPID FIRE")

    if jogador.shield > agora:
        poderes.append("ENERGY SHIELD")

    for indice, poder in enumerate(poderes):

        texto = fonte_hud.render(
            poder,
            True,
            AZUL_NEON
        )

        tela.blit(
            texto,
            (20, 145 + indice * 25)
        )


# =====================================
# LOOP PRINCIPAL
# =====================================

rodando = True

while rodando:

    relogio.tick(FPS)

    # =================================
    # EVENTOS
    # =================================

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:

            rodando = False

        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_ESCAPE:

                rodando = False

            # AGORA R REINICIA O JOGO
            if evento.key == pygame.K_r and estado != "jogando":

                reiniciar_jogo()

    # =================================
    # ATUALIZAÇÃO
    # =================================

    if estado == "jogando":

        # JOGADOR
        jogador.movimentar()
        jogador.atualizar_poderes()
        jogador.atirar(tiros_jogador)

        # TIROS DO JOGADOR
        tiros_jogador.atualizar()

        # =================================
        # MINI-BOSSES
        # =================================

        if not boss_ativo:

            dificuldade.atualizar()

            for inimigo in dificuldade.inimigos:

                if inimigo.vida > 0:

                    inimigo.atualizar(jogador)

            # LIBERAR CHEFÃO
            if dificuldade.boss_liberado:

                boss = Boss(
                    dificuldade.multiplicador()
                )

                boss_ativo = True

                mostrar_aviso(
                    f"CHEFAO - FASE {dificuldade.fase}"
                )

        # =================================
        # CHEFÃO
        # =================================

        else:

            boss.atualizar(jogador)

        # =================================
        # POWER-UPS
        # =================================

        powerups.atualizar(jogador)

        # =================================
        # COLISÃO: TIROS DO JOGADOR
        # =================================

        for tiro in tiros_jogador.projeteis[:]:

            acertou = False

            # Acertou o chefão?
            if (
                boss_ativo
                and boss.vida > 0
                and tiro.rect.colliderect(boss.rect)
            ):

                boss.receber_dano(tiro.dano)

                pontuacao += 10

                acertou = True

            else:

                # Acertou mini-boss?
                for inimigo in dificuldade.inimigos:

                    if (
                        not boss_ativo
                        and inimigo.vida > 0
                        and tiro.rect.colliderect(inimigo.rect)
                    ):

                        inimigo.receber_dano(tiro.dano)

                        acertou = True

                        if inimigo.vida <= 0:

                            if inimigo.tipo == "drone":

                                pontuacao += PONTOS_DRONE

                            elif inimigo.tipo == "destroyer":

                                pontuacao += PONTOS_DESTROYER

                            elif inimigo.tipo == "hunter":

                                pontuacao += PONTOS_HUNTER

                            # Drop de power-up
                            if random.random() < 0.35:

                                powerups.powerups.append(
                                    PowerUp(
                                        inimigo.rect.centerx,
                                        inimigo.rect.centery
                                    )
                                )

                        break

            if acertou:

                tiros_jogador.projeteis.remove(tiro)

        # =================================
        # COLISÃO: TIROS INIMIGOS
        # =================================

        tiros_inimigos = []

        if boss_ativo:

            tiros_inimigos.extend(boss.projeteis)

        else:

            for inimigo in dificuldade.inimigos:

                tiros_inimigos.extend(inimigo.projeteis)

        for tiro in tiros_inimigos:

            if tiro.rect.colliderect(jogador.rect):

                causar_dano_jogador(tiro.dano)

                if boss_ativo:

                    if tiro in boss.projeteis:

                        boss.projeteis.remove(tiro)

                else:

                    for inimigo in dificuldade.inimigos:

                        if tiro in inimigo.projeteis:

                            inimigo.projeteis.remove(tiro)

                            break

        # =================================
        # COLISÃO DIRETA
        # =================================

        if not boss_ativo:

            for inimigo in dificuldade.inimigos:

                if (
                    inimigo.vida > 0
                    and jogador.rect.colliderect(inimigo.rect)
                ):

                    causar_dano_jogador(20)

        # =================================
        # DERROTA
        # =================================

        if jogador.vida <= 0:

            estado = "derrota"

        # =================================
        # PRÓXIMA FASE
        # =================================

        elif boss_ativo and boss.vida <= 0:

            pontuacao += PONTOS_BOSS

            boss = None
            boss_ativo = False

            dificuldade.iniciar_proxima_fase()

            mostrar_aviso(
                f"FASE {dificuldade.fase}"
            )

    # =====================================
    # DESENHAR CENÁRIO
    # =====================================

    tela.blit(background, (0, 0))

    # Chefão
    if boss_ativo and boss is not None:

        boss.desenhar(tela)

    # Mini-bosses
    if not boss_ativo:

        for inimigo in dificuldade.inimigos:

            inimigo.desenhar(tela)

    # Power-ups
    powerups.desenhar(tela)

    # Tiros do jogador
    tiros_jogador.desenhar(tela)

    # Jogador
    jogador.desenhar(tela)

    # Interface
    desenhar_interface()

    # Aviso animado
    desenhar_aviso()

    # =====================================
    # TELA DE DERROTA
    # =====================================

    if estado == "derrota":

        # Fundo escurecido
        escuro = pygame.Surface(
            (LARGURA, ALTURA),
            pygame.SRCALPHA
        )

        escuro.fill((0, 0, 0, 180))

        tela.blit(escuro, (0, 0))

        mensagem = fonte_final.render(
            "GAME OVER",
            True,
            VERMELHO_NEON
        )

        tela.blit(
            mensagem,
            mensagem.get_rect(
                center=(LARGURA // 2, ALTURA // 2 - 70)
            )
        )

        texto_pontos = fonte_hud.render(
            f"PONTUAÇÃO FINAL: {pontuacao}",
            True,
            BRANCO
        )

        tela.blit(
            texto_pontos,
            texto_pontos.get_rect(
                center=(LARGURA // 2, ALTURA // 2)
            )
        )

        texto_reiniciar = fonte_botao.render(
            "PRESSIONE R PARA JOGAR NOVAMENTE",
            True,
            VERDE_NEON
        )

        tela.blit(
            texto_reiniciar,
            texto_reiniciar.get_rect(
                center=(LARGURA // 2, ALTURA // 2 + 65)
            )
        )

        texto_sair = fonte_hud.render(
            "ESC - SAIR",
            True,
            BRANCO
        )

        tela.blit(
            texto_sair,
            texto_sair.get_rect(
                center=(LARGURA // 2, ALTURA // 2 + 110)
            )
        )

    pygame.display.flip()


# =====================================
# ENCERRAMENTO
# =====================================

pygame.quit()
sys.exit()
