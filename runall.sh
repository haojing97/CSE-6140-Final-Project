#!/bin/bash


# rm -rf output/*

for inst in DATA/*; do
    for seed in {0..9}; do
        for alg in LS1 LS2 Approx; do
            python3 code/tsp_main.py -inst $inst -alg $alg -time 300 -seed $seed
        done
    done
done

for inst in DATA/Champaign.tsp DATA/Berlin.tsp; do
    for seed in {10..49}; do
        for alg in LS1 LS2; do
            python3 code/tsp_main.py -inst $inst -alg $alg -time 300 -seed $seed
        done
    done
done

for inst in DATA/*; do
    python3 code/tsp_main.py -inst $inst -time 600 -alg BnB
done

python3 gen_report.py >report.txt
