# Introdução

## Othello

### Sobre o jogo

**Othello**, também conhecido como Reversi, é um jogo de tabuleiro estratégico para dois jogadores. O objetivo do jogo é ter mais peças na mesa do que o adversário ao final da partida. O jogo é jogado em um tabuleiro de 8x8, onde os jogadores alternam turnos colocando suas peças. As peças são colocadas de forma a cercar as peças do adversário, o que permite que as peças cercadas sejam viradas para a cor do jogador que fez a jogada. O jogo termina quando nenhum dos jogadores pode fazer uma jogada válida, e o vencedor é aquele com mais peças na mesa.
Othello é um jogo de estratégia que requer planejamento e antecipação das jogadas do adversário, tornando-o um desafio interessante para a implementação de inteligência artificial.

### Modelagem formal do problema

Para traduzir o jogo e as suas regras no código, criamos uma classe chamada _Othello_, que representa o estado do jogo, incluindo o tabuleiro, o jogador atual e as regras para determinar os movimentos válidos, atualizar o estado do jogo e verificar as condições de vitória. A classe _Othello_ inclui métodos para:

- Inicializar o tabuleiro e o jogador atual.
- Verificar os movimentos válidos para o jogador atual.
- Realizar uma jogada, atualizando o tabuleiro e alternando o jogador.
- Verificar se o jogo terminou e determinar o vencedor.

No *Minimax*, cada tabuleiro é representado como um estado do jogo, e as jogadas possíveis são representadas como transições entre esses estados. O algoritmo de busca é usado para explorar a árvore de estados do jogo, avaliando as jogadas possíveis e escolhendo a melhor jogada com base em uma função heurística que avalia o estado do jogo.

# Busca adversarial

Busca adversarial é um modelo/tipo de busca onde existe a competição entre agentes (entidade que interagem com o ambiente a sua volta e contém um objetivo a cumprir), os agentes buscam maximizar seus resultados e diminuir o resultados de seu adversário. Um exemplo de busca adversarial seria jogos de tabuleiro onde o objetivo de um agente se baseia na derrota do outro.

## *Minimax*

É um algoritmo recursivo de tomada de decisões usado por inteligências artificiais em teoria de jogos e jogos de turno com dois jogadores de soma zero (a vitória de um jogador necessariamente implica a derrota do outro). Seu princípio de funcionamento é a análise das possíveis futuras jogadas, criando uma árvore de estados do jogo e a explorando com busca em profundidade, e escolhendo as suas jogadas maximizando a sua vantagem e minimizando perdas, de acordo com a sua função heurística. O algoritmo minimax é amplamente utilizado em jogos como xadrez, damas e jogo da velha, onde os jogadores alternam turnos e o planejamento estratégico de movimentos é crucial para o sucesso..

**Passos feitos na recursão**

1. Encontrar os movimentos possíveis para o jogador atual.
2. Para cada movimento possível, criar um novo estado do jogo e chamar recursivamente a função minimax para o próximo jogador.
3. Avaliar o valor do estado do jogo resultante usando uma função heurística, que atribui um valor numérico ao estado do jogo, indicando a vantagem ou desvantagem para o jogador atual.
4. Retornar o valor máximo (para o jogador maximizador) ou mínimo (para o jogador minimizador) dos valores avaliados para os movimentos possíveis.
5. O jogador maximizador escolhe a jogada que maximiza o valor retornado, enquanto o jogador minimizador escolhe a jogada que minimiza o valor retornado.
6. O processo continua até que um estado terminal seja alcançado (vitória, derrota ou empate), até que o tempo limite acabe ou até que uma profundidade máxima seja atingida, momento em que a função heurística é usada para avaliar o estado do jogo.

**Vantagens e Desvantagens**

- Vantagens:
  - Permite a tomada de decisões estratégicas, considerando as possíveis respostas do oponente.
  - Pode ser otimizado com técnicas como poda alpha-beta para reduzir o número de nós avaliados.
- Desvantagens:
  - Pode ser computacionalmente caro, especialmente em jogos com grandes espaços de busca.
  - A eficácia depende da qualidade da função heurística utilizada para avaliar os estados do jogo.

**Adaptações para Othello**

Para o Othello, o algoritmo foi implementado de forma que as peças **pretas** são tratadas como o jogador **maximizador**, enquanto as peças **brancas** são tratadas como o jogador **minimizador**. Isso significa que o algoritmo busca maximizar a pontuação para as peças pretas, enquanto minimiza a pontuação para as peças brancas.

