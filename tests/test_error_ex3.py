"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

"""
test_error_ex3.py
Test if a TypeError is correctly raised when a non-fasta file is given to the GC program.
"""

import subprocess


def test_error_ex3():
    """test_error_ex3"""
    result = subprocess.run(["python3", "./GC_analysis/GC_analysis.py",
                             "-i", "./tests/ex3.fasta",
                             "-o", "./tests/ex3.fasta.wig",
                             "-w", "5",
                             "-s", "5"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    assert result.stderr.split(b"\n")[-2] == b"TypeError"

    assert result.returncode == 1

    assert result.stdout[-28:] == b" contains no sequence data.\n"


if __name__ == "__main__":
    test_error_ex3()
