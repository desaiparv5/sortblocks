import sortblocks
from pathlib import Path


def test_sortblocks():
    sortblocks.sort_blocks(Path(__file__).parent.resolve() / Path('../sortblocks/sample.py'))


if __name__ == "__main__":
    test_sortblocks()
