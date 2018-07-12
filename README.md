[![Build Status](https://travis-ci.org/tonyyzy/GC_analysis.svg?branch=master)](https://travis-ci.org/tonyyzy/GC_analysis)
[![Build Status](https://travis-ci.org/tonyyzy/GC_analysis.svg?branch=parallel)](https://travis-ci.org/tonyyzy/GC_analysis)
# GC-analysis
A command-line utility for calculating GC percentages of genome sequences

# Quick starter
Calculate the GC content of chromosome 17 of the human reference genome with window size (or span) = 5 and shift (or step) = 5. Input fasta file is `GRCh38-Chrom17.fasta` and output wiggle file is `GRCh38-Chrom17.wig`. Note that the output file's extension is added by the program.
```
~ $ GC_analysis -i GRCh38-Chrom17.fasta -w 5 -s 5 -o GRCh38-Chrom17
```

# Installation guide
Note that pyBigWig can only be used under linux environment. To work with Windows system, the Docker image can be used as shown below. Alternatively, you can clone the repository, comment out `import pyBigWig` and the script would work but without BigWig support.

1. Pip install GC_analysis
```
pip3 install GC_analysis
```
Then `GC_analysis.py` command will be available globally.
```
GC_analysis.py -i [INPUT] -o [OUTPUT] -w [window size] -s [shift]
```

2. Run the python script directly. Please ensure you have python3 installed with pyBigwig and Biopython.
Clone the github repository and install packages.
```
git clone https://github.com/tonyyzy/GC_analysis
cd GC_analysis
pip3 install -r requirements.txt
```
run the script from `GC_analysis` directory.
```
python3 ./scripts/GC_analysis.py -i [INPUT] -o [OUTPUT] -w [window size] -s [shift]
```

3. Use the packaged binary.
```
mkdir ~/GC_analysis
cd ~/GC_analysis
wget https://github.com/tonyyzy/GC_analysis/releases/download/v0.3/GC_analysis
```
Execute the binary command
```
GC_analysis -i [INPUT] -o [OUTPUT] -w [window size] -s [shift]
```

4. Use the Docker image.
Firstly, pull the docker image (around 384 MB)
```
docker pull tonyyzy/gc_analysis
```
To use input files outside the container and save output files on your computer, the `-v` volume mapping option will be used. You will need to know the absolute path of the directory you want to map (which can be found out with `pwd`).
```
docker run -v /your/local/path:/app tonyyzy/gc_analysis GC_analysis -i /app/yours.fasta -o /app/yours -w 5 -s 5
```
This option maps `/your/local/path` to `/app` under the container's root directory. Your result file will be saved to `/your/local/path/yours.wig`.

# Command-line options
```
~ $ GC_analysis -h
usage: GC_analysis [-h] -i INPUT_FILE -w WINDOW_SIZE -s SHIFT [-o OUTPUT_FILE]
                   [-ot] [-f {wiggle,gzip,bigwig}]

required named arguments:

-i INPUT_FILE, --input_file INPUT_FILE
INPUTFILE: Name of the input file in FASTA format

-w WINDOW_SIZE, --window_size WINDOW_SIZE
WINDOW_SIZE: Number of base pairs that the GC percentage is calculated for

-s SHIFT, --shift SHIFT
SHIFT: The shift increment (step size)

optional arguments:

-h, --help
Show the help message and exit

-o OUTPUT_FILE, --output_file OUTPUT_FILE
OUTPUT_FILE: Name of the output file

-ot, --omit_tail
Use if the trailing sequence should be omitted. Default behaviour is to retain the leftover sequence.

-f {wiggle,bigwig,gzip}, --output_format {wiggle,bigwig,gzip}
Choose output formats from wiggle, bigwig or gzip compressed wiggle file.

```
## Example usage
1. Calculate the GC content of chromosome 17 of the human reference genome, the percentage is calculated over five base pairs (window_size), and the window is shifted by five base pairs every time (i.e. there is no overlapping base paires in each entry).
```
~ $ GC_analysis -i GRCh38-Chrom17.fasta -w 5 -s 5 -o GRCh38-Chrom17
```

2. By default, the GC percentage of the trailing sequence is calculated and appended to the end of the output file. For example, with the following input
```
~ $ GC_analysis -i examaple1.fasta -w 5 -s 5 -o with_tail
```
and `example1.fasta` is
```
>chr1
AAAAACC
```
the generated `with_tail.wig` will look like
```
track type=wiggle_0 name="GC percentage" description="chr1"
variableStep chrom=chr1 span=5
1	0
6	100
```
If it is desirable to omit the trailing sequence in the result, the `-ot` or `--omit_tail` option can be used. For example
```
~ $ GC_analysis -i examaple1.fasta -w 5 -s 5 -o without_tail -ot
```
will generate output file `without_tail` with the following content
```
track type=wiggle_0 name="GC percentage" description="chr1"
variableStep chrom=chr1 span=5
1	0
```

3. The program support three output file formats, wiggle, bigwig and gzip compressed wiggle file.
Wiggle output file follows the [UCSC variableStep format definition](https://genome.ucsc.edu/goldenpath/help/wiggle.html). Wiggle file is the default output format. The output format can be changed with `-f` or `--format` option.
```
~ $ GC_analysis -i GRCh38-Chrom17.fasta -w 5 -s 5 -o GRCh38-Chrom17
```
and
```
~ $ GC_analysis -i GRCh38-Chrom17.fasta -w 5 -s 5 -o GRCh38-Chrom17 -f wiggle
```
will generate `GRCh38-Chrom17.wig` as the output file.

```
~ $ GC_analysis -i GRCh38-Chrom17.fasta -w 5 -s 5 -o GRCh38-Chrom17 -f gzip
```
will generate `GRCh38-Chrom17.wig.gz` as the output file. Decompress `GRCh38-Chrom17.wig.gz` will give you the same wiggle file as choosing wiggle as the output format.

```
~ $ GC_analysis -i GRCh38-Chrom17.fasta -w 5 -s 5 -o GRCh38-Chrom17 -f bigwig
```
will generate `GRCh38-Chrom17.bw` as the output file. It should be noted that bigwig format does not allow overlapping bases, which means that `-w 5 -s 3` is an invalid option with choosing bigwig as the output format. In this case, where shift is smaller than window size and bigwig format is specified, the program will generate a wiggle file instead and output a warning message.

```
~ $ GC_analysis -i GRCh38-Chrom17.fasta -w 5 -s 3 -o GRCh38-Chrom17 -f bigwig
WARNING! BigWig file does not allow overlapped items. A wiggle file was generated instead.
```

4. If an output filename is not given, the result will be written to stdout. If the output filename is not given and a file format other than wiggle was chosen, the program will automatically output the result to stdout and give you a warning before and after the result.
Eg. 
```
GC_analysis -i example1.fasta -w 5 -s 3 -f bigwig
WARNING! BigWig file does not allow overlapped items. A wiggle file will be generated instead.
WARNING! An output filename is needed to save output as bigwig. The result is shown below:
track type=wiggle_0 name="GC percentage" description="chr1"
variableStep chrom=chr1 span=5
1       0
4       50
WARNING! BigWig file does not allow overlapped items. A wiggle file was generated instead.
WARNING! An output filename is needed to save output as bigwig. The result is shown above.
```
