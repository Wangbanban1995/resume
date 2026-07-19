# Chapter 8 Parameter–Distribution–Source–Correlation Summary Table (standalone extract)

Extracted from `WBE_Review_Ch1-10.md` §8.13 (Table 6) for standalone review. This is the same table embedded in the main chapter text, provided here as a separate file per request. "Typically correlated with" records the §8.10 dependencies documented in this review; entries marked "shape not established in this evidence base" reflect a documented evidence gap, not an assumption of normality.

---

## Table 6. Uncertainty source × type × distribution × propagation method × mitigation × residual effect

| Uncertainty source | Type (§8.1) | Plausible distribution shape | Typically correlated with (§8.10) | Propagation method (§8.6–8.9) | Mitigation | Residual effect if unaddressed |
|---|---|---|---|---|---|---|
| Individual shedding magnitude (§8.2) | Aleatory variability → parameter uncertainty at population scale | Right-skewed, long-tailed, over-dispersed (zero-inflated at low prevalence) — shape not established in this evidence base for every pathogen | Infection timing/kernel parameters (§7.2) | Monte Carlo or Bayesian hierarchical (§8.7, §8.9); delta method inappropriate (§8.6) | Externally-grounded shedding-kernel data (§4.3, §7.3) | Understated tail risk if normal approximation used |
| Excretion fraction / $CF$ (chemical) (§8.2, §7.1.1) | Epistemic parameter uncertainty; systematic bias if cross-population | Population-specific; represented as explicit prior in Jones et al. (2014) | Population demographic mismatch | Bayesian MCMC (demonstrated: Jones et al., 2014) | Population-matched clinical PK data | Systematic bias in $M(t)$, undetectable from wastewater data alone |
| Hydraulic retention-time distribution (§8.3) | Time-varying process uncertainty | Not a single value — a distribution across flow paths | Flow, rainfall | Hydraulic modeling + Monte Carlo | Tracer-study validation (rarely performed per this review's search) | Temporal-distortion (§3.0) uncorrected |
| Decay/transformation rate (§8.3, §4.1) | Time-varying process uncertainty | Temperature-dependent, not fixed | Temperature, retention time | Delta method (if near-linear) or Monte Carlo | Process-informed, temperature-covariate models (§4.3) | Amplitude bias, direction depends on temperature regime |
| Sedimentation/delayed release (§8.3, §4.1) | Unrepresented structural process | n/a — event-driven, not continuously distributed | Rainfall, flow | Not addressable by parameter-level propagation | Explicit structural term or event-flagging | False signal attributed to concurrent source event (§4.1) |
| CSO / overflow mass loss (§8.3, §6.8, §7.6) | Scenario uncertainty (discrete) | Bernoulli/event-indicator, not continuous | Rainfall | Scenario envelope (§8.12), not standard MC | Overflow-event flagging, exclusion, or explicit loss term | Capped/masked amplitude distortion (§4.2) |
| Recovery ($\eta_{rec}/\eta_{ext}$) (§8.4, §5.5) | Parameter uncertainty, amplitude-biasing | Matrix- and method-dependent; not established as normal | Inhibition/ion suppression | Delta method (if linear) or Monte Carlo | Recovery-control spikes, isotope-labeled internal standards | Systematic underestimation (recovery cannot exceed 100%) |
| Inhibition/ion suppression ($\eta_{inh}/\eta_{ion}$) (§8.4, §5.5) | Parameter uncertainty | Matrix-dependent | Recovery (shared matrix driver) | Monte Carlo (with recovery covariance, §8.10) | Inhibition controls, dilution, gp32 (§5.5) | Systematic bias, direction target-dependent |
| Interlaboratory/method effect (§8.4) | Structural/batch uncertainty | Documented wide spread across SOPs (Pecson et al., 2021; Yang et al., 2024) | Batch date, laboratory identity | Random-effects/hierarchical model (§8.9) | Shared reference standards, inter-lab calibration | Method effect mistaken for temporal/spatial signal (§5.5) |
| LOD/LOQ censoring (§8.4, §8.11) | Information loss / missingness | Left- or interval-censored, not a point value | Prevalence, dilution (rainfall) | Tobit, censored likelihood, multiple imputation, Bayesian censoring (§8.11) | Improved analytical sensitivity; report censoring rate | Bias, direction depends on substitution convention |
| Target/normalizer covariance (§8.5, §6.6) | Correlated measurement error | n/a — a covariance term, not a marginal distribution | By definition, this row *is* a correlation | Explicit covariance term in delta method or joint MC sampling | Shared-protocol co-analysis with documented covariance | Ratio uncertainty over- or under-stated depending on covariance sign |
| Structural model choice (§8.12, §7.0) | Structural uncertainty | n/a — discrete choice among candidate structures | Not a parameter; orthogonal axis | Ensemble averaging, Bayesian model averaging, scenario envelopes | Multi-structure comparison (rarely performed per Table 5) | Confidently wrong point estimate (§7.0's structural-adequacy failure) |
| Reference/clinical data uncertainty (§8.13, §7.5) | Epistemic, external to WBE chain | Ascertainment-dependent, itself time-varying | Testing policy, health-seeking behavior (§3.1) | Joint modeling of both uncertain series, not one-sided validation | Independent testing-rate data | Apparent WBE "failure" that is actually reference-data uncertainty |

---

## Companion: named correlated-parameter pairs (§8.10), as visualized in Figure 3

| Pair | Section documenting the dependency | Mechanism |
|---|---|---|
| Rainfall ↔ Flow | §4.2, §6.2 | Mechanically linked, not independently varying |
| Flow ↔ Hydraulic retention time | §4.1, §8.3 | Higher flow generally shortens retention time |
| Target sampling error ↔ Normalizer sampling error | §8.5 | Shared representativeness error when co-sampled from the same physical aliquot |
| Recovery ↔ Inhibition | §5.5, §8.4 | Both driven by shared underlying matrix composition |
| Infection timing ↔ Shedding-kernel parameters | §7.2 | Joint estimation trade-off, not two separately-uncertain quantities |
| Population change ↔ Water use | §6.3, §6.2 | Population influx raises both the flow-normalization denominator and the water-use proxy simultaneously |
| Temperature ↔ Decay rate | §4.1, §4.2, §8.3 | Mechanically linked via the same physical process |

**Ignoring these covariances can overstate or understate the true output interval depending on the sign of the correlation** (§8.10) — there is no single shortcut correction factor; the covariance structure must be estimated or reasoned through explicitly for the specific application.
