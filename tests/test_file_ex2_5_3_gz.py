"""
Test_1
"""

import filecmp
import subprocess


def test_1():
    """Test_1"""
    subprocess.run(["python3", "./scripts/GC_analysis.py",
                             "-i", "./tests/ex2.fasta",
                             "-o", "./tests/ex2.fasta.wig.gz",
                             "-w", "5",
                             "-s", "3",
                             "-f", "gzip"])
    subprocess.run(["gzip", "-d", "ex2.fasta.wig.gz"])
    assert filecmp.cmp("./tests/ex2.fasta.wig", "./tests/ex2_5_3.wig")


if __name__ == "__main__":
    test_1()