A classe criada tem os seguintes atributos: *game*, que é uma instância da classe _Othello_ representando o estado atual do jogo; *heuristic*, que é a função heurística usada para avaliar os estados do jogo; *time_limit*, que é o tempo máximo permitido para a tomada de decisão; *use_pruning*, que indica se a poda alpha-beta deve ser usada para otimizar a busca; *nodes_expanded*, que conta o número de nós expandidos durante a busca; e *start_time*, que registra o tempo de início da busca para garantir que o tempo limite seja respeitado.
A função principal da classe é a função _run()_, que executa o algoritmo minimax - também usando a técnica de *iterative deepening* - para encontrar a melhor jogada para o jogador atual, considerando as possíveis jogadas do oponente e usando a função heurística para avaliar os estados do jogo.

### Iterative deepening

#### Definição

**Iterative deepening** é uma técnica de busca que combina a profundidade limitada com a busca em profundidade. Em vez de explorar a árvore de busca até uma profundidade fixa, o algoritmo começa com uma profundidade limitada e aumenta gradualmente essa profundidade até atingir um limite máximo ou encontrar uma solução. Ele é usado para diminuir a quantidade de nós que serão explorados enquanto mantém a qualidade das respostas obtidas.

#### Aplicação no Othello

O conceito de **Iterative deepening** é aplicado na classe *Minimax* através de uma variável que inidica a profundidade máxima da busca atual. Ela é incrementada a cada iteração da busca, permitindo dessa forma que o algoritmo explore as profundidades gradualmente. Nesse caso, isso é ainda mais importante pelo grande número de possíveis jogadas a serem exploradas no jogo, o que pode levar a um tempo e custo computacional muito alto caso não seja limitado na busca.

### Alpha-beta Pruning

#### Definição

O algoritimo **Alpha-beta pruning** (poda alfa-beta) é um extensão do algoritmo *Minimax* com o intuito de diminuir o custo computacional das tomadas de decisão, para isso é utilizados os seguintes valores de controle:

- Alpha(∝):
  - Inicializa com −∞
  - representa o melhor valor que o jogador MAX atingiu (maior pontuação)

- Beta(β)
  - Inicializa com +∞
  - Representa o melhor valor que o MIN atingiu (menor pontuação)

Ao decorrer da busca em profundidade em cada nó é passado os valores de ∝ e β. Os nós que representam as possivéis jogadas de MAX, o valor de ∝ é alterado para a jogada com melhor pontuação. Já os nós que representam as possivéis jogadas de MIN, o valor de β é alterado para a jogada com o menor pontuação.

A principal característica do algoritmo é que ele interrompe a busca de ramos que não podem ter um impacto na decisão final, ou seja, quando o valor de ∝ é maior ou igual a β, o algoritmo pode parar de explorar aquele ramo, pois o jogador MIN não escolheria aquela jogada. Da mesma forma, quando o valor de β é menor ou igual a ∝, o algoritmo pode parar de explorar aquele ramo, pois o jogador MAX não escolheria aquela jogada.

![diagramaAlphaBeta](/documents/images/diagramAlphaBeta.png)
Fonte do diagrama:https://www.geeksforgeeks.org/artificial-intelligence/adversarial-search-algorithms/

#### Aplicação no Othello

Uma variável da classe _Minimax_ indica se o **Alpha-beta pruning** será usado. Caso ele seja usado, ao explorar os possíveis movimentos na função run(), o valor de cada uma é verificado e comparado ao valor de _alpha_ ou _beta_, interrompendo a busca ou atualizando o valor da variável ao depender do resultado obtido.

## Heurísticas

### Heurística dos Cantos

A função heuristicOfCorners(board,player) foca em fazer o jogador dominar os quatro cantos do tabuleiro, a função vai analisar sempre os cantos e os seus espaços adjacentes, o tabuleiro é avaliado das seguintes formas:

- Se o jogador possue o canto, é pontuado
- Se o oponente possue o canto, é penalizado
- Caso o canto for vazio verifica os espaços adjacentes:
  - Se o jogador está nesse espaço, é penalizado (criou-se uma margem para o oponente dominar um canto)
  - Se o oponente está nesse espaço, é pontuado (criou-se uma margem para o jogador dominar um canto)
