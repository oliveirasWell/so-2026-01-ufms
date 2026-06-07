# trab-2 — Simulador de Alocação Dinâmica de Memória

Aluno: Wellington de Oliveira dos Santos

Simulador de alocação dinâmica de memória. 

## Algoritmos 

- First Fit — percorre as gaps em ordem de
  endereço e devolve a primeira cujo tamanho comporta o pedido.
- Best Fit — examina todas as gaps e escolhe a
  que produz a menor sobra. Empate: vence a brecha mais à esquerda.
- Worst Fit (Pior-Apto) — examina todas as gaps e escolhe a
  maior que comporta o pedido. Empate: vence a brecha mais à esquerda.

Após cada `FREE`, blocos livres adjacentes são fundidos (*coalescing*)
para manter a memória representada de forma compacta.

## Detecção de fragmentação externa

Quando um `ALOC` falha (nenhuma brecha individual comporta o pedido),
o simulador distingue duas causas, conforme a definição literal do
enunciado:

- Fragmentação externa — `soma(gaps) ≥ pedido`, ou seja, há
  espaço total mas não contíguo.
- Falta de memória — nem somando todas as gaps dá no pedido.

Cada falha é contabilizada separadamente no relatório final.

## Requisitos

- Python 3.11+ — o simulador e a regressão usam apenas a biblioteca-padrão (usamos `enum.StrEnum`, disponível a partir do 3.11).
- Os notebooks (`notebook.ipynb`, `inputs.ipynb`) usam `matplotlib` e `notebook`.

> ⚠️ Observação importante sobre a linguagem. O enunciado deste
> trabalho permite apenas C, C++ ou Java. Esta implementação foi feita
> em Python como decisão consciente do aluno, priorizando legibilidade
> e velocidade de prototipagem. O comportamento exigido pelo enunciado
> (3 algoritmos, leitura de arquivo, visualização por evento, relatório
> final com utilização e processos rejeitados) está integralmente
> coberto.

### Setup

O simulador e a regressão (`test_simulator.py`) usam só a biblioteca-padrão.
Os notebooks precisam de `matplotlib` e `notebook`.

Atalho — `./start.sh` cria o `.venv`, instala as libs e abre o Jupyter:

```bash
./start.sh                 # ou: ./start.sh notebook.ipynb
```

Manual:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install notebook matplotlib   # só para os notebooks
```

Depois de criado, basta `source .venv/bin/activate` em sessões futuras.

## Como rodar

A partir da pasta `trab-2/`:

```bash
# rodar os TRÊS algoritmos e comparar (default — sem --algorithm)
python3 main.py --input inputs/workload.json

# rodar um único algoritmo (mostra o estado após cada evento)
python3 main.py --algorithm first-fit

# escolher outro arquivo de entrada
python3 main.py --algorithm best-fit --input inputs/workload_fragmentacao.json

# suprimir estado por evento (mostra só o relatório)
python3 main.py --algorithm worst-fit --quiet

