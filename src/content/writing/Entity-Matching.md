---
title: "Entity Matching"
date: 2026-02-23
---

Mr. Abrams has run Abram's PC, a beloved mom-and-pop computer parts store, for years. But with demand exploding and operations spiraling beyond what one person can manage, he jumps at an offer he can't refuse: a complete inventory buyout from the Microcenter down the road, for a pretty penny.
<br />
<br />

But now, Microcenter has a problem. Mr. Abram's records are structured but messy ![Local Image](./images/AbramsPC.png)and they need to merge their inventory schema with that of Abram's PC's. There are many issues that can arise here, but a particularly interesting one is Entity Resolution (ER). This problem asks how, given two tables of data, we can merge them s.t. there is no more than one row in the merged schema corresponding to each real world entity. 
<br />
<br />

The classical ER framework consists of a *blocking* step, where similar rows are grouped into blocks based on shared attributes, and then *matching*, where individual rows are compared to determine matches. And thus, we arrive at our problem of interest, Entity Matching. 
<br />
<br />

In our work, we formalize the problem simply; A binary classification with two tuple inputs. 
<br />
<br />

Let $r_i \in R$ and $s_j \in S$ be tuples from relations $R$ and $S$ respectively. Entity Matching is the task of learning $f$ s.t:
<div class="full-width">

$$f(r_i, s_j) = \begin{cases} 1 & \text{if } r_i \text{ and } s_j \text{ refer to the same real-world entity} \\ 0 & \text{otherwise} \end{cases}$$

</div>

Coming back to **A**bram's PC's and **M**icrocenter,

For example, 

<div class="full-width">


| source | id | brand | title | price | currency |
|--------|-----|-------|-------|-------|----------|
| Microcenter | 36868284 | Crucial | Crucial Memory 4GB DDR3L 1600 1.35V SODIMM Retail CT51264BF160BJ | 64.99 | CAD |
| Abram's PC | 13674019 | Crucial | Crucial 4GB DDR3 1600 MT/S (PC3-12800) CL11 SODIMM 204PIN 1.35V/1.5V Laptop Memory Kit | 0.00 | GBP |

</div>

This example takes some liberties. In reality, it is unlikely that the two stores would have the same schema structure, but even without this dimension, this problem is non-trivial.
<br />
<br />





