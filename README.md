# Adb Sudoku Solver
##### © 2021 João Vitor Oliveira de Melo. All rights reserved.

## English
The goal of this project is to be able to complete a Sudoku puzzle obtained in an android cellphone ([Link to Google Play][sudoku]) using image recognition and processing techniques.

>This software was made for educational purpose,
>any use to cheat at game is discriminable.

### Installation
In order to use this program you are going to need to install pytesseract (more instructions can be found on their [github repository][pytesseract]).

Another requirement is adb installed, to do that you can check [this page][adb-installation-en]. Also remember to insert adb to your PATH.

You are going to need to install some external libraries that can be easily be done with pip (using __pip install -r requirements.txt__).

### Usage
1. Connect the device using a cable to the computer
2. Run the program, if all goes right, it will show a message including the device serial
3. Start a new game at any difficulty  (**currently the algorithm works MUCH better with the white theme**)
4. Input "s" after the initial message disappeared  and wait
5. If you want to make sure it won't click on any advertisement make sure to disable internet access. (~~Sometimes it can even install apps if you are lucky enough~~)
6. Also, be ready to press Ctrl+C to stop the clicking if anything goes wrong


## Português
O objetivo é possibilitar a resolução de um sudoku obtido em um celular android ([Link para a Google Play][sudoku]) usando técnicas de reconhecimento e processamento de imagem.

>Esse software foi feito para uso educacional,
>qualquer uso para trapacear no jogo é discriminável,

### Instalação
Para usar esse programa você irá precisar instalar o pytesseract (mais instruções podem ser encontradas no [repositório git][pytesseract] deles).

Outro requisito também é que o adb esteja instalado, para fazer isso você pode visitar [essa página][adb-installation-pt]. Também lembre-se de inserir o adb no PATH.

Você também vai precisar instalar algumas bibliotecas externas, que poderão ser facilmente instaladas com o pip (using __pip install -r requirements.txt__).

### Uso
1. Conecte o dispositivo no computador utilizando um cabo
2. Execute o programa, se tudo der certo será exibida uma mensagem informando o número serial do dispositivo
3. Comece um novo jogo em qualquer dificuldade  (**atualmente o algoritmo funciona MUITO melhor com o tema claro**)
4. Insira "s" depois da mensagem inicial desaparecer e espere
5. Se você deseja ter certeza que nenhum anúncio será clicado garanta que o acesso a internet está desabilitado. (~~Algumas vezes ele pode até mesmo instalar aplicativos se você for sortudo o suficiente~~)
6. Esteja pronto para apertar Ctrl+C para parar o clique se algo der errado


   [pytesseract]: <https://github.com/UB-Mannheim/tesseract/wiki>
   [myGit]: <https://github.com/JhonesBR>
   [sudoku]: <https://play.google.com/store/apps/details?id=easy.sudoku.puzzle.solver.free>
   [adb-installation-en]: <https://www.xda-developers.com/install-adb-windows-macos-linux/>
   [adb-installation-pt]: <https://www.showmetech.com.br/aprenda-instalar-usar-adb-do-android-windows/>
