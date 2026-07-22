# -*- coding: utf-8 -*-
"""
TRÊS DOBRAS — conteúdo do jogo.
Cada carta de linguagem traz 3 níveis: o casal escolhe a altura da barra.
  Nível 1 CONHECER  · leve, para quebrar o gelo
  Nível 2 APROXIMAR · pessoal, exige abertura
  Nível 3 APROFUNDAR· vulnerabilidade real, para quem já tem intimidade
"""

NIVEIS = [("1", "CONHECER"), ("2", "APROXIMAR"), ("3", "APROFUNDAR")]

# ---------------------------------------------------------------- PALAVRA ----
PALAVRA = [
 ("Diga três qualidades dele(a) começando cada frase com “Eu admiro em você…”.",
  "Conte uma palavra que ele(a) te disse e que você guarda até hoje.",
  "Diga a palavra que você mais precisa ouvir do seu cônjuge — e peça que ele(a) diga agora."),
 ("Complete: “Eu tenho orgulho de você quando…”.",
  "Diga algo que você pensa sobre ele(a) e nunca teve coragem de falar em voz alta.",
  "Peça perdão por uma frase sua que ainda machuca. Sem usar a palavra “mas”."),
 ("Conte o que ele(a) fez esta semana que te fez rir.",
  "Descreva seu cônjuge para um estranho, em três frases, na frente dele(a).",
  "Conte uma crítica que você recebeu dele(a) e que te tornou uma pessoa melhor."),
 ("Fale de um talento dele(a) que você queria que o mundo conhecesse.",
  "Diga em que área da vida você depende dele(a) mais do que costuma admitir.",
  "Ore em voz alta abençoando seu cônjuge pelo nome. Uma frase já basta."),
 ("Complete: “A melhor decisão que tomamos juntos foi…”.",
  "Diga o que você falaria ao seu cônjuge se soubesse que hoje é o último dia.",
  "Confesse uma palavra dura que você guardou no peito — e escolha soltá-la em perdão."),
 ("Diga uma coisa simples que ele(a) faz e que te faz sentir amado(a).",
  "Conte como você fala do seu cônjuge quando ele(a) não está presente.",
  "Diga em que você tem sido duro(a) demais nas palavras e o que muda a partir de hoje."),
 ("Elogie a família dele(a) em algo que seja verdadeiro.",
  "Diga o que mudou em você desde o casamento — e a parte que ele(a) tem nisso.",
  "Fale de um medo que você tem sobre o futuro de vocês. O outro só escuta, sem responder."),
 ("Complete “Obrigado(a) por…” três vezes seguidas, sem repetir.",
  "Diga o que você mais teme perder no relacionamento de vocês.",
  "Peça em voz alta algo concreto que você precisa e nunca pediu com medo de incomodar."),
]

# ------------------------------------------------------------------ TEMPO ----
TEMPO = [
 ("Contem juntos: quantas horas por semana vocês ficam a sós, sem telas?",
  "Marquem agora, no celular, um encontro só dos dois nos próximos 15 dias.",
  "Digam um ao outro em que momento se sentiram mais sozinhos DENTRO do casamento."),
 ("Descreva o encontro perfeito de vocês dois, do começo ao fim.",
  "Contem qual foi o melhor passeio que já fizeram juntos e por quê.",
  "Fale de uma fase em que você esteve presente de corpo e ausente de coração."),
 ("Lembrem do primeiro encontro. Cada um conta a sua versão da história.",
  "O que mais roubou tempo de vocês no último ano? Digam sem culpar ninguém.",
  "Combinem um “horário sagrado” semanal e decidam o que será sacrificado por ele."),
 ("Digam três coisas que gostariam de fazer juntos e nunca fizeram.",
  "Contem qual foi o dia mais feliz da história de vocês.",
  "Falem de um ano difícil do casamento e do que os manteve juntos nele."),
 ("Se ganhassem um dia inteiro livre amanhã, o que fariam juntos?",
  "Que ritual de vocês vocês deixaram morrer? Retomem-no ainda esta semana.",
  "Digam o que sentem quando o outro escolhe qualquer outra coisa em vez de estar ali."),
 ("Qual música, série ou lugar é “de vocês dois”?",
  "Conte um momento em que você quis conversar e não encontrou espaço.",
  "Olhem-se em silêncio por 60 segundos. Depois cada um diz o que sentiu."),
 ("Planejem aqui e agora o próximo aniversário de casamento de vocês.",
  "Conte o que você faz quando quer atenção e não sabe como pedir.",
  "Digam como estará o casamento de vocês daqui a dez anos se nada mudar."),
 ("Digam qual é o momento favorito do dia de vocês, juntos.",
  "O que você gostaria de aprender ao lado do seu cônjuge?",
  "Escolham juntos uma coisa para tirar da agenda desta semana — e tirem de verdade."),
]

