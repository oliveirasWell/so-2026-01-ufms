# trab-1 — Simulador de Escalonamento

Simulador event-driven de algoritmos de escalonamento de CPU: FCFS, SJF (preemptivo e não-preemptivo), Priority e Round Robin.

## Requisitos

- Python 3.10+ (stdlib apenas para o simulador)
- `matplotlib` + `notebook` opcionais, só para o `notebook.ipynb`

### Setup do venv (necessário p/ notebook em macOS com Python do Homebrew)

```bash
cd trab-1
python3 -m venv .venv
source .venv/bin/activate
pip install notebook matplotlib
```

Depois de criado, basta `source .venv/bin/activate` em sessões futuras.

## Como rodar

A partir da pasta `trab-1/`:

```bash
# comparação de todos os algoritmos no workload default (inputs/workload.txt)
python main.py

# um algoritmo específico
python main.py --algo fcfs
python main.py --algo sjf
python main.py --algo sjf-preemptive
python main.py --algo priority
python main.py --algo round-robin

# adicionar trace evento-a-evento
python main.py --algo round-robin --trace

# usar outro arquivo de workload
python main.py --input inputs/workload-io-heavy.txt
python main.py --algo round-robin --input inputs/workload-cs-cost.txt

# rodar o teste de aceitação (spec seção 11)
python validate.py
```

## Formato do workload

Arquivo texto UTF-8. Linhas começando com `#` (ou tudo após `#` inline) são ignoradas.

Headers (case-insensitive):

- `quantum=<int>` — obrigatório se for executar Round Robin.
- `cs_cost=<int>` — opcional, default `0`. Custo de troca de contexto.

Linha de processo:

```
pid arrival priority cpu1 [io1 cpu2 [io2 cpu3 ...]]
```

- `bursts` deve ter tamanho **ímpar** (CPU IO CPU IO ... CPU), todos > 0.
- Menor `priority` = mais prioritário.

Exemplo:

```
quantum=2
P1 0 2 5 3 3
P2 1 1 4
P3 2 3 2 2 4
P4 4 2 1
```

## Workloads disponíveis em `inputs/`

| arquivo | foco |
|---|---|
| `workload.txt` | gabarito da spec (4 processos, mix CPU+I/O) |
| `workload-cpu-bound.txt` | só CPU, sem I/O — destaca diferenças entre FCFS/SJF/RR |
| `workload-io-heavy.txt` | muitos bursts de I/O em paralelo |
| `workload-priority-inversion.txt` | prioridades favorecem job longo, cenário que penaliza Priority |
| `workload-large.txt` | 8 processos, mix variado |
| `workload-cs-cost.txt` | igual ao default + `cs_cost=1` para ver impacto de troca de contexto |
| `workload-tiebreak.txt` | múltiplos processos chegando ao mesmo tempo, força critérios de desempate |

## Notebook

```bash
source .venv/bin/activate   # se ainda não estiver ativo
jupyter notebook notebook.ipynb
```

Cobre: tabela comparativa, Gantt por algoritmo, barras por métrica, e exploração de `cs_cost in {0,1,2}`.

## Estrutura

```
trab-1/
  main.py            # CLI
  validate.py        # teste de aceitação
  notebook.ipynb     # exploração visual
  inputs/            # workloads
  schedulers/        # FCFS, SJF, Priority, Round Robin (Scheduler ABC em base.py)
  shared/            # process, parser, simulator, metrics, comparison, reporter, plots
```
