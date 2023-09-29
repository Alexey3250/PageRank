import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    N = len(corpus)
    model = {}
    
    if len(corpus[page]) == 0:  # If no outgoing links, assume it links to all pages (including itself)
        for p in corpus:
            model[p] = 1 / N
    else:
        for p in corpus:  # Initialize probabilities
            model[p] = (1 - damping_factor) / N
            
        for link in corpus[page]:  # Update probabilities based on links
            model[link] += damping_factor / len(corpus[page])
            
    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    samples = []
    ranks = {page: 0 for page in corpus}
    
    # First sample (chosen randomly)
    sample = random.choice(list(corpus.keys()))
    samples.append(sample)
    
    for _ in range(n - 1):
        model = transition_model(corpus, sample, damping_factor)
        sample = random.choices(list(model.keys()), list(model.values()), k=1)[0]
        samples.append(sample)
        
    # Count occurrences of each page in samples
    for sample in samples:
        ranks[sample] += 1 / n
        
    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    ranks = {page: 1 / N for page in corpus}
    new_ranks = {}
    delta = 1
    
    while delta > 0.001:
        for page in corpus:
            new_rank = (1 - damping_factor) / N
            for possible_page in corpus:
                if page in corpus[possible_page]:
                    new_rank += damping_factor * (ranks[possible_page] / len(corpus[possible_page]))
                elif len(corpus[possible_page]) == 0:
                    new_rank += damping_factor / N
            new_ranks[page] = new_rank

        delta = sum(abs(new_ranks[page] - ranks[page]) for page in corpus)
        ranks = new_ranks.copy()
        
    return ranks


if __name__ == "__main__":
    main()
