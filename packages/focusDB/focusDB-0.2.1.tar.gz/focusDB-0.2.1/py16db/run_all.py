#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import subprocess
import random
import shutil
import gzip
import logging
import glob

from pathlib import Path
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

from py16db.run_sickle import run_sickle

from . import __version__
from py16db.FocusDBData import FocusDBData,fasterqdumpError

class bestreferenceError(Exception):
    pass


class downsamplingError(Exception):
    pass


class riboSeedError(Exception):
    pass


class riboSeedUnsuccessfulError(Exception):
    """ its not magic, this "error" is for when riboSeed
    finishes, but cant improve on assembly
    """
    pass


class extracting16sError(Exception):
    pass


def setup_logging(args):  # pragma: nocover
    if (args.verbosity * 10) not in range(10, 60, 10):
        raise ValueError('Invalid log level: %s' % args.verbosity)
    logging.basicConfig(
        level=logging.DEBUG,
        filename=os.path.join(args.output_dir, "focusDB.log"),
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    console_err = logging.StreamHandler(sys.stderr)
    console_err.setLevel(level=(args.verbosity * 10))
    console_err_format = logging.Formatter(
        str("%(asctime)s \u001b[3%(levelname)s\033[1;0m  %(message)s"),
        "%H:%M:%S")
    console_err.setFormatter(console_err_format)
    logging.addLevelName(logging.DEBUG,    "4m --")
    logging.addLevelName(logging.INFO,     "2m ==")
    logging.addLevelName(logging.WARNING,  "3m !!")
    logging.addLevelName(logging.ERROR,    "1m xx")
    logging.addLevelName(logging.CRITICAL, "1m XX")
    logger.addHandler(console_err)
    return logger


def get_args():  # pragma: nocover
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output_dir",
                        help="path to output", required=True)
    parser.add_argument("-n", "--organism_name",
                        help="genus or genus species in quotes",
                        required=True)
    parser.add_argument("--SRA_list",
                        help="path to file containing list of sras " +
                        "for assembly[one column]",
                        required=False)
    parser.add_argument("--version", action='version',
                        version='%(prog)s {version}'.format(
                            version=__version__))
    parser.add_argument("-l", "--approx_length",
                        help="Integer for approximate genome length",
                        required=False, type=int)
    parser.add_argument("--sraFind_path", dest="sra_path",
                        help="path to sraFind file; default is in .focusDB/",
                        default=None,
                        required=False)
    parser.add_argument("--focusDB_data", dest="focusDB_data",
                        help="path to data storage area; default .focusDB/",
                        default=None)
    parser.add_argument("--SRAs", default=None, nargs="+",
                        help="run pipeline on this (these) SRA(s) only",
                        required=False)
    parser.add_argument("-g", "--genomes_dir",
                        help="path to directory containing, or empty, " +
                        "candidate genomes for reference",
                        required=True)
    #  Note that this agument doesn't get called, but is inheirited by get_n_genomes
    parser.add_argument("-p", "--prokaryotes", action="store",
                        help="path_to_prokaryotes.txt",
                        default="./prokaryotes.txt",
                        required=False)
    parser.add_argument("-S", "--n_SRAs", help="max number of SRAs to be run",
                        type=int, required=False)
    parser.add_argument("-R", "--n_references",
                        help="max number of reference strains to consider. " +
                        "default (0) is download all",
                        type=int, required=False, default=0)
    parser.add_argument("--get_all",
                        help="if a biosample is associated with " +
                        "multiple libraries, default behaviour is to " +
                        "download the first only.  Use --get_all to " +
                        "analyse each library",
                        action="store_true", required=False)
    parser.add_argument("--cores",
                        help="integer for how many cores you wish to use",
                        default=1,
                        required=False, type=int)
    parser.add_argument("--threads",
                        action="store",
                        default=1, type=int,
                        choices=[1, 2, 4],
                        help="if your cores are hyperthreaded, set number" +
                        " threads to the number of threads per processer." +
                        "If unsure, see 'cat /proc/cpuinfo' under 'cpu " +
                        "cores', or 'lscpu' under 'Thread(s) per core'." +
                        ": %(default)s")
    parser.add_argument("--maxcov",
                        help="integer for maximum coverage of reads",
                        default=50,
                        required=False, type=int)
    parser.add_argument("--example_reads",
                        help="input of example reads", nargs='+',
                        required=False, type=str)
    parser.add_argument("--redo_assembly", action="store_true",
                        help="redo the assembly step, ignoring status file")
    parser.add_argument("--subassembler",
                        help="which program should riboseed " +
                        "use for sub assemblies",
                        choices=["spades", "skesa"],
                        required=False, default="spades")
    # this is needed for plentyofbugs, should not be user set
    parser.add_argument("--nstrains", help=argparse.SUPPRESS,
                        type=int, required=False)
    parser.add_argument("--memory",
                        help="amount of RAM to be used",
                        default=4,
                        required=False, type=int)
    parser.add_argument("--seed",
                        help="random seed for subsampling referencese",
                        type=int, default=12345)
    parser.add_argument("-v", "--verbosity", dest='verbosity',
                        action="store",
                        default=2, type=int, choices=[1, 2, 3, 4, 5],
                        help="Logger writes debug to file in output dir; " +
                        "this sets verbosity level sent to stderr. " +
                        " 1 = debug(), 2 = info(), 3 = warning(), " +
                        "4 = error() and 5 = critical(); " +
                        "default: %(default)s")
    args = parser.parse_args()
    # plentyofbugs uses args.nstrains, but wecall it args.n_references for clarity
    args.nstrains = args.n_references
    if args.SRAs is None:
        if args.n_SRAs is None:
            print("if not running with --SRAs, " +
                  "then --n_SRAs must be provided!")
            sys.exit(1)
    return(args)


