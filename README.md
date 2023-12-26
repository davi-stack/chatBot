# chatBot
ChatBot para busca em PDFs

Imagem ou GIF relevante:

![Imagem do ChatBot](imagem.png)

Descrição:

Este projeto é um ChatBot para busca em PDFs. Ele é capaz de carregar um PDF, dividi-lo em chuncks e usar embedinds para sempre que o usuário fazer uma busca passar trechos como base para resposta. O ChatBot também tem 3 botões para três possíveis OUTPUTs:

    Um em texto mesmo, usando o pdf como base para resposta da Api do OpenAI.
    Os 3 trechos do PDF mais próximos da pesquisa, com base na distância vetorial de cos.
    Um link da planilha criada, com os resultados da busca.

Tecnologias utilizadas:

    Streamlit: Biblioteca utilizada para criar a interface gráfica do usuário (GUI).
    OpenAI: API utilizada para gerar os embedinds dos trechos do PDF.
    Google Drive: Serviço utilizado para armazenar o PDF e a planilha criada.

Instalação:

Para instalar o projeto, siga estas etapas:

    Clone o repositório do projeto:

git clone https://github.com/davi-stack/chatBot

    Instale as dependências:

pip install -r requirements.txt

Como usar:

Para usar o projeto, siga estas etapas:
Crie uma chave api no site da OpenAI, e set ela no arquivo apikey.py, com "apikey" = 'sua-chave-aqui', ou como variável de ambiente (OPENAI_API_KEY).
Crie uma chave api do googleDrive: https://www.youtube.com/watch?v=l7pL_Y3fw-o&t=2464s , esse vídeo nos 10 primeiros minutos explica,
baixe o JSON e coloque localQueClonou/Chat/ChatBot
rode o projeto localmente no seu nevegador em:
localQueClonou/Chat/ChatBot
rodando no terminal o comando "streamlit run app.py"
resultados:
interface para adição de pdf, escolha de OUTPUT, em trechos, textos e sheets;



Exemplo de saída:

O objetivo do projeto é criar um ChatBot para busca em PDFs, com diferentes tipos de saída. Para facilitar atividades de pesquisa

Contribuições:
Contribuições são bem-vindas! Para contribuir, siga estas etapas:

    Faça um fork do repositório do projeto.
    Faça suas alterações no código.
    Crie um pull request para o repositório original.
Licença:

Este projeto é licenciado sob a licença MIT.

Teste o ChatBot e deixe seu feedback!

Como funciona?
