import networkx
import operator
from operator import itemgetter
import matplotlib.pyplot

# read the data from the amazon-books.txt;
# populate amazonProducts nested dicitonary;
# key = ASIN; value = MetaData associated with ASIN
fhr = open('./amazon-books.txt', 'r', encoding='utf-8', errors='ignore')
amazonBooks = {}
fhr.readline()
for line in fhr:
    cell = line.split('\t')
    MetaData = {}
    MetaData['Id'] = cell[0].strip() 
    ASIN = cell[1].strip()
    MetaData['Title'] = cell[2].strip()
    MetaData['Categories'] = cell[3].strip()
    MetaData['Group'] = cell[4].strip()
    MetaData['Copurchased'] = cell[5].strip()
    MetaData['SalesRank'] = int(cell[6].strip())
    MetaData['TotalReviews'] = int(cell[7].strip())
    MetaData['AvgRating'] = float(cell[8].strip())
    MetaData['DegreeCentrality'] = int(cell[9].strip())
    MetaData['ClusteringCoeff'] = float(cell[10].strip())
    amazonBooks[ASIN] = MetaData
fhr.close()

# read the data from amazon-books-copurchase.adjlist;
# assign it to copurchaseGraph weighted Graph;
# node = ASIN, edge= copurchase, edge weight = category similarity
fhr=open("amazon-books-copurchase.edgelist", 'rb')
copurchaseGraph=networkx.read_weighted_edgelist(fhr)
fhr.close()

# now let's assume a person is considering buying the following book;
# what else can we recommend to them based on copurchase behavior 
# we've seen from other users?
print ("Looking for Recommendations for Customer Purchasing this Book:")
print ("--------------------------------------------------------------")
asin = '0805047905' # from the assignment
#asin = '1559360968' # Contain sparse data
  
# example code to start looking at metadata associated with this book
print ("ASIN = ", asin) 
print ("Title = ", amazonBooks[asin]['Title'])
print ("SalesRank = ", amazonBooks[asin]['SalesRank'])
print ("TotalReviews = ", amazonBooks[asin]['TotalReviews'])
print ("AvgRating = ", amazonBooks[asin]['AvgRating'])
print ("DegreeCentrality = ", amazonBooks[asin]['DegreeCentrality'])
print ("ClusteringCoeff = ", amazonBooks[asin]['ClusteringCoeff'])

# First we need to fix the size of the recommendation set
n = 10 # size of the set

# We need to find the ego network of ASIN
ego = networkx.ego_graph(copurchaseGraph, asin, radius=1) 

# Now we want to trim the ego network such that only those edges remain which have weight > 0.5
threshold = 0.5
egotrim = networkx.Graph()
for n1, n2, e in ego.edges(data=True):
    if e['weight'] >= threshold:
        egotrim.add_edge(n1,n2,e) 
        
# We need to find number of neighbors of asin in this ego trimmed network 
ngbsLen = len(egotrim.neighbors(asin))

# Now we compare the asin's degree of centrality with n.
# If ngbsLen >= n we present top n neighboring ASINs by weights(similarity).
if ngbsLen >= n: 
    
    # From ego trim graph, find connecting nodes to asin and their weights and save into neighborsInfo
    neighborsInfo = []
    for line in networkx.generate_edgelist(egotrim, data=['weight']):
        if asin in line:
            tempList = []
            tempList = line.split()
            neighborsInfo.append(tempList) 

    # Below code snippet is removing the ASIN from the sublists of sortedList as ASIN cannot be a recommendation to itself.
    trimNeighbors = []
    for i in range(len(neighborsInfo)):
        recosList =[]
        for j in range(0,len(neighborsInfo[i])):
            if neighborsInfo[i][j] != asin:
                recosList.append(neighborsInfo[i][j])
        trimNeighbors.append(recosList)  
    
    # From similarNeighbors, we have to remove neighbors which have same book title. This can occur when 
    # when two books have same title but they are different versions. We want to make sure we are not
    # recommending same book to the user which she has already purchased.
    bookLists = []
    for item in range(len(trimNeighbors)):
        bookSubList = []
        bookTitle = amazonBooks[trimNeighbors[item][0]]['Title']
        bookRating = amazonBooks[trimNeighbors[item][0]]['AvgRating']
        if bookRating == None: # This is done incase neighbor does not have rating metadata
            bookRating = 0
        bookSubList = [bookTitle, bookRating, trimNeighbors[item][1]]
        bookLists.append(bookSubList) 
    
    # Removing same book title from the bookLists
    updateBookList = [] 
    for book in range(len(bookLists)):
        if bookLists[book][0] != amazonBooks[asin]['Title']:
            updateBookList.append(bookLists[book])
            
    # Next we sort the list and present the user with top n book title and their review ratings
    updateBookList = sorted(updateBookList, key = operator.itemgetter(2, 1), reverse = True)
    updateBookList = updateBookList[0:n]

    recommendations = []
    for m in range(len(updateBookList)):
        recosList = []
        recosList = [updateBookList[m][0],updateBookList[m][1]]
        recommendations.append(recosList)
    print()
    print("Recommendation List:")
    print()
    print(recommendations)