def check_programs(logger):
    """exits if the following programs are not installed"""

    required_programs = [
        "ribo", "barrnap", "fasterq-dump", "mash",
        "skesa", "plentyofbugs", "iqtree"]
    for program in required_programs:
        if shutil.which(program) is None:
            logger.critical('%s is not installed: exiting.', program)
            sys.exit(1)


def parse_status_file(path):
    # because downloading and assembling can fail for many reasons,
    # we write out status to a file.  this allows for easier restarting of
    # incomplete runs
    if not os.path.exists(path):
        return []
    statuses = []
    with open(path, "r") as statusfile:
        for line in statusfile:
            statuses.append(line.strip())
    return(statuses)


def update_status_file(path, to_remove=[], message=None):
    assert isinstance(to_remove, list)
    statuses = parse_status_file(path)
    # dont try to remove empty files
    if statuses != []:
        os.remove(path)
    # just for cleaning up status file
    if message is not None:
        statuses.append(message)
    # write out non-duplicated statuses
    with open(path, "w") as statusfile:
        for status in set(statuses):
            if status not in to_remove:
                statusfile.write(status + "\n")


def filter_SRA(sraFind, organism_name, strains, get_all, thisseed, logger):
    """sraFind [github.com/nickp60/srafind], contains"""
    results = []
    with open(sraFind, "r") as infile:
        for line in infile:
            split_line = [x.replace('"', '').replace("'", "") for x
                          in line.strip().split("\t")]
            if split_line[11].startswith(organism_name):
                if split_line[8].startswith("ILLUMINA"):
                    results.append(split_line[17])
    random.seed(thisseed)
    random.shuffle(results)

    if strains != 0:
        results = results[0:strains]
        logger.debug('Found SRAs: %s', results)

    sras = []
    for result in results:
        these_sras = result.split(",")
        if get_all:
            for sra in these_sras:
                sras.append(sra)
        else:
            sras.append(these_sras[0])

    return(sras)


def sralist(list):
    """ takes a file list of  of SRAs, return list
    for if you wish to use SRAs that are very recent and ahead of sraFind
    """
    sras = []
    with open(list, "r") as infile:
        for sra in infile:
            sras.append(sra.strip())
    return sras


