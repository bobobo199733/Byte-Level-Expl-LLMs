# Bytecode Level Explainability of Large Language Model Code Generation #

> **Research replication status (November 2026).**
> The historical 42.59% result is a single fixed task split, not a
> cross-task performance guarantee. The saved 500-split analysis
> (`research/cross_validation/cv_stats.json`) reports approximately
> **34.41% mean accuracy**, near the three-class chance reference.
> All 1,316 saved bytecode feature vectors were reproduced exactly by
> the researcher with CPython 3.13.18, and the saved classifier's 42.5856%
> test accuracy was reproduced. The new task-nested evaluation has not
> yet been run on the full dataset; do not interpret its existence as
> new empirical findings.
>
> **New research entry points:** [RQ1/RQ2 project guide](research/README_RQ1_RQ2.md),
> [RQ1 nested evaluation](research/rq1/run_nested_cv.py),
> [RQ2 validation roadmap](research/rq2/README.md).
> Historical scripts, datasets, models and SHAP artifacts remain unchanged.
>
Replication Package for "Bytecode Level Explainability of Large Language Model Code Generation" paper submitted at ICSE 2027.

Large Language Models (LLMs) are increasingly used for code generation, yet it remains difficult to explain how different models vary in their implementation choices. 
This study investigates whether SHAP-based explanations of bytecode classifiers can reveal meaningful, human-interpretable differences between LLM-generated Python programs.

A dataset of 1,316 Python scripts was generated from three open-weight LLMs: LLaMA 3.1 8B, Mistral 7B, and Qwen2.5 7B, across 50 programming tasks. 
An XGBoost classifier trained on a disjoint task split achieved 42.59\% accuracy on held-out tasks, above the 33.3\% random baseline, indicating that Python bytecode contains a learnable signal about the generating model. 
TreeSHAP was then used to identify influential byte positions, and backtracking was applied to trace these features from SHAP attribution to bytecode instructions and source-level constructs.

The strongest finding was byte\_16 = STORE\_FAST(110), which consistently contributed toward Mistral predictions and appeared in 14 Mistral-generated files across 6 of the 10 unseen test tasks. 
Backtracking showed that this byte position often corresponded to early variable assignments or storage operations in Mistral-generated code, while the corresponding LLaMA and Qwen programs used different source-level constructs at the same position. 
In contrast, byte\_14 = LOAD\_GLOBAL(91) was globally important and strongly associated with LLaMA by SHAP, but did not generalize reliably on held-out tasks. 
This contrast shows that SHAP can identify candidate model-specific implementation patterns, but attribution alone is insufficient.

The results demonstrate that SHAP-based bytecode explanations can provide meaningful insights into structural differences between LLM-generated programs when combined with source-level backtracking and validation on unseen tasks. 
The proposed workflow is therefore best understood as an exploratory method for identifying and validating candidate implementation patterns, rather than as a reliable LLM authorship detector.
