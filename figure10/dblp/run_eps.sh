#!/usr/bin/env bash
#SBATCH -J dblp_epscaling
#SBATCH -o dblp_epscaling.out
#SBATCH -e dblp_epscaling.err
#SBATCH -t 01-00:00:00
#SBATCH --exclusive
#SBATCH --nodes=4

# --- Config ---
rm -rf results
INPUT="/scratch/ipopa/repro/imm_hclib/input_files/com-dblp.ungraph-LT.txt"
OUTPUT_DIR="results"

# Fixed k value
K=100

# Run size
NODES=4
TPERNODE=192
CORES=$(( NODES * TPERNODE ))
NODELIST="parmi1,parmi2,parmi3,parmi"

# --- Prepare output ---
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

# --- Sweep for epsilon ---
EPSILONS=(0.1 0.2 0.3 0.4 0.5)

for E in "${EPSILONS[@]}"; do
    echo ">>> Running with epsilon=$E and k=$K"

    # Single repetition for each epsilon
    REP=1
    echo "  -> Repetition $REP / 1"

    # --- Production (1D) ---
    srun -N "$NODES" --nodelist="$NODELIST" \
        -n "$CORES" --ntasks-per-node="$TPERNODE" \
        --exclusive \
        /scratch/ipopa/repro/imm_hclib/src/lt_1D/production \
        -f "$INPUT" -u -w \
        -o "inf_k${K}_1D_e${E}_r${REP}.txt" \
        -t "time_k${K}_1D_e${E}_r${REP}.txt" \
        -e "$E" -c -k "$K" > "log_k${K}_1D_e${E}_r${REP}.txt" 2>&1

    # --- Production (2D) ---
    srun -N "$NODES" --nodelist="$NODELIST" \
        -n "$CORES" --ntasks-per-node="$TPERNODE" \
        --exclusive \
        /scratch/ipopa/repro/imm_hclib/src/lt_2D/production_2D \
        -f "$INPUT" -u -w \
        -o "inf_k${K}_2D_e${E}_r${REP}.txt" \
        -t "time_k${K}_2D_e${E}_r${REP}.txt" \
        -e "$E" -c -k "$K" > "log_k${K}_2D_e${E}_r${REP}.txt" 2>&1

done

