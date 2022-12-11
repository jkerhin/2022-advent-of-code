from advent2022 import ses


def find_index(stream: str, n_chars: int = 4) -> int:
    """Find the index of the 'start-of-packet' marker

    'start-of-packet' marker is when all four preceeding characters are different

    """
    ix = n_chars
    while ix < len(stream):
        buffer = stream[ix - n_chars : ix]
        if len(set(buffer)) == n_chars:
            # All characters are unique, index found
            return ix
        ix += 1
    raise ValueError("Unique letter run not found")


if __name__ == "__main__":
    r = ses.get("https://adventofcode.com/2022/day/6/input")
    r.raise_for_status()

    ix = find_index(r.text)
    print(f"'Packet' index found at {ix}")

    ix = find_index(r.text, n_chars=14)
    print(f"'Message' index found at {ix}")
