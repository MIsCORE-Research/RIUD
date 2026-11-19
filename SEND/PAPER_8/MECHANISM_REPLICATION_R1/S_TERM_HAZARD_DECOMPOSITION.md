# Frozen R40 S-term hazard decomposition

Input rows: 2976
Input SHA256: 6dc5b6261070250e5467b1b8e1c78b9b68ca52f6e5d5708e406b50a48dbc4796
Frozen gamma: 0.3162354634393393

For each frozen R40 P1 row, eta_without_S = eta_P1 - gamma*S. No coefficient, state, history, or likelihood refit was performed. The decomposition is algebraic and descriptive; it does not establish a microscopic origin.

Key quantities:
- `GAMMA_S` is the additive S contribution to eta.
- `LAMBDA_P1_WITHOUT_S` and `P_P1_WITHOUT_S` are the counterfactual frozen P1 hazard/probability with only the S term removed.
- `S_DELTA_LOGPROB` is the row log-probability change attributable to restoring the frozen S term relative to that counterfactual.

- GAMMA_S: median=-0.004117091254430516, IQR=[-0.07087307502209123,0.0798311612364655], min/max=[-0.28392594872375326,0.4575779618624876]
- LAMBDA_P1_WITHOUT_S: median=4.059285162708956, IQR=[1.0061611936358987,20.916600681243935], min/max=[0.17714475673709046,1110.3449938986125]
- LAMBDA_P1: median=4.241981583186702, IQR=[0.984623982573651,21.52698806123462], min/max=[0.1475293931957726,1370.4668531317095]
- P_P1_WITHOUT_S: median=0.11913655171874514, IQR=[0.030953361110897852,0.47985297723834686], min/max=[0.005520479487776991,0.9999999999999991]
- P_P1: median=0.1241513023530732, IQR=[0.030300936209318573,0.48968054935146227], min/max=[0.0045996824471274,1.0]
- S_DELTA_LOGPROB: median=0.0005876137408104181, IQR=[-0.005272041053644995,0.012784281851439115], min/max=[-0.6904443284384822,0.40249629923874486]

Total S-only log-probability contribution: 5.693923102455701
Positive-row count: 1672/2976
Negative-row count: 1304/2976

This does not turn S into a timestamp. It quantifies its role as a multiplicative hazard-rate modifier inside the frozen R40 operator.