- Ao final ele vai adicionar a diferença da quantidade de peças do jogador menos a quantidade de peças do oponente, visto que em situações de cantos iguais deve ser escolhido aquela que o jogador esteja na vantagem

### Heurística da Quantidade de Movimentos Possiveis

A função heuristicOfPossibleMoves(board,player) tem como objetivo retornar a diferença entre as jogadas possiveis do jogador e do oponente, de modo que as jogadas que garantem mais opções de movimento para o jogador e menos opções para o oponente são mais valorizadas.

### Heurística da Quantidade de Peças

A função heuristicOfPieceCount(board,player) tem como objetivo retornar a diferença entre as peças do jogador e do oponente, de modo que sempre será melhor ter mais peças.

### Heurística Combinada

A função heuristicOfCombination(board, player) é a junção de todas as outras heurísticas, tendo cada uma um peso agregado baseado em sua respectiva importância.

- A Heurística dos Cantos tem peso de 50%
- A Heurística da Quantidade de Movimentos tem peso de 30%
- A Heurística da Quantidade de Peças tem peso de 20%

# Experimentos computacionais (testes e discussão)

Primeiro avaliamos cada variação das heurísticas, com e sem o uso do **Alpha-beta pruning**, contra si mesma, para analisar a eficiência delas em algumas métricas diferentes. Depois, avaliamos o desempenho de configurações diferentes de heurísticas entre si para analisar os pontos fortes e fracos de cada uma.

## Heurística dos Cantos Com Pruning
Avaliando a Heurística dos Cantos com o uso do **Alpha-beta pruning** contra si mesma, obteve-se os seguintes resultados:

| Métrica                              | Valor     |
|--------------------------------------|-----------|
| Vitórias do Preto (B)                | 50        |
| Vitórias do Branco (W)               | 0         |
| Empates                              | 0         |
| Tempo médio das partidas (s)         | 9.21      |
| Média de nós expandidos (Preto)      | 17621.46  |
| Média de nós expandidos (Branco)     | 24744.90  |
| Tempo máximo do Preto (ms)           | 298601.22 |
| Tempo máximo do Branco (ms)          | 3374.30   |
| Máx. nós expandidos (Preto)          | 27954.00  |
| Máx. nós expandidos (Branco)         | 43132.00  |

É possível observar que é uma heurística com uma expansão de nós relativamente intensa, o que é esperado, visto que ela tem muitos parâmetros de pontuação, o que pode levar a um número maior de nós a serem explorados. Entretanto, o uso do **Alpha-beta pruning** permitiu que o tempo médio das partidas fosse relativamente baixo, mesmo com um número maior de nós expandidos, o que mostra a eficiência da técnica de poda para otimizar a busca.

## Heurística Dos Cantos Sem Pruning
Dessa vez sem o uso do **Alpha-beta pruning**, a Heurística dos Cantos apresentou os seguintes resultados:

| Métrica                              | Valor     |
|--------------------------------------|-----------|
| Vitórias do Preto (B)                | 4         |
| Vitórias do Branco (W)               | 1         |
| Empates                              | 0         |
| Tempo médio das partidas (s)         | 90.37     |
| Média de nós expandidos (Preto)      | 150680.20 |
| Média de nós expandidos (Branco)     | 146706.60 |
| Tempo máximo do Preto (ms)           | 51180.17  |
| Tempo máximo do Branco (ms)          | 52166.18  |
| Máx. nós expandidos (Preto)          | 175311.00 |
| Máx. nós expandidos (Branco)         | 188717.00 |


## Heurística das Possibilidades Com Pruning

Para a Heurística das Possibilidades com o uso do **Alpha-beta pruning**, os resultados foram:

| Métrica                              | Valor    |
|--------------------------------------|----------|
| Vitórias do Preto (B)                | 44       |
| Vitórias do Branco (W)               | 5        |
| Empates                              | 1        |
| Tempo médio das partidas (s)         | 13.14    |
| Média de nós expandidos (Preto)      | 31024.40 |
| Média de nós expandidos (Branco)     | 19979.02 |
| Tempo máximo do Preto (ms)           | 11914.39 |
| Tempo máximo do Branco (ms)          | 8514.37  |
| Máx. nós expandidos (Preto)          | 45783.00 |
| Máx. nós expandidos (Branco)         | 30913.00 |

