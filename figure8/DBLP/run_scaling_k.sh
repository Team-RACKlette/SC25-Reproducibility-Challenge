#!/usr/bin/env bash
#SBATCH -J dblp_kscaling
#SBATCH -o dblp_kscaling.out
#SBATCH -e dblp_kscaling.err
#SBATCH -t 01-00:00:00
#SBATCH --exclusive
#SBATCH --nodes=4
# --- Config ---
rm -rf results
INPUT="/scratch/ipopa/repro/imm_hclib/input_files/com-dblp.ungraph-LT.txt"
E=0.13
OUTPUT_DIR="results"

# Run size
NODES=4
TPERNODE=192
CORES=$(( NODES * TPERNODE ))
NODELIST="parmi1,parmi2,parmi3,parmi"

# --- Prepare output ---
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

# --- Sweep ---
K=64
REPS=5

while (( K <= 1024 )); do
    echo ">>> Running with k=$K"

    for REP in $(seq 1 "$REPS"); do
        echo "  -> Repetition $REP / $REPS"

        # --- Production (1D) ---
        srun -N "$NODES" --nodelist="$NODELIST" \
            -n "$CORES" --ntasks-per-node="$TPERNODE" \
            --exclusive \
            /scratch/ipopa/repro/imm_hclib/src/lt_1D/production \
            -f "$INPUT" -u -w \
            -o "inf_k${K}_1D_r${REP}.txt" \
            -t "time_k${K}_1D_r${REP}.txt" \
            -e "$E" -c -k "$K" > "log_k${K}_1D_r${REP}.txt" 2>&1

        # --- Production (2D) ---
        srun -N "$NODES" --nodelist="$NODELIST" \
            -n "$CORES" --ntasks-per-node="$TPERNODE" \
            --exclusive \
            /scratch/ipopa/repro/imm_hclib/src/lt_2D/production_2D \
            -f "$INPUT" -u -w \
            -o "inf_k${K}_2D_r${REP}.txt" \
            -t "time_k${K}_2D_r${REP}.txt" \
            -e "$E" -c -k "$K" > "log_k${K}_2D_r${REP}.txt" 2>&1

    done

    K=$(( K * 2 )) # Increase K for the next run
done

