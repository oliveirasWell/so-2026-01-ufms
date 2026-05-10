# trab-1 — Simulador de Escalonamento

Simulador event-driven de algoritmos de escalonamento de CPU: FCFS, SJF (preemptivo e não-preemptivo), Priority e Round Robin.

## Requisitos

- Python 3.10+
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
# comparação de todos os algoritmos no workload default (inputs/workload.json)
python main.py

# um algoritmo específico
python main.py --algo fcfs
python main.py --algo sjf
python main.py --algo sjf-preemptive
python main.py --algo priority
python main.py --algo round-robin

# adicionar trace evento-a-evento
python main.py --algo round-robin --trace

# usar outro arquivo de workload (JSON)
python main.py --input caminho/para/outro.json

# regressão de métricas (snapshot)
python test_simulator.py
```

## Formato do workload

Arquivo **JSON** UTF-8, lido por `shared.parser.parse_input`.

Objeto raiz:

- `quantum` (opcional, padrão `0`) — quantum do Round Robin.
- `context_switch_cost` (opcional, padrão `0`) — custo de cada troca de contexto.
- `processes` — array de processos.

Cada processo:

- `pid` (string), `arrival` (int ≥ 0), `bursts` (array de int > 0, **tamanho ímpar**: CPU, E/S, …, CPU).
- `priority` (opcional, padrão `1`). Menor valor = mais prioritário no escalonador por prioridade.

Exemplo mínimo:

```json
{
  "quantum": 2,
  "context_switch_cost": 0,
  "processes": [
    { "pid": "P1", "arrival": 0, "priority": 2, "bursts": [5, 3, 3] }
  ]
}
```

## Workloads em `inputs/`

| arquivo | descrição |
|---------|-----------|
| `workload.json` | carga padrão do projeto (vários processos, mix CPU/E/S) |

## Notebook

```bash
source .venv/bin/activate   # se ainda não estiver ativo
jupyter notebook notebook.ipynb
```

Cobre: tabela comparativa, Gantt por algoritmo, barras por métrica, e exploração de `cs_cost in {0,1,2}`.