# regressão por snapshot (3 algoritmos × 2 workloads + invariante de coalescing)
python3 test_simulator.py
```

## Formato do arquivo de entrada

Arquivo JSON, usuário garante que está bem-formado:

```json
{
  "total_memory": 1000,
  "events": [
    {"type": "ALLOC", "pid": "P1", "size": 200},
    {"type": "ALLOC", "pid": "P2", "size": 300},
    {"type": "FREE",  "pid": "P1"}
  ]
}
```

- `total_memory` (int): tamanho total da memória disponível para
  usuários, em bytes (unidade abstrata).
- `events` (lista): cada item tem `type` (`"ALLOC"` ou `"FREE"`) e
  `pid` (string). `size` (int) é obrigatório em `ALLOC` e ignorado
  em `FREE`.

Um `FREE` de um `pid` que não está alocado é tratado como aviso (não
trava a simulação) e contabilizado como `freed_missing` no
relatório.

## Workloads em `inputs/`

| arquivo | descrição |
|---------|-----------|
| `workload_simples.json` | 7 eventos sobre 1000 — exemplo mínimo, sem falhas, sanity check |
| `workload_complexo.json` | 45 eventos sobre 2000 — carga realista; diferencia fortemente os 3 algoritmos |
| `workload_fragmentacao.json` | 28 eventos sobre 1000 — fragmentação externa + falta de memória + FREE de pid inexistente |
| `workload.json` | cenário geral usado como default da CLI (1000, 20 eventos) |

## Regressão (snapshots)

`snapshots/*.json` guarda o resultado esperado de cada algoritmo nos
workloads de exemplo; `test_simulator.py` compara a execução atual com eles.
Para regerar após mudar a semântica:

```bash
python3 -c "import test_simulator as t; t.generate_snapshots()"
```

## Notebooks

Análise visual com `matplotlib` (rodar após o Setup acima):

```bash
jupyter notebook notebook.ipynb   # ou inputs.ipynb
```

- `notebook.ipynb` — relatório comparativo em três experimentos (validação →
  realista → fragmentação). Para cada workload: tabela comparativa, **mapa de
  memória ao longo do tempo** por algoritmo, gráficos de métricas e uma leitura
  dos resultados (com a maior brecha por evento no workload de fragmentação).
- `inputs.ipynb` — explora os workloads de entrada: capacidade, mix de eventos,
  demanda total de `ALOC` e distribuição dos tamanhos.

## Estrutura

Os modelos (dataclasses/enums) ficam em `models/` — um arquivo por modelo,
sem lógica — e a lógica fica em `shared/` e `algorithms/`.

```
trab-2/
├── README.md
├── .gitignore
├── main.py                       # entry fino: parse → run_simulation → print
├── parse_args.py                 # argparse (--algorithm opcional, --input, --quiet)
├── start.sh                      # cria venv + libs e abre o Jupyter
├── test_simulator.py             # regressão por snapshot + coalescing
├── notebook.ipynb                # análise comparativa (matplotlib)
├── inputs.ipynb                  # exploração dos workloads (matplotlib)
├── inputs/
│   ├── workload.json
│   ├── workload_fragmentacao.json
│   └── workload_simples.json
├── snapshots/                    # resultados fixados p/ a regressão
│   ├── workload_simples_stats.json
│   └── workload_fragmentacao_stats.json
├── models/                       # só definições de modelo (um arquivo por modelo)
│   ├── types.py                  # ChooseFunction (alias de tipo)
│   ├── memory/
│   │   ├── block.py              # Block
│   │   └── memory.py             # Memory (gaps, eligible_gaps, allocate, free + coalescing)
│   ├── workload/
│   │   ├── event_type.py         # EventType (StrEnum: ALLOC/FREE)
│   │   ├── event.py              # Event
│   │   └── workload.py           # Workload
│   └── simulation/
│       ├── result_kind.py        # ResultKind (StrEnum)
│       ├── event_result.py       # EventResult
│       ├── statistics.py         # Statistics
│       └── simulation_result.py  # SimulationResult
├── algorithms/
│   ├── instantiate_algorithms.py # registry: chave → choose
│   ├── first_fit.py
│   ├── best_fit.py
│   └── worst_fit.py
└── shared/
    ├── parser.py                 # leitura do JSON (object_hook → models)
    ├── simulator.py              # process (1 evento) + run (1 algoritmo) + timeline (snapshots por evento)
    ├── runner.py                 # run_simulation (1..N algoritmos)
    ├── evaluation.py             # pick_winners (vencedor por métrica)
    ├── visualization.py          # estado por evento + describe_result
    ├── plots.py                  # mapa de memória no tempo + barras + curva da maior brecha
    └── report.py                 # relatório final + tabela comparativa/markdown + snapshot_summary
```

## Saída exemplo

```
Evento #10: ALOC  P7=300  → FALHA: FRAGMENTAÇÃO EXTERNA (soma das gaps comporta, mas nenhuma individualmente)
  Partições ocupadas:
    [    0–  149] P1     tam=150
    [  300–  449] P3     tam=150
    [  600–  749] P5     tam=150
  Gaps:
    [  150–  299] LIVRE  tam=150
    [  450–  599] LIVRE  tam=150
    [  750–  999] LIVRE  tam=250
  Layout: |111111111|.........|333333333|.........|555555555|...............|
```

A barra de layout é proporcional ao tamanho total da memória. Gaps
aparecem como `.`; partições ocupadas usam o último caractere do `pid`
(P1 → `1`, P2 → `2`, etc.).

## Referências e notas

- A definição de "fragmentação externa" usada (espaço total ≥ pedido,
  mas nenhuma brecha individual comporta) segue o enunciado e a
  apresentação clássica de *Operating System Concepts* (Silberschatz,
  Galvin e Gagne).
- Foram utilizadas ferramentas de IA (Claude Code) para auxiliar parte
  da implementação e documentação deste projeto.