# --------------------------------------------------------------- PRESENTE ----
PRESENTE = [
 ("Qual o melhor presente que você já recebeu dele(a)?",
  "Diga um presente pequeno que faria o seu dia — algo de menos de R$ 50.",
  "Conte de uma vez em que você se sentiu esquecido(a) numa data importante."),
 ("Descreva o presente que você daria se dinheiro não fosse problema.",
  "Que presente invisível — um favor, um silêncio, uma paciência — ele(a) te deu esta semana?",
  "Digam com sinceridade como o dinheiro tem afetado o casamento de vocês."),
 ("Prometa um bilhete escrito à mão nesta semana. Diga onde vai escondê-lo.",
  "Que presente você guardou até hoje e por que ele significa tanto?",
  "Falem de uma expectativa financeira que um tem sobre o outro e nunca foi dita."),
 ("Que flor, doce ou cheiro faz seu cônjuge pensar em você?",
  "Diga um presente que você deu e que não foi valorizado — sem acusar.",
  "Decidam juntos algo que vocês vão dar a alguém, como casal, ainda neste mês."),
 ("Se pudesse embrulhar um sentimento, qual daria a ele(a) hoje?",
  "Conte um presente da sua infância que te marcou e por quê.",
  "Falem de um sonho que exige sacrifício financeiro — e do primeiro passo real."),
 ("Qual foi a compra mais divertida que vocês fizeram juntos?",
  "O que você comprou para si mesmo(a) e sentiu culpa? Conte.",
  "Perdoem, um ao outro, uma decisão financeira do passado. Em voz alta."),
 ("Combinem uma “surpresa de dez minutos” para esta semana.",
  "Diga o que você gostaria de receber e nunca pediu por achar bobagem.",
  "Digam o que vocês têm dado a todo mundo, menos um ao outro."),
 ("Que presente vocês dariam a Deus como casal neste ano?",
  "Que gesto do outro vale mais do que qualquer presente comprado?",
  "Escrevam uma meta financeira e uma meta de generosidade para os próximos 12 meses."),
]