def pob(genomes_dir, readsf, output_dir, logger):
    """use plentyofbugs to identify best reference
    Uses plentyofbugs, a package that useqs mash to
    find the best reference genome for draft genome
    """
    pobcmd = str("plentyofbugs -g {genomes_dir} -f {readsf} -o {output_dir} " +
                 "--downsampling_ammount 1000000").format(**locals())
    logger.info('Finding best reference genome: %s', pobcmd)

    for command in [pobcmd]:
        logger.debug(command)
        try:
            subprocess.run(command,
                           shell=sys.platform != "win32",
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           check=True)
            best_ref = os.path.join(output_dir, "best_reference")
        except:
            raise bestreferenceError("Error running the following command: %s" %
                                     command)

    with open(best_ref, "r") as infile:
        for line in infile:
            sraacc = line.strip().split('\t')
            sim = float(sraacc[1])
            ref = sraacc[0]
            logger.debug("Reference genome mash distance: %s", sim)

            length_path = os.path.join(output_dir, "genome_length")
            cmd = "wc -c {ref} > {length_path}".format(**locals())
            subprocess.run(cmd,
                           shell=sys.platform != "win32",
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           check=True)
            return(ref, sim)


def check_rDNA_copy_number(ref, output, logger):
    """ensure reference has multiple rDNAs
    Using barrnap to check that there are multiple rDNA copies in the reference genome
    """
    os.makedirs(os.path.join(output, "barrnap_reference"), exist_ok=True)
    barroutput = os.path.join(output, "barrnap_reference",
                              os.path.basename(ref) + ".gff")
    cmd = "barrnap {ref} > {barroutput}".format(**locals())
    subprocess.run(cmd,
                   shell=sys.platform != "win32",
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE,
                   check=True)
    rrn_num = 0
    with open(barroutput, "r") as rrn:
        for rawline in rrn:
            line = rawline.strip().split('\t')
            if line[0].startswith("##"):
                continue
            if line[8].startswith("Name=16S"):
                rrn_num += 1
    return rrn_num


def get_and_check_ave_read_len_from_fastq(fastq1, minlen, maxlen, logger=None):
    """return average read length in fastq1 file from first N reads
    from LP: taken from github.com/nickp60/riboSeed/riboSeed/classes.py;
    """
    count, tot = 0, 0
    if os.path.splitext(fastq1)[-1] in ['.gz', '.gzip']:
        open_fun = gzip.open
    else:
        open_fun = open
    with open_fun(fastq1, "rt") as file_handle:
        data = SeqIO.parse(file_handle, "fastq")
        logger.debug("Obtaining average read length from first 30 reads")
        for read in data:
            count += 1
            tot += len(read)
            if count == 30:
                break

    ave_read_len = float(tot / 30)
    if ave_read_len < minlen:
        logger.error("Average read length is too short: %s; skipping...",
                     ave_read_len)
        return (1, ave_read_len)
    if ave_read_len > maxlen:
        logger.critical("Average read length is too long: %s; skipping...",
                        ave_read_len)
        return (2, ave_read_len)
    logger.debug("Average read length: %s", ave_read_len)
    return (0, ave_read_len)


def get_coverage(read_length, approx_length, fastq1, fastq2, logger):
    """Obtains the coverage for a read set given the estimated genome size"""

    if os.path.splitext(fastq1)[-1] in ['.gz', '.gzip']:
        open_fun = gzip.open
    else:
        open_fun = open
    logger.debug("Counting reads")

    with open_fun(fastq1, "rt") as data:
        for count, line in enumerate(data):
            pass

    if fastq2 is not None:
        read_length = read_length * 2

    coverage = float((count * read_length) / (approx_length * 4))
    logger.info('Read coverage: %sx', round(coverage, 1))
    return(coverage)


