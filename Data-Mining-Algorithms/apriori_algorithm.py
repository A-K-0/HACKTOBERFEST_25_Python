
from itertools import combinations

transactions = [
    ['milk', 'bread', 'butter'],
    ['beer', 'bread'],
    ['milk', 'bread', 'butter', 'beer'],
    ['bread', 'butter'],
    ['milk', 'bread', 'beer']
]

min_support = 0.6  
min_confidence = 0.7  
def create_candidates(frequent_itemsets, k):
    candidates = []
    items = set()
    for itemset in frequent_itemsets:
        for item in itemset:
            items.add(item)
    items = list(items)
    for combination in combinations(items, k):
        candidates.append(set(combination))
    return candidates

def calculate_support(transactions, candidates):
    support_count = {}
    for candidate in candidates:
        count = 0
        for transaction in transactions:
            if candidate.issubset(transaction):
                count += 1
        support_count[frozenset(candidate)] = count / len(transactions)
    return support_count

def filter_itemsets(support_count, min_support):
    frequent_itemsets = []
    for itemset, support in support_count.items():
        if support >= min_support:
            frequent_itemsets.append(set(itemset))
    return frequent_itemsets

def apriori(transactions, min_support):
    transactions = list(map(set, transactions))
    
    items = set()
    for transaction in transactions:
        for item in transaction:
            items.add(item)
    candidates = [set([item]) for item in items]
    
    all_frequent_itemsets = []
    k = 1
    while candidates:
        support_count = calculate_support(transactions, candidates)
        frequent_itemsets = filter_itemsets(support_count, min_support)
        if frequent_itemsets:
            all_frequent_itemsets.extend(frequent_itemsets)
        k += 1
        candidates = create_candidates(frequent_itemsets, k)
    return all_frequent_itemsets

def generate_rules(frequent_itemsets, transactions, min_confidence):
    transactions = list(map(set, transactions))
    rules = []
    for itemset in frequent_itemsets:
        if len(itemset) > 1:
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = set(antecedent)
                    consequent = itemset - antecedent
                    support_count_itemset = sum(1 for t in transactions if itemset.issubset(t)) / len(transactions)
                    support_count_antecedent = sum(1 for t in transactions if antecedent.issubset(t)) / len(transactions)
                    confidence = support_count_itemset / support_count_antecedent
                    if confidence >= min_confidence:
                        rules.append((antecedent, consequent, confidence))
    return rules

frequent_itemsets = apriori(transactions, min_support)
print("Frequent Itemsets:")
for itemset in frequent_itemsets:
    print(itemset)

rules = generate_rules(frequent_itemsets, transactions, min_confidence)
print("\nAssociation Rules:")
for antecedent, consequent, confidence in rules:
    print(f"{set(antecedent)} -> {set(consequent)} (Confidence: {confidence:.2f})")
