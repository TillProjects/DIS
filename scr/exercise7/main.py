from collections import defaultdict, Counter
from typing import List, Tuple, Set, Dict

# Typ: Transaktion = Liste von ganzen Zahlen
Transaction = List[int]
Itemset = Tuple[int, ...]
Transactions = List[Transaction]

# Zählt einzelne Items (als Tupel)
def count_single_items(transactions: Transactions) -> Counter[Itemset]:
    flat_items = [(item,) for transaction in transactions for item in transaction]
    return Counter(flat_items)

# Filtert Itemsets mit genug Support
def filter_itemsets_by_support(counts: Dict[Itemset, int], minsup_count: int) -> Set[Itemset]:
    return {item for item, count in counts.items() if count >= minsup_count}

# Generiert Kandidaten der Länge k aus den vorherigen Itemsets
def generate_candidates(prev_itemsets: Set[Itemset], k: int) -> Set[Itemset]:
    candidates = set()
    prev_list = list(prev_itemsets)
    for i in range(len(prev_list)):
        for j in range(i + 1, len(prev_list)):
            union = tuple(sorted(set(prev_list[i]) | set(prev_list[j])))
            if len(union) == k:
                candidates.add(union)
    return candidates

# Zählt, wie oft Kandidaten in Transaktionen vorkommen
def count_support(transactions: Transactions, candidates: Set[Itemset]) -> Dict[Itemset, int]:
    candidate_count = defaultdict(int)
    for transaction in transactions:
        t_set = set(transaction)
        for candidate in candidates:
            if set(candidate).issubset(t_set):
                candidate_count[candidate] += 1
    return candidate_count

# Führt den Apriori-Algorithmus aus
def apriori(transactions: Transactions, minsup_ratio: float) -> Tuple[Dict[int, Set[Itemset]], List[Tuple[Itemset, float]]]:
    num_transactions = len(transactions)
    minsup_count = int(minsup_ratio * num_transactions)

    itemsets_by_size: Dict[int, Set[Itemset]] = dict()
    frequent_itemsets_with_support: List[Tuple[Itemset, float]] = []

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

# Main: Einlesen & Ausführen
if __name__ == "__main__":
    # Transaktionen einlesen
    with open("transactions.txt", "r") as file:
        transactions: Transactions = [list(map(int, line.strip().split())) for line in file]

    minsup_ratio = 0.01

    # Apriori ausführen
    itemsets_by_size, frequent_itemsets_with_support = apriori(transactions, minsup_ratio)

    # Ausgabe: Anzahl pro Itemset-Größe
    print("Anzahl häufiger Itemsets pro Länge:")
    for k, itemsets in itemsets_by_size.items():
        print(f"  {k}er Itemsets: {len(itemsets)}")

    # Ausgabe: Häufige Itemsets mit Support speichern
    with open("frequent_itemsets_with_support.txt", "w") as f:
        for itemset, support in frequent_itemsets_with_support:
            f.write(f"{itemset}: {support}%\n")
