"""
Test_1
"""

import filecmp
import subprocess


def test_1():
    """Test_1"""
    result = subprocess.run(["python3", "./scripts/GC_analysis.py",
                    "-i", "./tests/ex2.fasta",
                    "-o", "ex2.fasta.wig",
                    "-w", "5",
                    "-s", "5"], stderr=subprocess.PIPE)
    assert filecmp.cmp("./tests/ex2.fasta.wig", "./tests/ex2_5_5.wig")
    assert result.stderr == b"WARNING! This fasta file does not contain chromosome information.\n"

if __name__ == "__main__":
    test_1()
