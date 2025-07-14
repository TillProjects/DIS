from itertools import combinations
from collections import defaultdict
import math

MIN_SUPPORT_PERCENT = 1.0  # Minimum support in %
TRANSACTIONS_FILE = "Transactions.txt"

def load_transactions(filename):
    transactions = []
    with open(filename, 'r') as file:
        for line in file:
            items = tuple(sorted(map(int, line.strip().split())))
            if items:
                transactions.append(items)
    return transactions

def get_frequent_itemsets(transactions, minsup_count):
    itemsets = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            itemsets[(item,)] += 1
    L = {k: v for k, v in itemsets.items() if v >= minsup_count}
    all_frequent_itemsets = dict()
    k = 1
    while L:
        all_frequent_itemsets[k] = L
        k += 1
        candidate_counts = defaultdict(int)
        prev_itemsets = list(L.keys())
        candidates = generate_candidates(prev_itemsets, k)
        for transaction in transactions:
            transaction_set = set(transaction)
            for candidate in candidates:
                if set(candidate).issubset(transaction_set):
                    candidate_counts[candidate] += 1
        L = {k: v for k, v in candidate_counts.items() if v >= minsup_count}
    return all_frequent_itemsets, len(transactions)

def generate_candidates(prev_itemsets, k):
    candidates = set()
    len_prev = len(prev_itemsets)
    for i in range(len_prev):
        for j in range(i + 1, len_prev):
            l1, l2 = prev_itemsets[i], prev_itemsets[j]
            if l1[:k - 2] == l2[:k - 2]:
                new_candidate = tuple(sorted(set(l1) | set(l2)))
                if len(new_candidate) == k and all(tuple(sorted(sub)) in prev_itemsets for sub in combinations(new_candidate, k - 1)):
                    candidates.add(new_candidate)
    return candidates

def format_results(frequent_itemsets, total_transactions):
    print("Anzahl der häufigen Itemsets je Größe:")
    for size in sorted(frequent_itemsets.keys()):
        print(f"- {size}-Itemsets: {len(frequent_itemsets[size])}")
    print("\nHäufige Itemsets (ab Größe 2) mit Support (%):")
    result_list = []
    for size in sorted(frequent_itemsets.keys()):
        if size < 2:
            continue
        for itemset, count in frequent_itemsets[size].items():
            support = 100 * count / total_transactions
            result_list.append((itemset, f"{support:.2f}%"))
    for itemset, support in result_list:
        print(f"{itemset}: {support}")
    # Optional: speichern
    with open("frequent_itemsets.txt", "w") as f:
        for itemset, support in result_list:
            f.write(f"{itemset}: {support}\n")

def main():
    transactions = load_transactions(TRANSACTIONS_FILE)
    minsup_count = math.ceil(len(transactions) * MIN_SUPPORT_PERCENT / 100)
    frequent_itemsets, total = get_frequent_itemsets(transactions, minsup_count)
    format_results(frequent_itemsets, total)

if __name__ == "__main__":
    main()
