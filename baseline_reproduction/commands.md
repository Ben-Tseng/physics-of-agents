# Reproduction commands

Upstream commit: see `commit.txt`.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt

.venv/bin/python -m lib.datagen.collect_energy \
  --mock --mode subjective --limit 1 --num-agents 4 --num-edges 6 \
  --num-train-graphs 1 --num-seen-graphs 1 --num-fresh-graphs 0 \
  --no-lattices --trajectories 1 --num-steps 2 --k 3 \
  --max-workers 1 --seed 0 \
  --output-dir baseline_reproduction/mock_demo

cd res
JUPYTER_CONFIG_DIR=../baseline_reproduction/.jupyter \
JUPYTER_DATA_DIR=../baseline_reproduction/.jupyter_data \
IPYTHONDIR=../baseline_reproduction/.ipython \
../.venv/bin/jupyter nbconvert --to notebook --execute 4_prediction.ipynb \
  --output ../baseline_reproduction/4_prediction.executed.ipynb \
  --ExecutePreprocessor.timeout=-1
cd ..

.venv/bin/python baseline_reproduction/audit_baseline.py
.venv/bin/python res_attack/counterfactual_attack.py \
  --models gpt gma qwn lma --seeds 0 1 2 3 --strategies random \
  --output res_attack/results
.venv/bin/python res_attack/summarize_results.py \
  res_attack/results/counterfactual_attack.csv
```