O ponto mais notável dela é que a média de nós expandidos é maior que a heurística dos cantos, o que é esperado, visto que ela tem o objetivo de garantir mais opções de movimento para o jogador e menos opções para o oponente, o que pode levar a um número maior de nós a serem explorados. Ao mesmo tempo que uma maior quantidade de opções de movimento pode levar a uma maior eficiência na tomada de decisões, o elevado tempo de busca pode não ser algo desejado em jogo. Mas embora o alto custo de busca da heurística, o uso do **Alpha-beta pruning** permitiu que muito fosse economizado e que o tempo médio das partidas fosse relativamente baixo.

### Heurística das Possibilidades Sem Pruning

Os seguintes resutados foram obtidos para a Heurística das Possibilidades sem o uso do **Alpha-beta pruning**:

| Métrica                              | Valor     |
|--------------------------------------|-----------|
| Vitórias do Preto (B)                | 4         |
| Vitórias do Branco (W)               | 1         |
| Empates                              | 0         |
| Tempo médio das partidas (s)         | 90.63     |
| Média de nós expandidos (Preto)      | 174611.40 |
| Média de nós expandidos (Branco)     | 180517.60 |
| Tempo máximo do Preto (ms)           | 50619.83  |
| Tempo máximo do Branco (ms)          | 53108.34  |
| Máx. nós expandidos (Preto)          | 199364.00 |
| Máx. nós expandidos (Branco)         | 213603.00 |

Aqui é evidente que o tempo médio das partidas é muito alto, levando em conta o custo da heurística e a falta do uso do **Alpha-beta pruning**, que faz com que o número de nós expandidos aumente significativamente.

## Heurística Quantidade de Peças com Pruning

A Heurística da Quantidade de Peças dá mais valor aos movimentos que garantem mais capturas. Com o uso do **Alpha-beta pruning**, os resultados foram:

| Métrica                              | Valor    |
|--------------------------------------|----------|
| Vitórias do Preto (B)                | 41       |
| Vitórias do Branco (W)               | 7        |
| Empates                              | 2        |
| Tempo médio das partidas (s)         | 5.21     |
| Média de nós expandidos (Preto)      | 15141.98 |
| Média de nós expandidos (Branco)     | 13147.92 |
| Tempo máximo do Preto (ms)           | 5510.72  |
| Tempo máximo do Branco (ms)          | 4409.22  |
| Máx. nós expandidos (Preto)          | 26361.00 |
| Máx. nós expandidos (Branco)         | 18048.00 |

Essa é uma heurística com um custo de busca relativamente baixo, visto que ela tem o objetivo de garantir mais capturas para o jogador, o que pode levar a um número menor de nós a serem explorados. Infelizmente, esse baixo custo vem com o preço de uma baixa eficiência, com o fato de que ela não leva em consideração outros fatores importantes do jogo, como o controle dos cantos e a quantidade de opções de movimento, o que pode levar a decisões ruins, principalmente se comparada com as outras heurísticas. Somando a simplicidade dessa tática com o uso do **Alpha-beta pruning**, o tempo médio das partidas foi relativamente baixo.

## Heurística Quantidade de Peças sem Pruning

Para o teste dessa heurística sem o uso do **Alpha-beta pruning**, os resultados foram:

| Métrica                              | Valor     |
|--------------------------------------|-----------|
| Vitórias do Preto (B)                | 5         |
| Vitórias do Branco (W)               | 0         |
| Empates                              | 0         |
| Tempo médio das partidas (s)         | 47.59     |
| Média de nós expandidos (Preto)      | 122417.80 |
| Média de nós expandidos (Branco)     | 115855.00 |
| Tempo máximo do Preto (ms)           | 37521.88  |
| Tempo máximo do Branco (ms)          | 33070.23  |
| Máx. nós expandidos (Preto)          | 197455.00 |
| Máx. nós expandidos (Branco)         | 179370.00 |

Aqui fica muito evidente a diferença que o *alpha-beta pruning* faz ao ver a diferença entre o número de nós expandidos e o tempo médio das partidas, que aumentam de forma extrema sem o uso da técnica de poda.

## Heurística Combinadas Com Pruning
Para finalizar as diferentes heurísticas, a Heurística Combinada com o uso do **Alpha-beta pruning** apresentou os seguintes resultados:

