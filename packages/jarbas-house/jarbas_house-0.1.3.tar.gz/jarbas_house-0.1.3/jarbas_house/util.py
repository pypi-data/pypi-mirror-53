from threading import Thread


def merge_dict(base, delta):
    """
        Recursively merging configuration dictionaries.

        Args:
            base:  Target for merge
            delta: Dictionary to merge into base
    """

    for k, dv in delta.items():
        bv = base.get(k)
        if isinstance(dv, dict) and isinstance(bv, dict):
            merge_dict(bv, dv)
        else:
            base[k] = dv


def create_daemon(func):
    t = Thread(target=func)
    t.setDaemon(True)
    t.start()
    return t
