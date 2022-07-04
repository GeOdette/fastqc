"""
Assess the quality of the raw read equence reads.
"""


import subprocess
from pathlib import Path
from typing import Optional

from latch import small_task, workflow
from latch.types import LatchFile, LatchDir
import os


@small_task
def fastqc_task(input_dir: LatchDir, out_dir: LatchDir, nano: bool = False, kmer: Optional[str] = "7") -> LatchDir:

    # passing the files
    file_extensions = ['.fasta', '.fa', '.fastq',
                       '.fq', '.FASTA', '.FA', '.FASTQ', '.FQ', '.gz']
    input_files = [f for f in Path(
        input_dir).iterdir()if f.suffix in file_extensions]
    files = [f.as_posix() for f in input_files]

    # create the output directory
    os.mkdir(Path("fastqc_out"))

    # Command to process fro nanopore fast5 files
    nano_cmd = [
        "fastqc",
        "-kmers",
        str(kmer),
        input_dir.local_path,
        "--outdir",
        str("fastqc_out"),

    ]

    # Writing the command for general run
    _fastqc_rpt = [
        "fastqc",
        "-kmers",
        str(kmer),
        *files,
        "--outdir",
        str("fastqc_out"),

    ]

    if nano == True:
        subprocess.run(nano_cmd, check=True)
    else:
        subprocess.run(_fastqc_rpt, check=True)

    return LatchDir(str("fastqc_out"), out_dir.remote_path)


@workflow
def fastqc(input_dir: LatchDir, out_dir: LatchDir, nano: bool = False, kmer: Optional[str] = "7") -> LatchDir:
    """The latch implementation of fastqc tool to assess the quality of the raw read equence reads.

    FASQC

    ## Basic usage

    Just provide a folder with your input files and create a working directory at the latch console.<br>

    If working with nanopore fast5 files, please check in the __Process FAST5 files from nanopore__ box

    If you wish, you can dictate length of Kmer to look for in the Kmer content module.<br>

    Note: kmers are set to a default of 7

    EXample output<br>

    ![](https://camo.githubusercontent.com/79a3f66d3d0cdcf2b7f89006d556ce9fecb9897c0929eb18a54d7146d1c712c7/687474703a2f2f7777772e62696f696e666f726d61746963732e626162726168616d2e61632e756b2f70726f6a656374732f6661737471632f6661737471632e706e67)

    Note: As at now, there are no official documents to guide interpretation of the reports<br>
    This will be in future releases but you can find a detailed guide [here](https://shiltemann.github.io/wrangling-genomics/00-quality-control/index.html)


    __metadata__:
        display_name: Assess the quality of the raw read equence reads using fastqc

        author:
            name: Geodette

            email: steveodettegeorge@gmail.com

            github:
        repository: https://github.com/GeOdette/fastqc.git

        license:
            id: MIT

    Args:

        input_dir:
          Input directory containing FASTQ files

          __metadata__:
            display_name: Input directory containing FASTQ files

        nano:
          Check box if files come from nanopore sequences and are in fast5 format

          __metadata__:
            display_name: Process FAST5 files from nanopore

        kmer:
          Specify the length of Kmer to look for in the Kmer content module.

          __metadata__:
            display_name: Specify the length of Kmer

        out_dir:
          Output directory containing analyzed files

          __metadata__:
            display_name: Output directory 
    """

    return fastqc_task(input_dir=input_dir, out_dir=out_dir, nano=nano, kmer=kmer)
