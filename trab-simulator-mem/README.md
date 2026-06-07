# trab-2 — Simulador de Alocação Dinâmica de Memória

Aluno: Wellington de Oliveira dos Santos

Simulador de alocação dinâmica de memória. 

## Algoritmos 

- First Fit — percorre as brechas em ordem de
  endereço e devolve a primeira cujo tamanho comporta o pedido.
- Best Fit — examina todas as brechas e escolhe a
  que produz a menor sobra. Empate: vence a brecha mais à esquerda.
- Worst Fit (Pior-Apto) — examina todas as brechas e escolhe a
  maior que comporta o pedido. Empate: vence a brecha mais à esquerda.

Após cada `LIBERA`, blocos livres adjacentes são fundidos (*coalescing*)
para manter a memória representada de forma compacta.

## Detecção de fragmentação externa

Quando um `ALOC` falha (nenhuma brecha individual comporta o pedido),
o simulador distingue duas causas, conforme a definição literal do
enunciado:

- Fragmentação externa — `soma(brechas) ≥ pedido`, ou seja, há
  espaço total mas não contíguo.
- Falta de memória — nem somando todas as brechas dá no pedido.

Cada falha é contabilizada separadamente no relatório final.

## Requisitos

- Python 3.10+ — o simulador e a regressão usam apenas a biblioteca-padrão.
- Os notebooks (`notebook.ipynb`, `inputs.ipynb`) usam `matplotlib` e `notebook` (mesmas libs do trab-1).

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

Arquivo JSON, usuário garante que está bem-formado (mesma convenção
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
trava a simulação) e contabilizado como `freed_missing` no
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
python3 -c "import test_simulator as t; t.generate_snapshots()"
```

## Notebooks

Análise visual com `matplotlib` (rodar após o Setup acima):

```bash
jupyter notebook notebook.ipynb   # ou inputs.ipynb
```

- `notebook.ipynb` — compara First/Best/Worst Fit em cada workload: layout final
  da memória, gráficos de métricas (utilização, maior brecha, rejeições) e a
  maior brecha por evento no workload de fragmentação.
- `inputs.ipynb` — explora os workloads de entrada: capacidade, mix de eventos,
  demanda total de `ALOC` e distribuição dos tamanhos.

## Estrutura

```
trab-2/
├── README.md
├── .gitignore
├── main.py                       # entry fino: parse → run_simulation → print
├── cli.py                        # argparse (--algorithm opcional, --input, --quiet)
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
└── simulator/
    ├── parser.py                 # leitura do JSON
    ├── memory.py                 # Block + Memory (com coalescing)
    ├── runner.py                 # run (1 evento) + run_simulation (1..N algoritmos)
    ├── evaluation.py             # pick_winners (vencedor por métrica)
    ├── visualization.py          # estado por evento + describe_result
    ├── report.py                 # relatório final + tabela comparativa + snapshot_summary
    └── algorithms/
        ├── instantiate_algorithms.py   # registry: nome → choose
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
