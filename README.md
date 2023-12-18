# SoundScribe

## Sobre o Projeto

Este repositório contém os recursos do "SoundScribe: Aplicação de GPTs na Legendagem Inteligente para Surdos - Um Passo Adiante na Acessibilidade Auditiva", um projeto desenvolvido para auxiliar pessoas com deficiência auditiva. O sistema utiliza tecnologia de modelo Transformer Encoder-Decoder para transcrever fala e identificar sons ambientais de forma precisa e em tempo real.

### Funcionalidades
- Transcrição de Fala: Boa identificação de diálogos.
- Detecção de Sons Ambientais: Capacidade de distinguir e descrever sons do ambiente.
- Baixa Latência: Sincronização eficiente das legendas com o conteúdo visual.
- Integração com FFMPEG: Processamento e análise de áudio otimizados.

## Instalação

Para configurar o sistema, siga os passos abaixo:
```
    git clone https://github.com/GabrielHendrix/soundscribe
    cd soundscribe
```
Instale as dependências:

```
    pip3 install -r requirements.txt
```

## Uso

Para iniciar o sistema, garanta a existência de um microfone em sua máquina e execute o módulo de gravação:

```
    python3 audio_rec.py
```

Agora abra um novo terminal também dentro do diretório do projeto e execute o módulo de inferência do sistema:

```
    python3 cc_demo.py
```

Caso você deseje a transcrição das falas ao invés do sons execute o seguinte script:

```
    python3 demo.py
```

## Contribuição

Contribuições são bem-vindas. Veja CONTRIBUTING.md para mais informações.
