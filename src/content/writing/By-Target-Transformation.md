---
title: "By-Target Transformation"
date: 2026-02-22
---

Microcenter resolved their entity matching problem. But even after deduplicating the merged inventory, a new one surfaces: downstream systems expect data in specific formats, and getting messy source data into those formats is, if anything, the harder problem.

Okay, that's a contrived segue. But the underlying issue is real. Data scientists reportedly spend 80 to 90% of their time on data integration and wrangling tasks, and a significant chunk of that is transforming datasets from one schema into another.
<br />
<br />

Consider a civil engineering team trying to train a model on building energy usage. They've collected data from 20 different energy companies, each with a different schema describing the same semantics. Sensor IDs, timestamps, kilowatt readings, building classifications, all labeled differently, formatted differently, typed differently. Getting everything into a single target format took months. And then one company updates their schema, and the pipeline breaks.
<br />
<br />

There are three broad approaches to automating this. *Transform by Instructions* (TBI) asks users to describe what they want in natural language. *Transform by Example* (TBE) asks them to provide paired input/output examples showing what the transformation should do. Both put the burden on the user to be precise, either in words or in examples, which is harder than it sounds and error-prone.
<br />
<br />

The approach we study, *Transform by Target* (TBT), is more forgiving. You provide your source data and a fuzzy example of what the output should look like. The examples don't need to correspond row-by-row to your source; they just need to illustrate the target format. The system infers the transformation itself.
<br />
<br />

In our work, we formalize the problem simply; given a set of source datasets $\mathcal{T}^{in}$, a target schema $S^{tgt}$, and a collection of target examples $\mathcal{T}_0^{tgt}$, find a sequence of operators $\mathcal{O} = \{o_1, ..., o_k\}$ s.t. $o_k(...(o_1(\mathcal{T}^{in}))) = \hat{\mathcal{T}}^{tgt}$. Each operator is selected and configured by an LLM in response to a prompt.
<br />
<br />

The obvious challenge is that raw tables can be large. Dumping them into a prompt introduces noise, hits context limits, and buries the signal. Our key insight was to run data profiling over the source and target first and feed the LLM a compact structured summary instead of the raw data. This summary captures column types, value ranges, cardinalities, functional dependencies, and column mapping candidates, the information actually relevant to reasoning about transformations.
<br />
<br />

But even with a clean summary, there are a lot of design choices to make. Should the LLM plan the full transformation pipeline at once, or decide one operator at a time? Should it use iterative critique, search, or simple chain-of-thought? How should context be shared between steps? We treat this as a design space exploration problem, systematically varying these dimensions and evaluating their effects rather than committing to a single architecture up front.
<br />
<br />

A few findings from this process stand out. Planning at the pipeline level works better for simpler transformations; operator-level planning handles complex, multi-step cases more robustly. Iterative critique, where the LLM checks its own output against data quality constraints and revises, consistently helps. Sharing context across operators, so that what the LLM learned in an earlier step informs later ones, was one of the bigger wins.
<br />
<br />

One pattern that kept showing up: LLMs struggle when column names are misleading or don't accurately summarize the column's semantics. A target column computed from a sum of reading scores labeled `reading_scores` looks, to the model, like it should just map directly from the source. The model reaches for the obvious interpretation and misses the aggregation entirely. Prompting the model to flag and reason about suspicious column names before generating code caught a meaningful fraction of these errors.
<br />
<br />

We evaluate on a 700-case benchmark drawn from real GitHub repositories, evenly spread across seven complexity levels based on the number of operators required. As a reference point, Auto-Pipeline, a strong training-based baseline, achieves roughly 77% overall accuracy on this benchmark, with performance dropping sharply as case complexity increases. The design choices we explore directly address this degradation.
<br />
<br />

The broader takeaway: LLMs are already capable of reasoning about complex data transformations. The limiting factor isn't the model; it's how the problem is set up. Data profiling, structured prompts, and thoughtful planning strategies do more work than any single prompting trick, and the right combination of them substantially outperforms methods that required months of training data to build.
