# so-2026-01-ufms

Trabalhos e laboratórios da disciplina de Sistemas Operacionais (UFMS, 2026/1).

Aluno: Wellington de Oliveira dos Santos

## Conteúdo

| pasta | o que é | stack |
|-------|---------|-------|
| [`trab-1/`](trab-1/) | Simulador event-driven de escalonamento de CPU: FCFS, SJF (preemptivo e não), Prioridade e Round Robin. Métricas + Gantt + notebooks. | Python 3.10+, matplotlib |
| [`trab-2-simulator-mem/`](trab-2-simulator-mem/) | Simulador de alocação dinâmica de memória: First Fit, Best Fit e Worst Fit, com coalescing e detecção de fragmentação externa. | Python 3.11+, matplotlib |
| [`lab-modulo-kernel/`](lab-modulo-kernel/) | Módulo de kernel Linux com lista encadeada de aniversários. | C, Linux headers |

Cada pasta tem o próprio README com setup, comandos e formato de entrada.

## Início rápido

```bash
# trab-1 — comparar todos os escalonadores
cd trab-1 && python3 main.py

# trab-2 — comparar os três algoritmos de alocação
cd trab-2-simulator-mem && python3 main.py --input inputs/workload.json

# lab-modulo-kernel (Linux)
cd lab-modulo-kernel && make && sudo insmod simple.ko && dmesg | tail -10
```

Os dois simuladores têm regressão por snapshot: `python3 test_simulator.py` dentro da pasta.

## Notas

- Foram utilizadas ferramentas de IA (Claude Code e Cursor) para auxiliar parte da implementação e da documentação.
