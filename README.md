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

## Preparação de Dados

Treinamos em múltiplos conjuntos de dados: Audioset (nossa seleção), AudioCaps e, finalmente, Clotho. Para simplificar o trabalho com múltiplos conjuntos de dados, baixamos e convertemos em uma estrutura de arquivo o mais compatível possível. Chamamos isso de AudioFolder, pois é inspirado no AudioFolder ou ImageFolder da HuggingFace.

Embora os conjuntos de dados não sejam completamente compatíveis (por exemplo, uma legenda versus múltiplas legendas por clipe de áudio), a estrutura AudioFolder e a classe python audiocap.data.AudioFolder nos ajudam a trabalhar com eles de forma sistemática. As seções seguintes explicam como obter os dados e preparar AudioFolder a partir deles.



### Conjunto de Dados Clotho

<details>
  <summary> Obtendo os Dados </summary>

```
mkdir -p data/clotho_v2.1/audiofolder
```

Baixe os dados de https://zenodo.org/record/4783391 e extraia csv na pasta data/clotho_v2.1 e os áudios na pasta data/clotho_v2.1/audiofolder. Sua estrutura de diretórios deve ser assim:

```
soundscribe/
├── audiocap
│ ...
...
|
├── data
│ └── clotho_v2.1
│ ├── audiofolder
│ │ ├─ desenvolvimento
│ │ ├─ avaliação
│ │ ├─ teste
│ │ └─ validação
│ ├── clotho_captions_desenvolvimento.csv
│ ├── clotho_captions_avaliação.csv
│ ├── clotho_captions_validação.csv
│ ├── clotho_metadata_desenvolvimento.csv
│ ├── clotho_metadata_avaliação.csv
│ ├── clotho_metadata_teste.csv
│ └── clotho_metadata_validação.csv
...
```

</details>


<details>    
    <summary> Criando AudioFolder </summary>

Agora, prepare

```
python3 audiocap/prepare_audiofolder.py prepare-clotho-audiofolder data/clotho_v2.1/
```
Isso irá preparar a pasta no formato facilmente carregável.

Para limitar o tamanho de um conjunto (como validação e avaliação), execute:

```
python audiocap/prepare_audiofolder.py limit-clotho-split data/clotho_v2.1/audiofolder/ validação --limit 200
python audiocap/prepare_audiofolder.py limit-clotho-split data/clotho_v2.1/audiofolder/ avaliação --limit 400
```

Isso selecionará uma subamostra (com uma semente) do tamanho desejado e moverá os exemplos restantes para o conjunto de desenvolvimento.

</details>

### Dados de Pré-treinamento

<details>
  <summary> Obtendo AudioSet </summary>

AudioSet é um grande conjunto de dados de classificação multi-rótulos. Em nosso repositório, usamos informações da ontologia do AudioSet para construir legendas sintéticas baseadas em palavras-chave. Isso torna possível o pré-treinamento de um modelo de legendagem seq2seq (como Whisper) no AudioSet usando um pipeline de treinamento supervisionado de ponta a ponta.

As anotações do AudioSet são copiadas para este repositório, mas os áudios devem ser raspados do YouTube. Você pode usar o script `scripts/download_audioset.sh` que usará todos os núcleos para baixar e converter áudios com base em IDs do YouTube.

Torne o script executável

```
chmod +x ./scripts/download_audioset.sh
```

Baixe os arquivos de áudio

```
SPLIT='train_unbalanced' # execute novamente com 'train_balanced' ou 'eval'

mkdir -p logs/download_audioset

./scripts/download_audioset.sh
"data/audioset_full/csvs/${SPLIT}.csv"
"data/audioset_full/audios/${SPLIT}/" 2>&1
| tee >( sed 's/.*\r//' > "logs/download_audioset/${SPLIT}.txt" )
```
(`sed` está lá para excluir linhas de saída que apenas atualizam o progresso)

Por favor, note que raspar o AudioSet é apenas um esforço melhor. Vídeos podem ser excluídos do YouTube. Agora, você deve selecionar um subconjunto do AudioSet que atenda às suas necessidades. O AudioSet é fortemente desequilibrado, com música e fala ocorrendo na vasta maioria dos exemplos. No nosso caso, selecionamos cerca de 130k instâncias que cobriam o máximo possível das classes sub-representadas. No entanto, antes de selecionar o subconjunto, preparamos o AudioCaps - um conjunto de dados diferente que usamos para pré-treinamento. Isso é para evitar um vazamento entre os dois conjuntos de dados porque eles têm arquivos de áudio em comum.