def downsample(read_length, approx_length, fastq1, fastq2,
               maxcoverage, destination, logger, run):
    """downsample for optimal assembly
    Given the coverage from coverage(), downsamples the reads if over
    the max coverage set by args.maxcov. Default 50.
    """

    suboutput_dir_downsampled = destination
    downpath1 = os.path.join(suboutput_dir_downsampled,
                             "downsampledreadsf.fastq")
    downpath2 = None
    if fastq2 is not None:
        downpath2 = os.path.join(suboutput_dir_downsampled,
                                 "downsampledreadsr.fastq")
    coverage = get_coverage(read_length, approx_length,
                            fastq1, fastq2, logger=logger)
    covfraction = round(float(maxcoverage / coverage), 3)
    downcmd =  "seqtk sample -s100 {fastq1} {covfraction} > {downpath1}".format(**locals())
    downcmd2 = "seqtk sample -s100 {fastq2} {covfraction} > {downpath2}".format(**locals())
    # at least downsample the forward/single reads, but add the
    # other command if using paired reads
    commands = [downcmd]
    if (coverage > maxcoverage):
        if run:
            os.makedirs(suboutput_dir_downsampled)
            logger.info('Downsampling to %s X coverage', maxcoverage)
            if fastq2 is not None:
                commands.append(downcmd2)
            for command in commands:
                try:
                    logger.debug(command)
                    subprocess.run(command,
                                   shell=sys.platform != "win32",
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   check=True)
                except:
                    raise downsamplingError("Error running following command ", command)
        return(downpath1, downpath2)
    else:
        logger.info('Skipping downsampling as max coverage is < %s', maxcoverage)
        return(fastq1, fastq2)


def make_riboseed_cmd(sra, readsf, readsr, cores, subassembler, threads,
                      output, memory, logger):
    """Runs riboSeed to reassemble reads """
    if memory < 10:
        serialize = "--serialize "
    else:
        serialize = ""
    cmd = str("ribo run -r {sra} -F {readsf} -R {readsr} --cores {cores} " +
              "--threads {threads} -v 1 -o {output} {serialize}" +
              "--subassembler {subassembler} --just_seed " +
              "--memory {memory}").format(**locals())

    if readsr is None:
        cmd = str("ribo run -r {sra} -S1 {readsf} --cores {cores} " +
                  "--threads {threads} -v 1 -o {output} {serialize}" +
                  "--subassembler {subassembler} --just_seed " +
                  "--memory {memory}").format(**locals())
    return(cmd)


