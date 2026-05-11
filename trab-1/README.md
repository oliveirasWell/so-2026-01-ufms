# trab-1 — Simulador de Escalonamento

Simulador event-driven de algoritmos de escalonamento de CPU: FCFS, SJF preemptivo e não-preemptivo, Prioridade e Round Robin.

- Controle de burts 
- Controle de entrada e saída
- Preempção
- Quantum de utilização
- Tempo gasto em troca de contexto

## Algoritmos implementados

- FCFS (First-Come, First-Served) — não-preemptivo. A fila de prontos é
  atendida pela ordem de chegada: o processo que entrou primeiro
  na fila roda até terminar a rajada de CPU (ou bloquear em E/S).

- SJF (Shortest Job First) — não-preemptivo. A cada decisão de despacho,
  escolhe o processo da fila de prontos com a menor rajada de CPU restante.
  
- SJF preemptivo (SRTF — Shortest Remaining Time First) — Sempre que um novo processo chega (ou volta de E/S) à
  fila de prontos com burst de CPU restante estritamente menor que a do
  processo em execução, o atual é preemptado e o mais curto assume a CPU.

- Prioridade — não-preemptivo, Cada processo carrega um valor inteiro de prioridade;
  o escalonador escolhe sempre o processo de menor valor numérico
  (convenção: `1` é a prioridade mais alta).
  Empates entre prioridades caem no critério de desempate (ver
  abaixo).

- Round Robin — preemptivo por tempo. Processo atual executa por até `quantum` ticks de CPU e, se não
  terminar o burst nesse intervalo, é preemptado e reinserido no fim da
  fila.

### Critério de desempate

Quando duas ou mais decisões empatam (mesma burst restante em SJF, mesma
prioridade, mesmo instante de E/S concluída, etc.), o desempate é feito
pelo `pid` em ordem lexicográfica. Para que isso coincida com a ordem
numérica, todos os workloads em `inputs/` usam `pid`s zero-padded
(`P01`, `P02`, …, `P27`). Workloads novos devem seguir a mesma
convenção (ou usar nomes que ordenem como esperado).

## Requisitos

- Python 3.10+
- `matplotlib`
- `notebook` opcionais para `notebook.ipynb`

### Setup

```bash
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

Arquivo **JSON**, usuário garante que irá utilizar arquivo com padrão correto.


```
{
  "quantum": 0, 
  "context_switch_cost": 0,
  "processes": [
    {"pid": "P01", "arrival": 0, "priority": 1, "bursts": [5, 3, 3]}
  ]
}
```

## Workloads em `inputs/`

| arquivo | descrição |
|---------|-----------|
| `workload.json` | carga padrão do projeto (27 processos, mix CPU/E/S, `quantum=5`, `cs=1`) |
| `workload_simple.json` | carga simples, somente CPU, sem `quantum` e sem `context_switch_cost` |
| `workload_random_01.json` … `workload_random_10.json` | 10 cargas aleatórias usadas pelo notebook para a média do experimento de Round Robin variando o `quantum` |

## Notebooks

- **`notebook.ipynb`** — comparação dos algoritmos: gráficos de Gantt, métricas
  agregadas e o experimento de Round Robin variando o `quantum`.
- **`inputs.ipynb`** — explora os arquivos em `inputs/` antes de rodar
  qualquer algoritmo: tempo médio por processo, σ, mix CPU/E/S e
  comparação entre os 10 workloads aleatórios. Útil para entender como
  a forma do input influencia o resultado.

```bash
source .venv/bin/activate   # se ainda não estiver ativo
jupyter notebook notebook.ipynb   # ou inputs.ipynb
```

