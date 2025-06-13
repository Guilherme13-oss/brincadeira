import random
import time

# --- Configurações Globais do Jogo ---
VIDA_MAXIMA_SAPO = 100
FOME_MAXIMA_SAPO = 50
FOME_POR_TURNO = 5
VIDA_PERDIDA_POR_FOME_ZERO = 10 # Dano à vida se a fome chegar a zero
EXPERIENCIA_POR_MOSCA = 10
MOSCAS_INICIAIS_NO_MAPA = 5
TAXA_GERACAO_MOSCAS_TURNOS = 3 # A cada X turnos, novas moscas podem aparecer
TAXA_GERACAO_INIMIGOS_TURNOS = 7 # A cada X turnos, um inimigo pode aparecer

# --- Classe Sapo ---
class Sapo:
    def __init__(self):
        self.vida = VIDA_MAXIMA_SAPO
        self.fome = FOME_MAXIMA_SAPO
        self.experiencia = 0
        self.nivel = 1
        self.lingua_alcance = 1 # Representação simplificada do alcance
        self.dano_lingua = 10 # Dano base que o sapo causa
        self.esta_vivo = True

    def comer_mosca(self, quantidade_fome=15, quantidade_xp=EXPERIENCIA_POR_MOSCA):
        """Sapo come uma mosca, restaurando fome e ganhando XP."""
        self.fome = min(self.fome + quantidade_fome, FOME_MAXIMA_SAPO)
        self.experiencia += quantidade_xp
        print(f"Sapo comeu uma mosca! Fome: {self.fome}/{FOME_MAXIMA_SAPO}, XP: {self.experiencia}")
        self._verificar_nivel()

    def atacar(self, inimigo):
        """Sapo ataca um inimigo com sua língua."""
        dano_causado = self.dano_lingua + random.randint(-2, 2) # Pequena variação no dano
        inimigo.tomar_dano(dano_causado)
        print(f"Sapo atacou a {inimigo.nome} com a língua, causando {dano_causado} de dano!")

    def tomar_dano(self, dano):
        """Sapo toma dano."""
        self.vida -= dano
        if self.vida <= 0:
            self.vida = 0
            self.esta_vivo = False
            print("Sapo foi derrotado...")
        print(f"Sapo tomou {dano} de dano. Vida: {self.vida}/{VIDA_MAXIMA_SAPO}")

    def _verificar_nivel(self):
        """Verifica se o sapo subiu de nível e aplica melhorias."""
        xp_para_proximo_nivel = self.nivel * 50
        if self.experiencia >= xp_para_proximo_nivel:
            self.nivel += 1
            print(f"\n🎉 Sapo subiu para o Nível {self.nivel}!")
            self.vida = min(self.vida + 20, VIDA_MAXIMA_SAPO) # Aumenta um pouco a vida
            self.lingua_alcance += 1 # Aumenta alcance da língua
            self.dano_lingua += 5 # Aumenta dano da língua
            print(f"Vida restaurada um pouco. Alcance da língua: {self.lingua_alcance}, Dano da língua: {self.dano_lingua}")

    def passar_turno(self):
        """Efeitos que ocorrem a cada turno (ex: fome diminui)."""
        self.fome -= FOME_POR_TURNO
        if self.fome <= 0:
            print("Sapo está com MUITA fome!")
            self.fome = 0 # Fome não fica negativa
            self.tomar_dano(VIDA_PERDIDA_POR_FOME_ZERO) # Perde vida se estiver com fome

# --- Classe Inimigo ---
class Inimigo:
    def __init__(self, nome, vida, dano, xp_recompensa):
        self.nome = nome
        self.vida = vida
        self.dano = dano
        self.xp_recompensa = xp_recompensa
        self.esta_vivo = True

    def tomar_dano(self, dano):
        """Inimigo toma dano."""
        self.vida -= dano
        if self.vida <= 0:
            self.vida = 0
            self.esta_vivo = False
            print(f"A {self.nome} foi derrotada!")
        else:
            print(f"A {self.nome} tem {self.vida} de vida restante.")

    def atacar(self, alvo):
        """Inimigo ataca o alvo (Sapo)."""
        print(f"A {self.nome} atacou o Sapo, causando {self.dano} de dano!")
        alvo.tomar_dano(self.dano)

# --- Funções do Jogo ---
def exibir_status(sapo, moscas_restantes, inimigos_presentes):
    """Exibe o status atual do sapo e do pântano."""
    print("\n--- Status do Sapo ---")
    print(f"Vida: {sapo.vida}/{VIDA_MAXIMA_SAPO}")
    print(f"Fome: {sapo.fome}/{FOME_MAXIMA_SAPO}")
    print(f"Nível: {sapo.nivel} (XP: {sapo.experiencia})")
    print(f"Moscas no Pântano: {moscas_restantes}")
    if inimigos_presentes:
        print(f"Inimigos à vista: {len(inimigos_presentes)}")
        for i, inimigo in enumerate(inimigos_presentes):
            print(f"  {i+1}. {inimigo.nome} (Vida: {inimigo.vida})")
    else:
        print("Nenhum inimigo à vista. (Por enquanto!)")
    print("--------------------")

def gerar_moscas(quantidade):
    """Gera um número de moscas no pântano."""
    print(f"Novas {quantidade} moscas apareceram no pântano!")
    return quantidade