def process_strain(rawreadsf, rawreadsr, read_length, this_output, args, logger, status_file):
    pob_dir = os.path.join(this_output, "plentyofbugs")
    ribo_dir = os.path.join(this_output, "riboSeed")
    sickle_out = os.path.join(this_output, "sickle")
    best_reference = os.path.join(pob_dir, "best_reference")

    # Note thhat the status file is checked before each step.
    # If a failure occured, all future steps are rerrun
    # for instance, if trimming has been done, but downsample hasn't,
    # downsampling and assembly will be run. This is to protectt against
    # files sticking around when they shouldn't
    if not os.path.exists(best_reference):
        pob(genomes_dir=args.genomes_dir, readsf=rawreadsf,
            output_dir=pob_dir, logger=logger)

    with open(best_reference, "r") as infile:
        for line in infile:
            best_ref_fasta=line.split('\t')[0]

    if args.approx_length is None:
        genome_length=os.path.join(pob_dir, "genome_length")
        with open(genome_length, "r") as infile:
            for line in infile:
                approx_length = float(line.split()[0])
                logger.debug("Using genome length: %s", approx_length)
    else:
        approx_length = args.approx_length
    if "TRIMMED" not in parse_status_file(status_file):
        logger.info('Quality trimming reads')
        update_status_file(status_file,
                           to_remove=["DOWNSAMPLED", "RIBOSEED COMPLETE"])
        if os.path.exists(sickle_out):
            shutil.rmtree(sickle_out)
    trimmed_fastq1, trimmed_fastq2 = run_sickle(
        fastq1=rawreadsf,
        fastq2=rawreadsr,
        output_dir=sickle_out,
        run="TRIMMED" not in parse_status_file(status_file))
    update_status_file(status_file, message="TRIMMED")
    logger.debug('Quality trimmed f reads: %s', trimmed_fastq1)
    logger.debug('Quality trimmed r reads: %s', trimmed_fastq2)

    logger.debug('Downsampling reads')
    if "DOWNSAMPLED" not in parse_status_file(status_file):
        update_status_file(status_file, to_remove=["RIBOSEED COMPLETE"])
        if os.path.exists(os.path.join(this_output, "downsampled")):
            shutil.rmtree(os.path.join(this_output, "downsampled"))
    downsampledf, downsampledr = downsample(
        approx_length=approx_length,
        fastq1=trimmed_fastq1,
        fastq2=trimmed_fastq2,
        maxcoverage=args.maxcov,
        destination=os.path.join(this_output, "downsampled"),
        read_length=read_length,
        logger=logger,
        run="DOWNSAMPLED" not in parse_status_file(status_file))
    update_status_file(status_file, message="DOWNSAMPLED")
    logger.debug('Downsampled f reads: %s', downsampledf)
    logger.debug('Downsampled r reads: %s', downsampledr)
    riboseed_cmd = make_riboseed_cmd(sra=best_ref_fasta, readsf=downsampledf,
                                     readsr=downsampledr, cores=args.cores,
                                     memory=args.memory,
                                     subassembler=args.subassembler,
                                     threads=args.threads, output=ribo_dir,
                                     logger=logger)
    # do we want to redo the assembly?
    if args.redo_assembly:
        update_status_file(status_file, to_remove=["RIBOSEED COMPLETE"])
    # file that will contain riboseed contigs
    ribo_contigs = os.path.join(this_output, "riboSeed", "seed",
                                "final_long_reads", "riboSeedContigs.fasta")
    if "RIBOSEED COMPLETE" not in parse_status_file(status_file):
        if os.path.exists(ribo_dir):
            shutil.rmtree(ribo_dir)
        try:
            logger.info("Running riboSeed")
            logger.debug(riboseed_cmd)
            subprocess.run(riboseed_cmd,
                           shell=sys.platform != "win32",
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           check=True)

            update_status_file(status_file, message="RIBOSEED COMPLETE")
        except Exception as e:
            logger.error(e)
            raise riboSeedError("Error running the following command: %s" %
                                riboseed_cmd)
    else:
        logger.info("Skipping riboSeed")
    # check for the files to see if riboSeed completed
    if os.path.exists(ribo_contigs):
        update_status_file(status_file, message="RIBOSEED COMPLETE")
    else:
        raise riboSeedUnsuccessfulError(
            "riboSeed completed but was not successful; for details, see log file at %s" %
            os.path.join(this_output, "riboSeed", "run_riboSeed.log"))


def run_barrnap(assembly,  results, logger):
    barrnap = "barrnap {assembly} > {results}".format(**locals())
    logger.debug('Identifying 16S sequences with barnap: %s', barrnap)
    try:
        subprocess.run(barrnap,
                       shell=sys.platform != "win32",
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       check=True)
    except:
        raise extracting16sError(
            "Error running the following command %s" % barrnap)


def extract_16s_from_assembly(assembly, gff, sra, output, args, logger):
    results16s = {}  # [sra_#, chromosome, start, end, reverse complimented]
    nseqs = 0
    with open(gff, "r") as rrn, open(output, "a") as outf:
        rrn_num = 0
        for rawline in rrn:
            line = rawline.strip().split('\t')
            # need this: catches index errors
            if line[0].startswith("##"):
                pass
            elif line[8].startswith("Name=16S"):
                rrn_num = rrn_num + 1
                if line[6] == "-":
                    suffix = 'chromosome-RC@'
                else:
                    suffix = ''
                chrom = line[0]
                ori = line[6]
                start = int(line[3])
                end = int(line[4])
                thisid = "{}_{}".format(sra, rrn_num)
                results16s[thisid] = [chrom, start, end, line[6]]
                with open(assembly, "r")  as asmb:
                    for rec in SeqIO.parse(asmb, "fasta"):
                        if rec.id == chrom:
                            seq = rec.seq[start + 1: end + 1]
                            if ori == "-":
                                seq = seq.reverse_complement()
                            thisdesc = "{chrom}:{start}:{end}({ori})".format(**locals())
                            SeqIO.write(SeqRecord(seq, id=thisid, description=thisdesc), outf,  "fasta")
                            nseqs = nseqs + 1

    return nseqs


