"""
Calculate gRSCU w/ BioKIT
"""

from pathlib import Path
import subprocess
from typing import Optional

from latch import small_task, workflow
from latch.types import LatchFile

@small_task
def calc_codon_optimization_task(
    cds_file: LatchFile,
    output_file_name: Optional[str],
    ) -> LatchFile:

    ## specify output file name
    # Set output file name
    if not output_file_name:
        gw_rscu_file = Path("gw_rscu.txt").resolve()
    else:
        gw_rscu_file = output_file_name
    

    _biokit_cmd = [
        "biokit",
        "gw_rscu",
        cds_file.local_path
    ]

    with open(gw_rscu_file, "w") as f:
        subprocess.call(_biokit_cmd, stdout=f)

    if not output_file_name:
        return LatchFile(str(gw_rscu_file), f"latch:///{gw_rscu_file.name}")
    else:
        return LatchFile(str(gw_rscu_file), f"latch:///{gw_rscu_file}")

@workflow
def codon_optimization_biokit(
    cds_file: LatchFile,
    output_file_name: Optional[str] = None
    ) -> LatchFile:
    """
    BioKIT gw-RSCU
    ----
    # Codon optimization estimation
    ## About
    Estimates of codon optimization can be used to identify
    genes that are expressed at high levels and are important
    for organismal ecology. Here, we will use the metric
    gRSCU (gene-wise relative synonymous codon usage), which
    is a function in the bioinformatic toolkit
    [BioKIT](https://jlsteenwyk.com/BioKIT),
    to estimate codon optimization.

    ## gRSCU
    gRSCU is calculated by determining the mean or median
    relative synonymous codon usage value for all codons in each
    gene based on their genome-wide values.

    ## Citation
    If you found [BioKIT](https://jlsteenwyk.com/BioKIT) useful,
    please cite *BioKIT: a versatile toolkit for processing and
    analyzing diverse types of sequence data*. Steenwyk et al.
    2021, bioRxiv. doi:
    [10.1101/2021.10.02.462868](https://www.biorxiv.org/content/10.1101/2021.10.02.462868v2.full).

    __metadata__:
        display_name: Estimate gene-wise codon optimization with BioKIT
        author: Jacob L. Steenwyk
            name: Jacob L. Steenwyk
            email: jlsteenwyk@gmail.com
            github: https://github.com/JLSteenwyk
        repository: https://github.com/JLSteenwyk/BioKIT
        license:
            id: MIT
        

    Args:

        cds_file: 
            Input FASTA file of protein coding sequences encoded in a genome
            __metadata__:
                display_name: "Input cds file"
                appearance:
                    comment: "Input cds file"

        output_file_name:
            Outputted file name that contains gRSCU values.
            __metadata__:
                display_name: "Output file with gRSCU values"
                appearance:
					comment: "Output file with gRSCU values"
    """

    return calc_codon_optimization_task(
        cds_file=cds_file,
        output_file_name=output_file_name
    )
