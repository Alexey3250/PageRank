# PageRank

#### Explanations

1. **Transition Model**: We calculate the probabilities based on the damping factor and outgoing links.
    - If there are no outgoing links, we assume it links to every other page.
2. **Sample PageRank**:
    - The first sample is chosen completely at random.
    - For subsequent samples, probabilities from the transition model are used.
3. **Iterate PageRank**: We iterate until the change in PageRank value between iterations is less than 0.001 for all pages.

#### Key Terminology and Formulas

- **Damping Factor (d)**: The probability of following a link.
    
    $ PageRank(i)\=(1−d)+d∗∑j∈B(i)PageRank(j)L(j)PageRank(i) = (1 - d) + d \* \\sum\_{j \\in B(i)} \\frac{PageRank(j)}{L(j)}PageRank(i)\=(1−d)+d∗∑j∈B(i)​L(j)PageRank(j) $
    
- **Transition Model**: Dictates the probabilities of moving from one page to another.
    
   $ T(pagei)\=(1−d)/N+d/L(pagei)T(page\_i) = (1 - d) / N + d / L(page\_i)T(pagei​)\=(1−d)/N+d/L(pagei​) $