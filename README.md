## Network Based Recommendation Strategy for Amazon Books

Our goal here is to develop a network based recommendation system that provides recommendation to a user based on the books that have been purchased on Amazon. We want to develop a system that deals both with high degree of centrality as well as data sparsity.

For the sake of simplicity, we fix the size of our recommendation set to size n. Figure 1 illustration is for n = 2. The first step of our implementation would be to create the Ego Network of the ASIN at depth = 1. In the ego network, all neighbor nodes A, B, C, D are shown. We then create an inland graph, which remove links that have similarity less than 0.5. This is to ensure we have more similar items in the recommendation list. At this point, we check the degree of centrality of the inland graph, which is 3. If this degree is greater than or equal to n, we just sort the neighbors of inland graph by weight and pick the top n item into our recommendation set. As shown below, when n = 2, we look at the inland graph for top 2 weights, which here are of A, B. Hence recommendation set will have {A, B}. 

<img src="/assets/Picture1.png" 
align="middle"/>

Now, considering same scenario as above, if n = 5, then based on inland’s degree of centrality, it becomes a case of “sparse data”. At the stage of inland graph, we take all the neighbors and put them in recommendation set {A, B, D} (figure 2). In order to combat sparsity, we now consider neighbors’ neighbors of ego graph. The reason we consider ego graph is because after trimming, inland may land up with 0 connected nodes. The new nodes introduced are {1, 2, 3, C}. Node 1, 2, 3 are not neighbors to ASIN but we can still calculate their similarity to ASIN (shown with dashed lines). It is just like Facebook recommending friends’ friends to you. For simplicity, we just limit to neighbors’ neighbors. Even though ASIN and Node 1, 2, 3 have never been co-purchased together but their high similarity makes them good candidate to be put in the recommendation set. For example, our user is a chef. ASIN is a book on French cooking. B is a book on Italian cooking and 1 is another book on Italian cooking but it is new in the market. In that case, it seems reasonable to advise our chef user, book 1. Before sorting we remove exactly matching titles (i.e. same book title but different editions). For example, if user bought “Mastering the Art of French Cooking” edition 1, we do not want to recommend him “Mastering the Art of French Cooking” edition 2. Again, we pick only those similarities which are greater than 0.5. Since we already picked 3 recommendations from the inland graph - {A, B, D}, we now pick only 5-3 = 2 from the neighbors’ neighbors i.e. {2, 1} and append to our recommendation list – {A, B, D, 2, 1}. Please note that for both cases of high and low degree of centrality, if two competing nodes have same weight, we break tie with their average rating.

<img src="/assets/Picture2.png" 
class="center"/>

### Disclaimar:
PreprocessAmazonBooks.py included in the repo is part of the course CS509 - Arizona State University. The author of this repo does not wish to take credit for PreprocessAmazonBooks.py code.