</details>


<details>
  <summary> Obtendo AudioCaps </summary>

AudioCaps é um conjunto de dados de legendagem com muito mais áudios do que Clotho (mas é possivelmente de menor qualidade).

As anotações do AudioCaps também fazem parte deste repositório. Além disso, AudioCaps é um subconjunto do AudioSet,
então você tem todos os áudios do AudioCaps preparados uma vez que você baixa o AudioSet.
</details>
<details>
  <summary> Criando AudioCaps AudioFolder </summary>

Execute:

  ```
    python audiocap/prepare_audiofolder.py prepare-audiocaps-audiofolder \
    --audiocaps-path data/audiocaps \
    --audioset-path data/audioset_full \
    --audio-format mp3
  ```

 Isso copiará os arquivos do AudioSet e preparará a estrutura e anotações do AudioFolder
com registros descartados sobre áudios que estavam listados nos csvs do AudioCaps
mas os arquivos estavam ausentes (indisponíveis quando você raspou o AudioSet).
</details>
<details>
  <summary> Criando um subconjunto balanceado do AudioSet </summary>

Esta parte é a mais complexa. Queremos ao mesmo tempo

    um subconjunto diverso
    um subconjunto balanceado
    um subconjunto grande
    sem vazamento com o AudioCaps

Isso é difícil e não tem solução ótima. Especialmente balancear um conjunto de dados é complicado quando cada exemplo tem múltiplos rótulos.
Neste repositório, existem algumas utilidades que ajudam a selecioná-lo. Se você quiser selecionar seu próprio subconjunto, pode olhar em notebooks/select_audioset_subset.ipynb

No entanto, o subconjunto que selecionamos também está disponível neste repositório em data/audioset_small.
</details>
<details>
  <summary> Criando AudioSet-small AudioFolder </summary>

Execute:

  ```shell
    python3 audiocap/prepare_audiofolder.py prepare-audioset-small-audiofolder \
    --audioset-small-path data/audioset_small \
    --audioset-full-path data/audioset_full \
    --audio-format mp3
  ```

</details>

Parabéns. Agora você tem todos os três conjuntos de dados preparados para treinamento.


### Verificando Arquivos de Áudio Corrompidos

Durante o treinamento, arquivos de áudio corrompidos (não carregáveis ​​por librosa) são ignorados. No entanto, se você quiser verificar arquivos corrompidos, pode usar o audiocap.data.find_corrupted_audios.

## Treinamento

Treinamos em duas fases. Pré-treinamos em uma mistura de AudioCaps e AudioSet pequeno e depois afinamos em Clotho.

Monitoramos métricas (no wandb) em cada conjunto de dados separadamente e também registramos algumas previsões para que se possa ver as saídas que o modelo gera.

Como podemos pré-treinar usando o mesmo objetivo de áudio-para-texto que usamos no ajuste fino, só precisamos de um único script de treinamento configurável.

### Pré-treinamento

O AudioSet é originalmente um conjunto de dados de classificação. Durante o treinamento, convertemos as etiquetas em tempo real em legendas sintéticas baseadas em palavras-chave.

```
CUDA_VISIBLE_DEVICES="..." python3
audiocap/train_whisper_supervised.py
--checkpoint-dir-root="./checkpoints"
--audioset-dir="./data/audioset_small/audiofolder"
--audiocaps-dir="./data/audiocaps/audiofolder"
--training-config="./configs/pretrain_1on1_large_config.yaml"
--wandb-group="pretraining"
```

O argumento `--training-config` é o mais importante - especifica tudo de importante sobre o treinamento. Experimentamos com diferentes configurações. Você pode encontrar as diferentes configurações dentro da pasta configs/.

### Ajuste Fino

Para executar o ajuste fino, use o seguinte comando:

```
CUDA_VISIBLE_DEVICES="..." python
audiocap/train_whisper_supervised.py
--checkpoint-dir-root="./checkpoints"
--clotho-dir="./data/clotho_v2.1/audiofolder"
--training-config="./configs/finetune_large_config.yaml"
--load-checkpoint="..."
--wandb-group="finetuning"
```
`--load-checkpoint` é um argumento opcional que permite inicializar o modelo com pesos de um arquivo local.


## Contribuição

Contribuições são bem-vindas. Veja CONTRIBUTING.md para mais informações.
