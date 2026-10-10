from .loader import load
from .selection import select
from .render import render

def execute(path, tenant=None, limit=None):
    records=load(path)
    chosen=select(records, tenant=tenant, limit=limit)
    return render(chosen)
