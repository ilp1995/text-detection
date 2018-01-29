O processo de detecção de textos envolve uma série de passos essenciais para a obtenção de um melhor resultado. Esse projeto foi inspirado no trabalho [x] no qual faz uso de um algoritmo que calcula a largura entre bordas paralelas. O algoritmo é Stroke Width Transform (SWT), cujo objetivo é calcular as distâncias entre as bordas paralelas de uma imagem. Pois, segundo [x] as letras possuem um certo padrão entre as distâncias de um ponto a outro, o que torna mais fácil a identificação de uma letra no restante da imagem. Assim, descartando regiões que não estão dentro de um limiar gerado em tempo de execução. A metodologia, segue de acordo com a Figura 1.
Este trabalho utiliza a base de dados MSRA Text Detection 500 Database (MSRA-TD500) [x] contendo mais de 500 imagens de textos com diferentes fontes, diferentes orientações e diferentes idiomas. A Figura 1 mostra a metodologia utilizada neste trabalho, e foi aplicada a um conjunto de imagens selecionadas a partir dessa base descrita anteriormente. Cada etapa desse processo é essencial para o objetivo deste trabalho: detectar textos em imagens.
Para a codificação desses algoritmos foi utilizada a linguagem de programação Python utilizando a biblioteca OpenCV [x], uma das mais utilizadas em projetos de visão computacional. O código-fonte desse projeto está disponível no GitHub (https://github.com/ilp1995/text-detection) para consulta e possíveis contribuições.

Figura 1. Etapas do processo de detecção de texto.
Na Figura 1, é mostrado um esquema de como funciona o processo de detecção de bordas, no qual temos uma imagem como entrada, ou seja, a imagem original que se deseja encontrar o texto. Em seguida, passa para a etapa de pré-processamento que tem o objetivo de melhorar a imagem de entrada para a etapa de detecção de bordas, no qual são aplicados alguns algoritmos de Processamento de Imagens, como Sobel e Canny. Após isso, temos o SWT, que consiste noalgoritmo que realiza alguns cálculos sobre a imagem a fim de obter a largura dos traçados das bordas. Esse resultado será aplicado na etapa posterior, a extração dos componentes conectados da imagem, ou seja, diferencia o que faz parte de um texto e de um objeto qualquer da imagem.
A primeira etapa do processo de detecção de textos é o pré-processamento, que consiste na melhoria da imagem para um melhor resultados nas etapas seguintes. Nesta etapa, a imagem pode (dependendo do parâmetro usado) ter seu histograma equalizado a fim de tornar a imagem com um contraste maior, tornando as bordas mais evidentes e os textos borrados mais nítidos. No fim, a imagem resultante é convertida em tons de cinza, como mostra a Figura 1.
Figura 2. À esquerda a imagem original, à direita a imagem equalizada.
A segunda etapa é a detecção de bordas, o algoritmo utilizado é o Canny, por ser um algoritmo que faz a extração de bordas ótimas de uma imagem. O limiar mínimo e máximo é variável no algoritmo Canny, podendo ser definido para uma imagem específica ao ser analisada, no entanto, o padrão foi definido entre 250 e 400 para obter apenas as bordas mais definidas, no caso as bordas de textos. Na Figura 2, mostra o resultado após a aplicação do algoritmo Canny.
 
Figura 3. Resultado da aplicação do algoritmo Canny.
Nessa mesma etapa, ainda ocorre a extração dos gradientes vertical e horizontal da imagem, mostrando na Figura 3, a fim de obter as direções de todas as bordas, algo fundamental no algoritmo SWT. A terceira etapa, uma etapa mais matemática, consiste na aplicação do algoritmo SWT nas imagens resultantes do algoritmo Canny e Sobel. 
Figura 4. Imagens resultantes após a aplicação do algoritmo Sobel na vertical e horizontal.
Para um maior entendimento de como funciona o cálculo da largura dos traçados basta olhar para a Figura 5. Nela é possível notar linhas de um canto da borda para o outro. Esse traçado corresponde ao tamanho da largura de uma letra. No geral, as letras possuem um padrão, com variações pequenas da largura, por isso o algoritmo SWT é tão importante para a detecção de bordas, já que com o resultado é possível descartar partes da imagem que não possuem o padrão da fonte do texto. Assim, obtendo a imagem resultante do SWT, durante a etapa de extração dos componentes conectados o cálculo será mais prático, tornando a exclusão do que não faz parte do texto simplificada.
Figura 5. À esquerda a imagem original, à direita após aplicação do algoritmo Stroke Width Transform (SWT).
A última etapa consiste em analisar a imagem resultante do algoritmo SWT com o objetivo de verificar as larguras das bordas para descartar o que não é texto. A etapa de extração dos componentes conectados, verifica os resultados comparando com um limiar mínimo e máximo, verificando as larguras que mais aparecem. Se uma determinada largura estiver abaixo ou acima do limiar, então o algoritmo considera aquela parte da imagem como background e é descartado da imagem. Esse passo é executado para todas as bordas. No fim, teremos as áreas que o algoritmo considera como palavra ou texto. Desse modo, podemos aplicar uma máscara na imagem original, criando um retângulo nas posições obtidas no processo de extração dos componentes conectados. A Figura 6 mostra o resultado final. As áreas destacadas em verde claro, são as posições obtidas após a execução do algoritmo.