def gerar_inimigo(nivel_sapo):
    """Gera um novo inimigo (Garça Faminta), escalando com o nível do sapo."""
    # Garça Faminta: vida e dano escalam com o nível do sapo para um desafio crescente
    vida_garca = random.randint(30, 50) + (nivel_sapo - 1) * 10
    dano_garca = random.randint(10, 20) + (nivel_sapo - 1) * 5
    xp_garca = random.randint(20, 30) + (nivel_sapo - 1) * 5
    
    print(f"Uma Garça Faminta apareceu no pântano!")
    return Inimigo("Garça Faminta", vida_garca, dano_garca, xp_garca)

# --- Loop Principal do Jogo ---
def iniciar_jogo():
    print("Bem-vindo ao Sapo Caçador de Moscas!")
    print("Coma moscas para sobreviver e crescer. Cuidado com a fome e os predadores!")
    
    sapo = Sapo()
    moscas_no_mapa = MOSCAS_INICIAIS_NO_MAPA
    inimigos_no_mapa = []
    turno = 0

    while sapo.esta_vivo:
        turno += 1
        print(f"\n--- Turno {turno} ---")
        exibir_status(sapo, moscas_no_mapa, inimigos_no_mapa)
        sapo.passar_turno() # Sapo fica com fome

        # Geração de moscas
        if turno % TAXA_GERACAO_MOSCAS_TURNOS == 0:
            moscas_no_mapa += gerar_moscas(random.randint(1, 3))

        # Geração de inimigos
        if turno % TAXA_GERACAO_INIMIGOS_TURNOS == 0 and random.random() < 0.7: # 70% de chance
            inimigos_no_mapa.append(gerar_inimigo(sapo.nivel))

        # Ações dos inimigos (primeiro os inimigos atacam)
        # Cria uma cópia da lista para iterar, permitindo remoção segura
        for inimigo in list(inimigos_no_mapa): 
            if inimigo.esta_vivo:
                inimigo.atacar(sapo)
                if not sapo.esta_vivo: # Verifica se o sapo morreu após o ataque do inimigo
                    break 
        if not sapo.esta_vivo:
            break

        # Opções do jogador
        print("\nO que Sapo vai fazer?")
        print("1. Procurar e Comer Mosca")
        if inimigos_no_mapa:
            print("2. Lutar contra Inimigo")
            print("3. Tentar Fugir (pode falhar)")
            print("4. Descansar")
            print("5. Sair do Jogo")
        else:
            print("2. Descansar")
            print("3. Sair do Jogo")


        escolha = input("Sua escolha: ").strip()

        if escolha == '1':
            if moscas_no_mapa > 0:
                print("Sapo procura por moscas...")
                sapo.comer_mosca()
                moscas_no_mapa -= 1
            else:
                print("Não há moscas para comer agora!")
        elif escolha == '2' and inimigos_no_mapa: # Lutar
            if not inimigos_no_mapa: # Garante que ainda há inimigos após ataques iniciais
                print("Não há inimigos para lutar neste momento.")
                continue

            print("Qual inimigo Sapo vai atacar?")
            for i, inimigo in enumerate(inimigos_no_mapa):
                print(f"  {i+1}. {inimigo.nome} (Vida: {inimigo.vida})")
            
            try:
                alvo_escolha = int(input("Número do inimigo: ")) - 1
                if 0 <= alvo_escolha < len(inimigos_no_mapa):
                    sapo.atacar(inimigos_no_mapa[alvo_escolha])
                    # Se o inimigo for derrotado, ele é removido e o sapo ganha XP
                    if not inimigos_no_mapa[alvo_escolha].esta_vivo:
                        sapo.experiencia += inimigos_no_mapa[alvo_escolha].xp_recompensa
                        print(f"Sapo ganhou {inimigos_no_mapa[alvo_escolha].xp_recompensa} XP por derrotar a {inimigos_no_mapa[alvo_escolha].nome}!")
                        sapo._verificar_nivel() # Verifica se subiu de nível após ganhar XP
                        inimigos_no_mapa.pop(alvo_escolha)
                else:
                    print("Escolha inválida de inimigo.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
        elif escolha == '3' and inimigos_no_mapa: # Fugir
            print("Sapo tenta fugir...")
            if random.random() < 0.5: # 50% de chance de fugir
                print("Sapo conseguiu escapar dos inimigos por enquanto!")
                inimigos_no_mapa.clear() # Limpa inimigos do mapa para simplificar a fuga
            else:
                print("Sapo não conseguiu fugir e permanece sob ameaça!")
        elif (escolha == '2' and not inimigos_no_mapa) or (escolha == '4' and inimigos_no_mapa): # Descansar
            print("Sapo está descansando... A fome ainda ataca!")
            # Poderia adicionar alguma recuperação de vida aqui para descanso
        elif (escolha == '3' and not inimigos_no_mapa) or (escolha == '5' and inimigos_no_mapa): # Sair do jogo
            print("Sapo decide tirar uma soneca muito longa... Fim de jogo.")
            break
        else:
            print("Comando inválido. Tente novamente.")

        # Pausa para melhor visualização
        time.sleep(1.5)

    print(f"\n--- FIM DE JOGO ---")
    print(f"Sapo sobreviveu por {turno} turnos e atingiu o Nível {sapo.nivel}.")
    print(f"XP total: {sapo.experiencia}")

# Inicia o jogo quando o script é executado
if __name__ == "__main__":
    iniciar_jogo()