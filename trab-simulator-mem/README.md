# trab-2 — Simulador de Alocação Dinâmica de Memória

Aluno: Wellington de Oliveira dos Santos

Simulador textual de alocação dinâmica de memória contígua com partições
variáveis. Lê um arquivo JSON com a memória total e uma sequência de
eventos (alocações e liberações), aplica um dos três algoritmos clássicos
e mostra o estado da memória após cada evento, além de um relatório
final com utilização e contagem de rejeições.

## Algoritmos implementados

- **First Fit (Primeiro-Apto)** — percorre as brechas em ordem de
  endereço e devolve a primeira cujo tamanho comporta o pedido.
- **Best Fit (Melhor-Apto)** — examina todas as brechas e escolhe a
  que produz a **menor sobra**. Empate: vence a brecha mais à esquerda.
- **Worst Fit (Pior-Apto)** — examina todas as brechas e escolhe a
  **maior** que comporta o pedido. Empate: vence a brecha mais à esquerda.

Após cada `LIBERA`, blocos livres adjacentes são fundidos (*coalescing*)
para manter a memória representada de forma compacta.

## Detecção de fragmentação externa

Quando um `ALOC` falha (nenhuma brecha individual comporta o pedido),
o simulador distingue duas causas, conforme a definição literal do
enunciado:

- **Fragmentação externa** — `soma(brechas) ≥ pedido`, ou seja, há
  espaço total mas não contíguo.
- **Falta de memória** — nem somando todas as brechas dá no pedido.

Cada falha é contabilizada separadamente no relatório final.

## Requisitos

- Python 3.10+ (apenas biblioteca-padrão, sem dependências)

> ⚠️ **Observação importante sobre a linguagem.** O enunciado deste
> trabalho permite apenas C, C++ ou Java. Esta implementação foi feita
> em Python como decisão consciente do aluno, priorizando legibilidade
> e velocidade de prototipagem. O comportamento exigido pelo enunciado
> (3 algoritmos, leitura de arquivo, visualização por evento, relatório
> final com utilização e processos rejeitados) está integralmente
> coberto.

### Setup

O projeto usa **apenas a biblioteca-padrão**, então não há nada para
instalar — basta o `python3`. Opcionalmente, isole o ambiente num virtualenv:

```bash
python3 -m venv .venv
source .venv/bin/activate
# nenhuma dependência externa para instalar
```

## Como rodar

A partir da pasta `trab-2/`:

```bash
# rodar os TRÊS algoritmos e comparar (default — sem --algoritmo)
python3 main.py --input inputs/workload.json

# rodar um único algoritmo (mostra o estado após cada evento)
python3 main.py --algoritmo first-fit

# escolher outro arquivo de entrada
python3 main.py --algoritmo best-fit --input inputs/workload_fragmentacao.json

# suprimir estado por evento (mostra só o relatório)
python3 main.py --algoritmo worst-fit --quiet

# regressão por snapshot (3 algoritmos × 2 workloads + invariante de coalescing)
python3 test_simulator.py
```

## Formato do arquivo de entrada

Arquivo **JSON**, usuário garante que está bem-formado (mesma convenção
do trab-1):

```json
{
  "memoria_total": 1000,
  "eventos": [
    {"tipo": "ALOC",   "pid": "P1", "tamanho": 200},
    {"tipo": "ALOC",   "pid": "P2", "tamanho": 300},
    {"tipo": "LIBERA", "pid": "P1"}
  ]
}
```

- `memoria_total` (int): tamanho total da memória disponível para
  usuários, em bytes (unidade abstrata).
- `eventos` (lista): cada item tem `tipo` (`"ALOC"` ou `"LIBERA"`) e
  `pid` (string). `tamanho` (int) é obrigatório em `ALOC` e ignorado
  em `LIBERA`.

`LIBERA` de um `pid` que não está alocado é tratado como aviso (não
trava a simulação) e contabilizado como `liberados_inexistentes` no
relatório.

## Workloads em `inputs/`

| arquivo | descrição |
|---------|-----------|
| `workload.json` | cenário didático geral (1200 bytes, 15 eventos) — diferencia visivelmente os 3 algoritmos |
| `workload_fragmentacao.json` | reproduz fragmentação externa canônica + falta de memória + LIBERA de pid inexistente |
| `workload_simples.json` | exemplo mínimo, sem falhas, útil para sanity check |

## Regressão (snapshots)

`snapshots/*.json` guarda o resultado esperado de cada algoritmo nos
workloads de exemplo; `test_simulator.py` compara a execução atual com eles.
Para regerar após mudar a semântica:

```bash
python3 -c "import test_simulator as t; t.gerar_snapshots()"
```

## Estrutura

```
trab-2/
├── README.md
├── .gitignore
├── main.py                       # entry fino: parse → run_simulation → print
├── cli.py                        # argparse (--algoritmo opcional, --input, --quiet)
├── test_simulator.py             # regressão por snapshot + coalescing
├── inputs/
│   ├── workload.json
│   ├── workload_fragmentacao.json
│   └── workload_simples.json
├── snapshots/                    # resultados fixados p/ a regressão
│   ├── workload_simples_stats.json
│   └── workload_fragmentacao_stats.json
└── simulador/
    ├── parser.py                 # leitura do JSON
    ├── memoria.py                # Bloco + Memoria (com coalescing)
    ├── runner.py                 # executar (1 evento) + run_simulation (1..N algoritmos)
    ├── avaliacao.py              # pick_winners (vencedor por métrica)
    ├── visualizacao.py           # estado por evento + descrever_resultado
    ├── relatorio.py              # relatório final + tabela comparativa + resumo p/ snapshot
    └── algoritmos/
        ├── instantiate_algoritmos.py   # registry: nome → escolher
        ├── first_fit.py
        ├── best_fit.py
        └── worst_fit.py
```

## Saída exemplo

```
Evento #7: ALOC  P5=220  → FALHA: FRAGMENTAÇÃO EXTERNA (soma das brechas comporta, mas nenhuma individualmente)
  Partições ocupadas:
    [  200–  299] P2     tam=100
    [  400–  449] P4     tam=50
  Brechas:
    [    0–  199] LIVRE  tam=200
    [  300–  399] LIVRE  tam=100
    [  450–  599] LIVRE  tam=150
  Layout: |....................|2222222222|..........|44444|...............|
```

A barra de layout é proporcional ao tamanho total da memória. Brechas
aparecem como `.`; partições ocupadas usam o último caractere do `pid`
(P1 → `1`, P2 → `2`, etc.).

## Referências e notas

- A definição de "fragmentação externa" usada (espaço total ≥ pedido,
  mas nenhuma brecha individual comporta) segue o enunciado e a
  apresentação clássica de *Operating System Concepts* (Silberschatz,
  Galvin e Gagne).
- Foram utilizadas ferramentas de IA (Claude Code) para auxiliar parte
  da implementação e documentação deste projeto.
