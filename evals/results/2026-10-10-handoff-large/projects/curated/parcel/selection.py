def select(records, tenant=None, limit=None):
    chosen=[]
    seen=set()
    for row in records:
        if tenant is not None and row["tenant"]!=tenant:
            continue
        key=(row["tenant"], row["id"])
        if key in seen:
            continue
        seen.add(key)
        chosen.append(row)
    # The cap applies to selected records, after tenant filtering and dedup.
    if limit is not None:
        chosen=chosen[:limit]
    return chosen
