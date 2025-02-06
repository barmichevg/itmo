#!/bin/bash

# ДЕМОНСТРАЦИОННЫЙ ПРИМЕР ЗАПОЛНЕНИЯ ДЛЯ RUST
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

. $HOME/.cargo/env

rustc hamming_7_4.rs -o hamming_7_4