| Métrica                              | Valor    |
|--------------------------------------|----------|
| Vitórias do Preto (B)                | 50       |
| Vitórias do Branco (W)               | 0        |
| Empates                              | 0        |
| Tempo médio das partidas (s)         | 10.10    |
| Média de nós expandidos (Preto)      | 37457.06 |
| Média de nós expandidos (Branco)     | 39785.80 |
| Tempo máximo do Preto (ms)           | 8808.26  |
| Tempo máximo do Branco (ms)          | 9095.04  |
| Máx. nós expandidos (Preto)          | 65305.00 |
| Máx. nós expandidos (Branco)         | 71163.00 |

Ela apresenta métricas relativamente boas. Um número um pouco maior de nós expandidos mas um tempo relativamente baixo também. O seu objetivo é balancear o melhor que cada heurística tem a oferecer, mas uma visão mais ampla para diferentes aspectos do jogo. Felizmente, o custo mais alto de busca é aliviado pelo uso do **Alpha-beta pruning**.

## Heurística Combinadas Sem Pruning
Agora sem o uso do **Alpha-beta pruning**, a heurística combinada apresentou os seguintes resultados:

| Métrica                              | Valor     |
|--------------------------------------|-----------|
| Vitórias do Preto (B)                | 5         |
| Vitórias do Branco (W)               | 0         |
| Empates                              | 0         |
| Tempo médio das partidas (s)         | 57.47     |
| Média de nós expandidos (Preto)      | 239066.60 |
| Média de nós expandidos (Branco)     | 192640.60 |
| Tempo máximo do Preto (ms)           | 43796.34  |
| Tempo máximo do Branco (ms)          | 40486.92  |
| Máx. nós expandidos (Preto)          | 329425.00 |
| Máx. nós expandidos (Branco)         | 308115.00 |

É facilmente perceptível que o custo dessa heurística é muito alto sem o uso do **Alpha-beta pruning**, trazendo um tempo médio das partidas muito alto e um número de nós expandidos muito alto, o que mostra a importância da técnica de poda para otimizar a busca, principalmente em heurísticas mais complexas como essa.

## Enfrentamentos entre Heurísticas Com e Sem Pruning

Todos os testes estão ocorrendo com Iterative Deepning = 4

| Heuristica | Vitórias B | Vitórias W | Prunning B | Prunning W | Tempo Médio (s) | Nós B        | Nós W        |
| :-----     | :-----     | :-----     | :-----     | :-----     | :-----          | :-----       | :-----       |
| Cantos     | 5          | 0          | Não        | Sim        | 50.21           | 143460.80    | 22776.80     |
| Cantos     | 5          | 0          | Sim        | Não        | 57.87           | 23136.60     | 144210.80    |
| Combinação | 5          | 0          | Não        | Sim        | 55.15           | 149465.60    | 39309.00     |
| Combinação | 5          | 0          | Sim        | Não        | 62.08           | 41084.80     | 153351.60    |

Os testes evidenciam uma vantagem clara de B sobre W, pois mesmo tendo ou não *pruning*, B se saiu melhor em todos os casos, a única diferença perceptível é que quando B não usa pruning o jogo demora mais para terminar.

## Enfrentamento entre Heurísticas Diferentes

Todos os testes estão ocorrendo com *pruning* e *iterative deepening* = 4

| Heurística B | Heurística W | Vitórias B | Vitórias W | Tempo Médio (s) | Nós B     | Nós W     |
| :-----       | :-----       | :-----     | :-----     | :-----          | :-----    | :-----    |
| Qtde Jogadas | Qtde Peças   | 5          | 0          | 29.50           | 44031.00  | 22231.60  |
| Qtde Jogadas | Combinação   | 5          | 0          | 41.65           | 37685.00  | 37167.80  |
| Qtde Peças   | Combinação   | 5          | 0          | 13.94           | 14317.40  | 16920.60  |

Pode-se observar que o B ainda exerce uma dominância no quesito de resultados, mas é perceptível que, por expandir poucos nós a Heurítica de Quantidade de Peças gera jogos mais rápidos.

## Considerações Sobre os Testes

Os experimentos demonstram que o uso do algoritmo *Minimax* aliado ao *Alpha-Beta Pruning* é fundamental para a viabilidade computacional do jogo, reduzindo drasticamente o número de nós explorados sem comprometer a qualidade das decisões.

