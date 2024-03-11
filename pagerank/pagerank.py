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

    # Total number of pages in corpus
    pages = len(corpus.keys())

    # Pages linked from page 
    links_from_page = corpus[page]

    distribution_proba = {}
    if links_from_page:
        for key in corpus.keys():
            distribution_proba[key] = (1 - damping_factor) / pages

            if key == page:
                continue

            if key in links_from_page:
                distribution_proba[key] += (damping_factor / len(links_from_page))
        
    else:
        for key in corpus.keys():
            distribution_proba[key] = 1 / pages

    return distribution_proba


def get_next_sample(distribution):
    """
    Given a distribution probabilities for each html page,
    this functions selects one pseudorandomly (weighted by its probabilities)
    """
    # List of tuples
    distribution_list = list(distribution.items())

    # Extract the keys and values from dictionary separately
    pages, probabilities = zip(*distribution_list)

    # Return page chosen pseudorandomly
    return random.choices(pages, weights=probabilities, k=1)[0]


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize page_rank dictionary assigning count 0 for each page in corpus
    page_rank = {}
    for page in corpus.keys():
        page_rank[page] = 0

    for i in range(n):
        # If first sample, choose a page at random
        if i == 0:
            sample = random.choices(tuple(page_rank.keys()))[0]
            page_rank[sample] += 1
        # Otherwise, get probabilities distribution from transition_model,
        # Get next sample pseudorandomly (base on previous sample probabilities)
        else:
            transition = transition_model(corpus, sample, damping_factor)
            sample = get_next_sample(transition)
            page_rank[sample] += 1

    # Transform count into distribution
    for page, count in page_rank.items():
        page_rank[page] = count / n

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Total number of pages in the corpus 
    total_pages = len(corpus.keys())

    # Update corpus to deal with pages without links 
    updated_corpus = update_corpus(corpus)

    # Threshold
    threshold_value = 0.001 
    threshold = False

    iterations = 0
    page_rank_iterations = {} # This dictionary will save all the calculations of N iterations
    while(not threshold):
        threshold_counter = 0 
        for page in corpus.keys():

            if iterations != 0:
                # Get all pages that links to page p
                # incoming_pages = links_to_page(corpus, page)
                incoming_pages = links_to_page(updated_corpus, page)

                # The probability that we were on page i and chose the link to page p
                prob_of_i_to_p = 0

                for i_page in incoming_pages:     
                    # The number of links present on page i
                    num_links = len(updated_corpus[i_page])

                    # Page Rank of i in the last iteration / number of links present on page i
                    prob_of_i_to_p += page_rank_iterations[i_page][iterations - 1] / num_links

                page_rank_iterations[page].append( ((1 - damping_factor) / total_pages) + (damping_factor * prob_of_i_to_p) )

                # Check if threshold was reached
                if abs(page_rank_iterations[page][-1] - page_rank_iterations[page][-2]) <= threshold_value:
                    threshold_counter += 1

            else: # Begin (in first iteration) by assigning each page a rank of 1 / N, where N is the total number of pages in the corpus

                page_rank_iterations[page] = [1 / total_pages] 

        # If threshold of all pages was reached, stop
        if threshold_counter == total_pages:
            threshold = True

        iterations += 1


    # After reaching the threshold, get last page rank calculated from dictionary 
    page_rank = {}
    for key, values in page_rank_iterations.items():
        page_rank[key] = values[-1]

    return page_rank


def links_to_page(corpus, page):
    """
    TO DO
    """
    pages = []
    for key, value in corpus.items():
        if page in value:
            pages.append(key)

    return pages


def update_corpus(corpus):
    """
    TO DO
    """
    # List of All pages 
    pages = list(corpus.keys())

    for key in corpus.keys():
        if not corpus[key]:
            corpus[key] = set(corpus.keys())
    
    return corpus
    


if __name__ == "__main__":
    main()
