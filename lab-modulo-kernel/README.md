# lab-modulo-kernel

Módulo de kernel Linux com lista encadeada de aniversários.

## Requisitos

- Ubuntu ARM
- `sudo apt install build-essential linux-headers-$(uname -r)`

## Executar

- `make`
- `sudo insmod simple.ko`
- `dmesg | tail -10` — ver saída
- `sudo rmmod simple` — descarrega
- `dmesg | tail -10` — ver saída após desmontar