# ---------------------------------------------------------------- SERVIÇO ----
SERVICO = [
 ("Diga uma tarefa da casa que você faria com prazer por ele(a) esta semana.",
  "Qual tarefa te esgota e você nunca pediu ajuda para fazer?",
  "Assuma uma responsabilidade do outro pelos próximos 30 dias. Diga qual, agora."),
 ("Conte a última vez em que ele(a) te ajudou sem você precisar pedir.",
  "Diga o que faria a sua segunda-feira ficar mais leve.",
  "Peça perdão por algo que você prometeu fazer e nunca fez."),
 ("Massageie os ombros do seu cônjuge por um minuto enquanto ele(a) fala.",
  "Digam em que área da casa vocês mais discutem — e criem uma regra nova.",
  "Lave hoje as mãos ou os pés do seu cônjuge, em silêncio. (João 13.14)"),
 ("Que serviço dele(a) você toma como garantido? Agradeça agora, em voz alta.",
  "Conte de um dia em que você se sentiu sobrecarregado(a) e sozinho(a).",
  "Revejam a divisão das tarefas da casa e mudem UMA delas hoje."),
 ("Diga um cuidado do seu pai ou da sua mãe que você gostaria de ter em casa.",
  "Como você prefere ser cuidado(a) quando está doente?",
  "Fale de uma vez em que você precisou dele(a) e ele(a) não veio."),
 ("Prometa um café na cama, um carro lavado ou algo do tipo. Diga o dia.",
  "Que serviço dele(a) te faz sentir respeitado(a)?",
  "Digam qual dos dois tem carregado mais peso hoje — e reequilibrem a carga."),
 ("O que vocês fazem melhor juntos do que separados?",
  "Onde vocês poderiam servir juntos, na igreja ou na comunidade?",
  "Confesse uma vez em que você serviu a todo mundo, menos ao seu cônjuge."),
 ("Digam três coisas pelas quais vocês são gratos hoje.",
  "Qual hábito seu você sabe que pesa para o outro?",
  "Escolha um hábito para abandonar por amor a ele(a). Diga qual e comece hoje."),
]

# ------------------------------------------------------------------ TOQUE ----
TOQUE = [
 ("Deem as mãos e permaneçam assim até o fim desta rodada.",
  "Diga onde e como você mais gosta de receber carinho.",
  "Abrace seu cônjuge por 20 segundos, em silêncio, sem soltar primeiro."),
 ("Olhe nos olhos dele(a) por 20 segundos, sem dizer nada.",
  "Contem qual foi o abraço mais importante que vocês já se deram.",
  "Diga o que o toque do seu cônjuge desperta em você."),
 ("Diga o que você achou bonito nele(a) hoje.",
  "Elogie o corpo do seu cônjuge de um jeito sincero e respeitoso.",
  "Fale de uma insegurança sua com o próprio corpo. O outro responde com uma bênção."),
 ("Encostem as testas uma na outra e respirem juntos cinco vezes.",
  "Conte de um momento em que um simples toque te acalmou.",
  "Digam como vocês se sentem quando o outro se afasta fisicamente."),
 ("Faça um carinho no rosto do seu cônjuge enquanto conta até dez.",
  "Que gesto físico faz você se sentir seguro(a)?",
  "Conversem, com respeito, sobre a frequência e a qualidade da intimidade de vocês."),
 ("Qual foi o primeiro toque de vocês dois que ficou na memória?",
  "Que gesto em público — mão, braço, ombro — te faz sentir escolhido(a)?",
  "Peça um toque de que você tem sentido falta. Peça com todas as letras."),
 ("Dancem uma música juntos agora, mesmo que não haja música.",
  "Conte o que faz você se sentir desejado(a).",
  "Falem de um pudor ou vergonha que hoje atrapalha a intimidade de vocês."),
 ("Beijem-se na testa e digam “eu escolho você”.",
  "Diga o que mudou no corpo de vocês e do que você se orgulha hoje.",
  "Orem juntos, de mãos dadas, pela intimidade do casamento. Sem pressa."),
]

LINGUAGENS = [("PALAVRA", PALAVRA), ("TEMPO", TEMPO), ("PRESENTE", PRESENTE),
              ("SERVICO", SERVICO), ("TOQUE", TOQUE)]

# ---------------------------------------------------------------- ESPELHO ----
# Regra: você responde POR ELE(A). Acertou, quem avança 2 casas é o CÔNJUGE.
ESPELHO = [
 "Sem perguntar: qual é o maior sonho ainda não realizado do seu cônjuge?",
 "Que medo o seu cônjuge tem e quase nunca diz em voz alta?",
 "Se ele(a) tivesse uma tarde inteira livre e sozinho(a), o que faria?",
 "Qual foi a maior dor da infância do seu cônjuge?",
 "O que ele(a) diria ser a maior qualidade sua? E o maior defeito?",
 "O que o seu cônjuge mais gostaria de mudar na rotina de vocês?",
]

