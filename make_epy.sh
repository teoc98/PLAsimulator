#!/bin/sh

declare -a ops
ops=(--html --pdf)

for i in ${ops[*]}
do
  epydoc $i -o doc/refdoc --url ../.. --name "Programmable Logic Array Simulator - Alice Plebe, Matteo Cavallaro" ./pla.py ./circuits.py ./component.py
done
