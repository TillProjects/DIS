from collections import defaultdict
import itertools

# -----------------------------
# 🔹 Hilfsfunktion: Items zählen
# -----------------------------
def count_single_items(transactions):
    item_count = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            item_count[(item,)] += 1
    return item_count

# --------------------------------------------
# 🔹 Hilfsfunktion: Filtere nach Mindest-Support
# --------------------------------------------
def filter_itemsets_by_support(counts, minsup_count):
    return {item for item, count in counts.items() if count >= minsup_count}

# -----------------------------------------
# 🔹 Hilfsfunktion: Kandidaten erzeugen (Ck)
# -----------------------------------------
def generate_candidates(prev_itemsets, k):
    candidates = set()
    prev_list = list(prev_itemsets)
    for i in range(len(prev_list)):
        for j in range(i + 1, len(prev_list)):
            union = tuple(sorted(set(prev_list[i]) | set(prev_list[j])))
            if len(union) == k:
                candidates.add(union)
    return candidates

# ------------------------------------------------------
# 🔹 Hilfsfunktion: Zähle Support für gegebene Kandidaten
# ------------------------------------------------------
def count_support(transactions, candidates):
    candidate_count = defaultdict(int)
    for transaction in transactions:
        t_set = set(transaction)
        for candidate in candidates:
            if set(candidate).issubset(t_set):
                candidate_count[candidate] += 1
    return candidate_count

# ------------------------------------------
# 🔹 Hauptfunktion: Apriori-Algorithmus
# ------------------------------------------
def apriori(transactions, minsup_ratio):
    num_transactions = len(transactions)
    minsup_count = int(minsup_ratio * num_transactions)

    itemsets_by_size = dict()
    frequent_itemsets_with_support = []

    # Schritt 1: 1-Itemsets zählen & filtern
    single_counts = count_single_items(transactions)
    L1 = filter_itemsets_by_support(single_counts, minsup_count)
    itemsets_by_size[1] = L1

    # Wiederholung für k ≥ 2
    k = 2
    L_prev = L1

    while L_prev:
        candidates = generate_candidates(L_prev, k)
        candidate_counts = count_support(transactions, candidates)
        Lk = filter_itemsets_by_support(candidate_counts, minsup_count)

        if Lk:
            itemsets_by_size[k] = Lk
            for itemset in Lk:
                support = candidate_counts[itemset] / num_transactions * 100
                frequent_itemsets_with_support.append((itemset, round(support, 2)))

        L_prev = Lk
        k += 1

    return itemsets_by_size, frequent_itemsets_with_support

# ------------------------------------------
# 🔹 Main: Einlesen & Ausführen
# ------------------------------------------
if __name__ == "__main__":
    # Tr