# ------------------------------------------------------------------ ALTAR ----
ALTAR = [
 ("GRATIDÃO",
  "De mãos dadas, cada um agradece a Deus por três coisas do outro. Em voz alta."),
 ("PERDÃO",
  "Digam: “Eu te perdoo por…” e “Eu te peço perdão por…”. Depois, 30 segundos de silêncio."),
 ("BÊNÇÃO",
  "Coloque a mão sobre o ombro do seu cônjuge e abençoe-o(a) pelo nome."),
 ("PACTO",
  "Leiam juntos Eclesiastes 4.9-12 e assinem o Pacto no verso do tabuleiro."),
]

# ----------------------------------------------------- ENVELOPE SELADO -------
# NÃO se abre no evento. É para casais casados, em casa.
SELADO_TITULO = "O JARDIM FECHADO"
SELADO_EPIGRAFE = "“Jardim fechado és tu, minha irmã, minha esposa.” — Cântico 4.12"
SELADO = [
 "Leiam juntos Cântico dos Cânticos 4.9-11, em voz alta, revezando os versos.",
 "Reservem uma noite sem celular, sem televisão e sem pressa. Marquem a data agora.",
 "Descreva o que te atrai no seu cônjuge HOJE — não na juventude dele(a), hoje.",
 "Contem um ao outro o que faz vocês se sentirem desejados. Ouçam sem se defender.",
 "Combinem um gesto discreto que signifique “eu quero você” e que só vocês entendam.",
 "Preparem juntos o quarto: luz baixa, um cheiro bom, e nenhum relógio à vista.",
 "Dez minutos de massagem, revezando. Sem pressa, sem cobrança e sem destino.",
 "Falem, sem vergonha, do que gostariam de viver juntos — e também do que não gostariam.",
 "Orem antes, juntos: agradeçam a Deus pelo corpo um do outro. (1 Coríntios 7.3-5)",
 "Escrevam, cada um, um bilhete para o outro e leiam-nos antes de dormir.",
]

# ------------------------------------------------------- TRILHA DO TABULEIRO -
# 30 casas. Casa 1 = INÍCIO. Sentido horário.
TRILHA = [
 "INICIO", "PALAVRA", "TEMPO", "PRESENTE", "SERVICO", "TOQUE",
 "ESPELHO", "PALAVRA", "TEMPO", "PRESENTE", "SERVICO", "TOQUE",
 "PALAVRA", "ESPELHO", "TEMPO", "PRESENTE", "SERVICO", "TOQUE",
 "PALAVRA", "TEMPO", "ESPELHO", "PRESENTE", "SERVICO", "TOQUE",
 "PALAVRA", "TEMPO", "PRESENTE", "ESPELHO", "SERVICO", "TOQUE",
]

VERSICULO = "“O cordão de três dobras não se rebenta com facilidade.”"
VERSICULO_REF = "ECLESIASTES 4.12"

PACTO = [
 "Nós escolhemos, hoje, ser o cordão que não se rebenta.",
 "Prometo te ouvir antes de responder.",
 "Prometo te procurar antes de me afastar.",
 "Prometo te abençoar antes de te corrigir.",
 "E prometo não deixar Deus de fora da nossa terceira dobra.",
]

REGRAS_RESUMO = [
 ("1", "Um peão só: vocês caminham juntos, sem competir."),
 ("2", "Toda carta tem 3 níveis. Vocês escolhem a altura."),
 ("3", "Cumpriu a carta? Plantem uma semente no canteiro."),
 ("4", "Espelho: acertou, andem 2. Errou, ele(a) conta."),
 ("5", "Fim da volta: o Altar. Quatro cartas, sem pressa."),
 ("6", "Canteiro vazio é linguagem esquecida. Cuidem dela."),
]