# Below code snippet is incase degree of centrality is less than the the recommendation set of n    
    
else:
    shortBy = n - ngbsLen
    # From ego trim graph, find connecting nodes to asin and their weights and save into neighborsInfo
    neighborsInfo = []
    for line in networkx.generate_edgelist(egotrim, data=['weight']):
        if asin in line:
            tempList = []
            tempList = line.split()
            neighborsInfo.append(tempList)

    # Below code snippet is removing the ASIN from the sublists of sortedList as ASIN cannot be a recommendation to itself.
    trimNeighbors = []
    for i in range(len(neighborsInfo)):
        recosList =[]
        for j in range(0,len(neighborsInfo[i])):
            if neighborsInfo[i][j] != asin:
                recosList.append(neighborsInfo[i][j])
        trimNeighbors.append(recosList)  
    
    # From similarNeighbors, we have to remove neighbors which have same book title. This can occur when 
    # when two books have same title but they are different versions. We want to make sure we are not
    # recommending same book to the user which she has already purchased.
    bookLists = []
    for item in range(len(trimNeighbors)):
        bookSubList = []
        bookTitle = amazonBooks[trimNeighbors[item][0]]['Title']
        bookRating = amazonBooks[trimNeighbors[item][0]]['AvgRating']
        if bookRating == None: # This is done incase neighbor does not have rating metadata
            bookRating = 0
        bookSubList = [bookTitle,bookRating, trimNeighbors[item][1]]
        bookLists.append(bookSubList) 
    
    # Removing same book title from the bookLists
    updateBookList = []
    for book in range(len(bookLists)):
        if bookLists[book][0] != amazonBooks[asin]['Title']:
            updateBookList.append(bookLists[book])
    
    # Next we sort the list and present the user with top n book titles and their review ratings
    updateBookList = sorted(updateBookList, key = operator.itemgetter(2, 1), reverse = True)
    updateBookList = updateBookList[0:n]
    recommendations = []
    for m in range(len(updateBookList)):
        recosList = []
        recosList = [updateBookList[m][0],updateBookList[m][1]]
        recommendations.append(recosList)

    # Now since the data is sparse, we will find neighbors' neighbors and find how similar they are to asin
    similarity = 0 
    
    # We find neighbors list of the ego network 
    egoNeighbourList = ego.neighbors(asin)  
    
    # In the egoNeighbourList we add asin as asin cannot be its own neighbor
    egoNeighbourList.append(asin) 
    
    # neighboursNeighbours will contain neighbors' neighbors minus trimNeighbourList
    neighboursNeighbours = []
 
    # For every neighbor, we find their neighbors from the copurchase graph
    for h in egoNeighbourList:
        neighboursNeighbours = neighboursNeighbours + copurchaseGraph.neighbors(h)
    
    # Since neighboursNeighbours contains original neighbors from trim network, we remove them
    neighboursNeighbours = list(set(neighboursNeighbours) - set(egoNeighbourList))
    
    # For every node in neighboursNeighbours, we find AvgRating, Title, Similarity to asin 
    # and save it into sparseRecommendations
    # Here we again add those items in sparseRecommendations which have similarity > 0.5
    sparseRecommendations = [] 
    for nasin in neighboursNeighbours:
        recosList = []
        # Below we try to find the similarity between two non connected nodes by the number of common words they have in categories
        n1 = set((amazonBooks[asin]['Categories']).split())
        n2 = set((amazonBooks[nasin]['Categories']).split())
        n1In2 = n1 & n2
        n1Un2 = n1 | n2 
        if (len(n1Un2)) > 0:
            similarity = round(len(n1In2)/len(n1Un2),2)
            
        # Again, we keep only those items which have similarity greater than 0.5
        if similarity > 0.5:
            bookRating = amazonBooks[nasin]['AvgRating']
            bookTitle = amazonBooks[nasin]['Title']
            if bookRating == None: # This is done incase neighbor does not have rating metadata
                bookRating = 0
            recosList = [bookTitle, bookRating, similarity]
            sparseRecommendations.append(recosList)
    sparseRecommendations = sorted(sparseRecommendations, key = operator.itemgetter(2, 1), reverse = True)
    sparseRecommendations = sparseRecommendations[0:shortBy]

    # Next we sort the list and present the user with top n book title and their review ratings
    neighborsRecommendations = []
    for m in range(len(sparseRecommendations)):
        recosList = []
        recosList = [sparseRecommendations[m][0],sparseRecommendations[m][1]]
        neighborsRecommendations.append(recosList)
    print()
    print("Recommendation List:")
    print()
    recommendations = recommendations + neighborsRecommendations
    print(recommendations)

 