def write_pass_fail(args, stage, status, note):
    """
    format fail messages in tabular fomat:
    organism\tstage\tmessage
    """
    path = os.path.join(args.output_dir, "SUMMARY")
    org = args.organism_name
    with open(path, "a") as failfile:
        failfile.write("{}\t{}\t{}\t{}\n".format(org, status, stage, note))


def our_get_n_genomes(args, logger):
    # taken from the main function of get_n_genomes
    if not os.path.exists(args.prokaryotes):
        gng.fetch_prokaryotes(dest=args.prokaryotes)
    org_lines = gng.get_lines_of_interest_from_proks(path=args.prokaryotes,
                                                     org=args.organism_name)
    if len(org_lines) == 0:
        return 1
    if args.nstrains == 0:
        nstrains = len(org_lines)
    else:
        nstrains = args.nstrains
    print(nstrains)
    cmds = gng.make_fetch_cmds(
        org_lines,
        nstrains=nstrains,
        thisseed=args.seed,
        genomes_dir=args.genomes_dir,
        SHUFFLE=True)
    print(cmds)
    # this can happen if tabs end up in metadata (see
    # AP019724.1 B. unifomis, and others
    # I updated plentyofbugs to try to catch it, but still might happen
    if len(cmds) == 0:
        return 1
    try:
        for i, cmd in enumerate(cmds):
            sys.stderr.write("Downloading genome %i of %i\n%s\n" %(i + 1, len(cmds), cmd))
            logger.debug(cmd)
            subprocess.run(
                cmd,
                shell=sys.platform != "win32",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True)
    except Exception as e:
        logger.error(e)
        return 2

    unzip_cmd = "gunzip " + os.path.join(args.genomes_dir, "*.gz")
    sys.stderr.write(unzip_cmd + "\n")
    try:
        subprocess.run(
            unzip_cmd,
            shell=sys.platform != "win32",
            check=True)
    except Exception as e:
        logger.error(e)
        return 3
    return 0


def decide_skip_or_download_genomes(args, logger):
    """ checks the genomes dir
    returns
    - 0 if all is well
    - 1 if no matching genomes in prokaryotes.txt
    - 2 if error downloading
    - 3 if error unzipping
    """
    # check basic integrity of genomes dir
    # it might exist, but making it here simplifies the control flow later
    # it seems counter intuitive, but checking if the dir we might have just
    # created is easier than checking if it exists/is intact twice
    os.makedirs(args.genomes_dir, exist_ok=True)
    if len(glob.glob(os.path.join(args.genomes_dir, "*.fna"))) == 0:
        logger.info('Downloading genomes')
        return(our_get_n_genomes(args, logger))
    if len(glob.glob(os.path.join(args.genomes_dir, "*.fna.gz"))) != 0:
        logger.warning('Genome downloading may have been interupted; ' +
                       'downloading fresh')
        shutil.rmtree(args.genomes_dir)
        os.makedirs(args.genomes_dir)
        return(our_get_n_genomes(args, logger))
    return 0


def get_focusDB_dir(args):
    if args.focusDB_data is None:
        return os.path.join(os.path.expanduser("~"), ".focusDB", "")
    else:
        return args.args.focusDB_data


