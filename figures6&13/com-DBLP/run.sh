#!/usr/bin/env bash
#SBATCH -J dblp_scaling
#SBATCH -o dblp_scaling.out
#SBATCH -e dblp_scaling.err
#SBATCH -t 01-00:00:00   # 1 day (adjust if needed)
#SBATCH --exclusive
#SBATCH --nodes=4

# Config
INPUT="/scratch/ipopa/repro/imm_hclib/input_files/com-dblp.ungraph-LT.txt"
K=100
E=0.13
OUTPUT_DIR="results"
REPS=5

# Prep
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

CORE_COUNTS=(24 48 96 192 384 576 768)
#CORE_COUNTS=(768)

for CORES in "${CORE_COUNTS[@]}"; do
  # Decide node count and exact nodelist by cores
  if   (( CORES <= 192 )); then
    NODES=1
    NODELIST="parmi1"
  elif (( CORES <= 384 )); then
    NODES=2
    NODELIST="parmi1,parmi2"
  elif (( CORES <= 576 )); then 
    NODES=3
    NODELIST="parmi1,parmi2,parmi3"
  else
    NODES=4
    NODELIST="parmi1,parmi2,parmi3,parmi"
  fi

  # tasks per node (integer with these choices)
  TPERNODE=$(( CORES / NODES ))

  echo ">>> Running with $CORES cores on $NODES node(s) [$NODELIST] (tasks/node=$TPERNODE)"

  for REP in $(seq 1 "$REPS"); do
    echo "  -> Repetition $REP / $REPS"

    # --- Production (1D) ---
    srun -N "$NODES" --nodelist="$NODELIST" \
         -n "$CORES" --ntasks-per-node="$TPERNODE" \
         --exclusive \
         /scratch/ipopa/repro/imm_hclib/src/lt_1D/production \
         -f "$INPUT" -u -w \
         -o "inf_${NODES}n_${CORES}c_1D_r${REP}.txt" \
         -t "time_${NODES}n_${CORES}c_1D_r${REP}.txt" \
	 -e "$E" -c -k "$K" > "log_${NODES}n_${CORES}c_1D_r${REP}.txt" 2>&1

    # --- Production (2D) ---
    srun -N "$NODES" --nodelist="$NODELIST" \
         -n "$CORES" --ntasks-per-node="$TPERNODE" \
         --exclusive \
         /scratch/ipopa/repro/imm_hclib/src/lt_2D/production_2D \
         -f "$INPUT" -u -w \
         -o "inf_${NODES}n_${CORES}c_2D_r${REP}.txt" \
         -t "time_${NODES}n_${CORES}c_2D_r${REP}.txt" \
	 -e "$E" -c -k "$K" > "log_${NODES}n_${CORES}c_2D_r${REP}.txt" 2>&1
  done
done