Entre as heurísticas analisadas, aquelas que consideram múltiplos fatores estratégicos, como controle de cantos e mobilidade, apresentaram melhor desempenho em relação a heurísticas mais simples, como a contagem de peças, que embora mais eficientes computacionalmente, resultam em decisões menos eficazes.

Além disso, observou-se um viés consistente a favor do jogador preto (B), o que indica que fatores estruturais, como ordem de jogada ou implementação, podem influenciar os resultados.

# Problemas Encontrados

## Manutenção do Jogador Atual

Inicialmente, o jogador seria encontrado a partir do tabuleiro atual, contando as peças e analisando a paridade do total. Entretanto, isso se mostrou falho, tendo em vista que em turnos onde o jogador não tem jogadas válidas, o turno é passado. Assim, o número de peças não aumenta e o jogador muda, quebrando a paridade.
Para resolver isso, foi necessário criar uma variável auxiliar para manter controle do jogador. Testamos algumas opções diferentes, como _current_player_, _b_parity_ e _turn_count_, para manter o jogador atual, a paridade das peças pretas e o número de turnos, respectivamente. No fim, optamos por current_player, pois era a opção mais simples e direta para manter o controle do jogador atual, sem a necessidade de cálculos adicionais ou contagem de turnos.

### Conflitos com o _Minimax_

Imaginamos que esse problema havia sido resolvido apenas com essa implementação, mas ao testar o _Minimax_, percebemos que o jogador atual estava sendo alterado de forma incorreta durante a recursão, o que afetava a lógica do algoritmo. Isso acontecia já que o algoritmo de busca alterava o jogador enquanto percorria a árvore de estados, o que podia acabar afetando o estado real do jogo. Com isso, analisamos algumas formas diferentes de resolver o problema, com duas principais.

Uma delas era salvar o estado do jogador atual antes de cada chamada recursiva, restaurando-o após a chamada. Isso evitava que o jogador atual real fosse alterado duranto a busca, mas fazia o _Minimax_ ser responsável de manter o controle do jogador, associando a lógica do jogo com a lógica do algoritmo de busca, o que não parecia ser uma boa solução.

A outra opção era passar o jogador atual real na primeira chamada recursiva, e a partir disso, o _Minimax_ passaria o jogador de cada busca subsequente por parâmetro, sem alterar o atributo da classe _Othello_. Assim, o jogador atual real não se alteraria durante a busca, e o _Minimax_ apenas alteraria a variável local que o representaria nas buscas.

Por fim, escolhemos essa segunda solução como definitiva, por ser a menos intrusiva, mantendo a lógica do jogo separada da lógica do algoritmo de busca, e evitando a necessidade de salvar e restaurar uma variável externa à classe _Minimax_. Entretanto, vale ressaltar que essa escolha exigiu certas mudanças na estrutura da classe _Othello_, como a criação de novos parâmetros nas funções que precisavam saber o jogador atual para que pudessem ser usadas na busca recursiva. Assim, por esse contraponto não ser objetivamente problemático - sendo apenas uma mudança da estrutra esperada - e ser mais _limpo_ que a outra opção, ainda optamos por essa solução.

# Conclusão
O trabalho apresentou um problema interessante, com a implementação do algoritmo de *Minimax* no jogo *Othello*, com o uso de algumas técnicas diferentes no algoritmo e a análise de sua influência nos resultados obtidos. O jogo é simples e complexo ao mesmo tempo, permitindo várias possibilidades diferentes para serem exploradas na implementação do projeto. A criação da funcionalidade do *Minimax* junto do *iterative deepening* apresentou-se como um desafio lógico muito recompensante, que compreende uma estrutura básica mas também bem completa. Foi possível analisar a diferença que o *alpha-beta pruning* faz no custo de busca e a importância dessas técnicas que buscam trazer uma melhoria na eficiência de algoritmos custosos. 

Além disso, exploramos as diferentes abordagens que podemos ter ao buscar uma forma eficiente de jogar *Othello* com a criação das diferentes funções heurísticas. Os testes pelo terminal permitiram obter uma ideia de como os algoritmos estudados se desenvolveram e ver sua real eficácia em cenários reais.

Por fim, o projeto ajudou a consolidar conceitos importantes, como algoritmos de busca com heurísticas e a criação de agentes, além de permitir o entendimento e a aplicação de técnicas de otimização relevantes, contribuindo para uma melhor compreensão das técnicas que abordam a inteligência artificial.
