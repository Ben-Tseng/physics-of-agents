# Baseline reproduction

The official offline mock pipeline completed without an API key. The main
`res/4_prediction.ipynb` notebook also completed on the released data.

The reproduced artifact was compared with the repository's checked-in
`couplings.json` over 372 numeric values. The maximum absolute difference was
`5.11e-13`, which is floating-point noise.

The five objective coupling values used by the draft are the repository values
rounded to two decimals for all four models.

Although fitting is performed on standardized columns, `res/utils.py` converts
the fitted coefficients back to raw feature units and adjusts the intercept
before saving. No additional de-standardization is required when applying the
stored coefficients to raw design rows.

This validates the coefficient extraction. It does not validate the draft's
synthetic intrinsic-field distribution, attack-message semantics, or causal
interpretation. Those assumptions are tested separately in `res_attack/`.