def main():
    args = get_args()

    genomesdir = os.path.join(args.genomes_dir, "")

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    if os.path.exists(os.path.join(args.output_dir, "SUMMARY")):
        os.remove(os.path.join(args.output_dir, "SUMMARY"))

    logger = setup_logging(args)
    logger.info("Processing %s", args.organism_name)
    logger.info("Usage:\n{0}\n".format(" ".join([x for x in sys.argv])))
    logger.debug("All settings used:")
    for k,v in sorted(vars(args).items()):
        logger.debug("{0}: {1}".format(k,v))
    check_programs(logger)
    # set up the data object
    fDB = FocusDBData(dbdir = get_focusDB_dir(args))
    fDB.fetch_sraFind_data(dest_path=args.sra_path, logger=logger)

    if args.SRAs is not None:
        filtered_sras = args.SRAs
    elif args.SRA_list is not None:
        filtered_sras = sralist(list=args.SRA_list)
    else:
        filtered_sras = filter_SRA(
            sraFind=fDB.sraFind_data,
            organism_name=args.organism_name,
            strains=args.n_SRAs,
            thisseed=args.seed,
            logger=logger,
            get_all=args.get_all)

    sra_num = len(filtered_sras)
    if filtered_sras == []:
        if args.example_reads is None:
            logger.critical('No SRAs found on NCBI by sraFind')
            write_pass_fail(
                args, status="FAIL",
                stage="global",
                note="No SRAs available")
            sys.exit(1)

    pob_result = decide_skip_or_download_genomes(args, logger)
    if pob_result != 0:
        if pob_result == 1:
            message = "No available references"
        elif pob_result == 2:
            message ="Error downloading genome from NCBI"
        elif pob_result == 3:
            message ="Error unzipping genomes; delete directory and try again"
        else:
            pass
        logger.critical(message)
        write_pass_fail(args, status="FAIL", stage="global", note=message)
        sys.exit(1)

    if not os.path.exists(os.path.join(args.genomes_dir, ".references_passed_checks")):
        logger.info("checking reference genomes for rDNA counts")
        for potential_reference in glob.glob(os.path.join(args.genomes_dir, "*.fna")):
            rDNAs = check_rDNA_copy_number(ref=potential_reference,
                                           output=args.genomes_dir,
                                           logger=logger)
            if rDNAs < 2:
                logger.warning(
                    "reference %s does not have multiple rDNAs; excluding", potential_reference)
                os.remove(potential_reference)
        with open(os.path.join(args.genomes_dir, ".references_passed_checks"), "w") as statusfile:
            statusfile.write("References have been checked\n")
    else:
        logger.debug("Already checked reference genomes")
    if len(glob.glob(os.path.join(args.genomes_dir, "*.fna"))) == 0:
        logger.critical("No usable reference genome found!")
        write_pass_fail(args, status="FAIL",
                        stage="global",
                        note="No references had more than 1 rDNA")
    # data_dirs = []
    if args.example_reads is not None:
        this_output = os.path.join(args.output_dir, "example", "")
        # data_dirs.append(this_output)
        status_file = os.path.join(this_output, "example", "")
        if os.path.exists(this_output):
            logger.warning("using existing output directory")
        os.makedirs(this_output)
        rawreadsf = args.example_reads[0]
        try:
            rawreadsr = args.example_reads[1]
        except IndexError:
            rawreadsr = None
        read_len_status, read_length = get_and_check_ave_read_len_from_fastq(
            minlen=65,
            maxlen=301,
            fastq1=rawreadsf,
            logger=logger)
        if read_len_status != 0:
            if read_len_status == 1:
                message = "Reads were shorter than 65bp threshold"
            else:
                message = "Reads were longer than 300bp threshold"
            write_pass_fail(args, status="FAIL",
                            stage="examplereads",
                            note=message)
            logger.error(message)
            sys.exit(1)

        process_strain(rawreadsf, rawreadsr, read_length,this_results, args, logger, status_file)

    else:
        for i, accession in enumerate(filtered_sras):
            this_output = os.path.join(args.output_dir, accession)
            this_data = os.path.join(get_focusDB_dir(), "data")
            this_results = os.path.join(this_output, "results")
            os.makedirs(this_output, exist_ok=True)
            status_file = os.path.join(this_output, "status")
            logger.info("Organism: %s", args.organism_name)
            try:
                rawreadsf, rawreadsr, download_error_message = \
                    fDB.get_SRA_data(
                        cores=args.cores,
                        SRA=accession,
                        logger=logger)
            except fasterqdumpError:
                message =  'Error downloading %s'  % accession
                write_pass_fail(args, status="FAIL", stage=accession, note=message)
                logger.error(message)
                continue
            if download_error_message is not  "":
                write_pass_fail(args, status="FAIL", stage=accession,
                                note=download_error_message)
                logger.error(
                    "Error either downloading or parsing the file " +
                    "name for this accession.")
                logger.error(this_data)
                logger.error(download_error_message)
                continue
            read_len_status, read_length = get_and_check_ave_read_len_from_fastq(
                minlen=65,
                maxlen=301,
                fastq1=rawreadsf, logger=logger)
            if read_len_status != 0:
                if read_len_status == 1:
                    message = "Reads were shorter than 65bp threshold"
                else:
                    message = "Reads were longer than 300bp threshold"
                write_pass_fail(args, status="FAIL", stage=accession, note=message)
                logger.error(message)
                continue

            try:
                process_strain(rawreadsf, rawreadsr, read_length,this_results, args,  logger, status_file)

            except subprocess.CalledProcessError:
                write_pass_fail(args, status="FAIL",
                                stage=accession,
                                note="Unknown failure")
                logger.error('Unknown subprocess error')
                continue
            except bestreferenceError as e:
                write_pass_fail(args, status="FAIL",
                                stage=accession,
                                note="Unknown error selecting reference")
                logger.error(e)
                continue
            except downsamplingError as e:
                write_pass_fail(args, status="FAIL",
                                stage=accession,
                                note="Unknown error downsampling")
                logger.error(e)
                continue
            except riboSeedError as e:
                write_pass_fail(args, status="FAIL",
                                stage=accession,
                                note="Unknown failure running riboSeed")
                logger.error(e)
                continue
            except riboSeedUnsuccessfulError as e:
                write_pass_fail(args, status="FAIL",
                                stage=accession,
                                note="riboSeed unsuccessful")
                logger.error(e)
                continue

            except extracting16sError as e:
                write_pass_fail(args, status="FAIL",
                                stage=accession,
                                note="Unknown error extracting 16s sequences")
                logger.error(e)
                continue
            write_pass_fail(args, status="PASS", stage=accession, note="")

    all_assemblies  =  glob.glob(
        os.path.join(args.output_dir, "*", "results", "riboSeed",
                     "seed", "final_long_reads", "riboSeedContigs.fasta"))
    ###########################################################################
    extract16soutput = os.path.join(
        args.output_dir,
        "{}_ribo16s.fasta".format(args.organism_name.replace(" ", "_")))
    if os.path.exists(extract16soutput):
        os.remove(extract16soutput)

    n_extracted_seqs = 0
    for assembly in all_assemblies:
        sra = str(Path(assembly).parents[4].name)
        barr_gff = os.path.join(args.output_dir, sra, "barrnap.gff")
        try:
            run_barrnap(assembly,  barr_gff, logger)
            this_extracted_seqs = extract_16s_from_assembly(
                assembly, barr_gff, sra, extract16soutput, args, logger)
            n_extracted_seqs  = n_extracted_seqs + this_extracted_seqs
        except extracting16sError as e:
            write_pass_fail(args, status="FAIL", stage=sra,
                note="Error running barrnap")

    ###########################################################################
    logger.info("Wrote out %i sequences", n_extracted_seqs)
    if n_extracted_seqs == 0:
        write_pass_fail(args, status="FAIL", stage="global",
                        note="No 16s sequences detected in re-assemblies")
        logger.warning("No 16s sequences recovered. exiting")
        sys.exit()
    write_pass_fail(args, status="PASS", stage="global", note="")
    sys.exit()


if __name__ == '__main__':
    main()
