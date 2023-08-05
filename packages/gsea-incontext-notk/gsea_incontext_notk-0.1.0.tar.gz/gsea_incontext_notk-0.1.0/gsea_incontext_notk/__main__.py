
import sys, logging
import argparse as ap


# ------------------------------------
# Main function
# ------------------------------------

# there is a bug in add_argument(required=True), for hacking, don't set metavar='' when required=True,
# or args = argparser.parse_args() will throw bugs!!!


__version__ = '0.9.3'

def main():
    """The Main function/pipeline for gsea_incontext_notk."""

    # Parse options...
    argparser = prepare_argparser()
    args = argparser.parse_args()
    subcommand = args.subcommand_name

    if subcommand == "gsea":
        # compute using gsea_incontext_notk
        from .gsea import GSEA

        gs = GSEA(args.data, args.gmt, args.cls, args.outdir,
                  args.mins, args.maxs, args.n, args.weight,
                  args.type, args.method, args.ascending, args.threads,
                  args.figsize, args.format, args.graph, args.noplot, args.seed, args.verbose)
        gs.run()
    elif subcommand == "prerank":
        from .gsea import Prerank

        pre = Prerank(args.rnk, args.gmt, args.outdir, args.label[0], args.label[1],
                      args.mins, args.maxs, args.n, args.weight, args.ascending, args.threads,
                      args.figsize, args.format, args.graph, args.noplot, args.seed, args.verbose)
        pre.run()

    elif subcommand == "incontext":
        from .gsea import GSEA_InContext

        ic = GSEA_InContext(args.rnk, args.gmt, args.bg_rnks, args.outdir, args.label[0], args.label[1],
                      args.mins, args.maxs, args.n, args.weight, args.ascending, args.threads,
                      args.figsize, args.format, args.graph, args.noplot, args.seed, args.verbose)
        ic.run()

    elif subcommand == "enrichr":
        # calling enrichr API
        from .enrichr import Enrichr
        enr = Enrichr(gene_list= args.gene_list, descriptions=args.descrip, gene_sets=args.library,
                      outdir=args.outdir, format=args.format, cutoff=args.thresh, figsize=args.figsize,
                      top_term=args.term, no_plot=args.noplot, verbose=args.verbose)
        enr.run()
    else:
        argparser.print_help()
        sys.exit(0)


def prepare_argparser():
    """Prepare argparser object. New options will be added in this function first."""
    description = "%(prog)s -- Gene Set Enrichment Analysis in Python"
    epilog = "For command line options of each command, type: %(prog)s COMMAND -h"

    # top-level parser
    argparser = ap.ArgumentParser(description=description, epilog=epilog)
    argparser.add_argument("--version", action="version", version="%(prog)s "+ __version__)
    subparsers = argparser.add_subparsers(dest='subcommand_name') #help="sub-command help")

    # command for 'gsea'
    add_gsea_parser(subparsers)
    # command for 'prerank'
    add_prerank_parser(subparsers)
    # command for 'incontext'
    add_incontext_parser(subparsers)
    # command for 'enrichr'
    add_enrichr_parser(subparsers)

    return argparser

def add_output_option(parser):
    """output option"""

    parser.add_argument("-o", "--outdir", dest="outdir", type=str, default='gsea_incontext_notk_reports',
                        metavar='', action="store", help="The gsea_incontext_notk output directory. Default: the current working directory")
    parser.add_argument("-v", "--verbose", action="store_true", default=False, dest='verbose',
                        help="increase output verbosity, print out progress of your job", )

def add_output_group(parser, required=True):
    """output group"""

    output_group = parser.add_mutually_exclusive_group(required=required)
    output_group.add_argument("-o", "--ofile", dest="ofile", type=str, default='gsea_incontext_notk_reports',
                              help="Output file name. Mutually exclusive with --o-prefix.")
    output_group.add_argument("--o-prefix", dest="ofile", type=str, default='gsea_incontext_notk_reports',
                              help="Output file prefix. Mutually exclusive with -o/--ofile.")



def add_gsea_parser(subparsers):
    """Add main function 'gsea' argument parsers."""

    argparser_gsea = subparsers.add_parser("gsea", help="Main gsea_incontext_notk Function: run gsea_incontext_notk instead of GSEA.")

    # group for input files
    group_input = argparser_gsea.add_argument_group("Input files arguments")
    group_input.add_argument("-d", "--data", dest="data", action="store", type=str, required=True,
                             help="Input gene expression dataset file in txt format.Same with GSEA.")
    group_input.add_argument("-c", "--cls", dest="cls", action="store", type=str, required=True,
                             help="Input class vector (phenotype) file in CLS format. Same with GSEA.")
    group_input.add_argument("-g", "--gmt", dest="gmt", action="store", type=str, required=True,
                             help="Gene set database in GMT format. Same with GSEA.")
    group_input.add_argument("-t", "--permu-type", action="store", dest="type", type=str, metavar='perType',
                             choices=("gene_set", "phenotype"), default="gene_set",
                             help="Permutation type. Same with GSEA, choose from {'gene_set', 'phenotype'}")

    # group for output files
    group_output = argparser_gsea.add_argument_group("Output arguments")
    add_output_option(group_output)

     # group for General options.
    group_opt = argparser_gsea.add_argument_group("GSEA advanced arguments")
    group_opt.add_argument("-n", "--permu-num", dest = "n", action="store", type=int, default=1000, metavar='nperm',
                           help="Number of random permutations. For calculating esnulls. Default: 1000")
    group_opt.add_argument("--min-size",  dest="mins", action="store", type=int, default=15, metavar='int',
                           help="Min size of input genes presented in Gene Sets. Default: 15")
    group_opt.add_argument("--max-size", dest = "maxs", action="store", type=int, default=500, metavar='int',
                           help="Max size of input genes presented in Gene Sets. Default: 500")
    group_opt.add_argument("-w", "--weight", action='store', dest='weight', default=1.0, type=float, metavar='float',
                           help='Weighted_score of rank_metrics.For weighting input genes. Choose from {0, 1, 1.5, 2},default: 1',)
    group_opt.add_argument("-m", "--method", action="store", dest="method", type=str, metavar='',
                           choices=("signal_to_noise", "t_test", "ratio_of_classes", "diff_of_classes", "log2_ratio_of_classes"),
                           default="log2_ratio_of_classes",
                           help="Methods to calculate correlations of ranking metrics. \
                           Choose from {'signal_to_noise', 't_test', 'ratio_of_classes', 'diff_of_classes','log2_ratio_of_classes'}.\
                           Default: 'log2_ratio_of_classes'")
    group_opt.add_argument("-a", "--ascending", action='store_true', dest='ascending', default=False,
                           help='Rank metric sorting order. If the -a flag was chosen, then ascending equals to True. Default: False.')
    group_opt.add_argument("-s", "--seed", dest = "seed", action="store", type=int, default=None, metavar='',
                           help="Number of random seed. Default: None")
    group_opt.add_argument("-p", "--threads", dest = "threads", action="store", type=int, default=1, metavar='procs',
                           help="Number of Processes you are going to use. Default: 1")

    return

def add_prerank_parser(subparsers):
    """Add function 'prerank' argument parsers."""

    argparser_prerank = subparsers.add_parser("prerank", help="Run gsea_incontext_notk Prerank tool on preranked gene list.")

    # group for input files
    prerank_input = argparser_prerank.add_argument_group("Input files arguments")
    prerank_input.add_argument("-r", "--rnk", dest="rnk", action="store", type=str, required=True,
                             help="ranking metric file in .rnk format.Same with GSEA.")
    prerank_input.add_argument("-g", "--gmt", dest="gmt", action="store", type=str, required=True,
                             help="Gene set database in GMT format. Same with GSEA.")
    prerank_input.add_argument("-l", "--label", action='store', nargs=2, dest='label',
                             metavar=('pos', 'neg'), type=str, default=('Pos','Neg'),
                             help="The phenotype label argument need two parameter to define. Default: ('Pos','Neg')")

    # group for output files
    prerank_output = argparser_prerank.add_argument_group("Output arguments")
    add_output_option(prerank_output)

     # group for General options.
    prerank_opt = argparser_prerank.add_argument_group("GSEA advanced arguments")
    prerank_opt.add_argument("-n", "--permu-num", dest = "n", action="store", type=int, default=1000, metavar='nperm',
                             help="Number of random permutations. For calculating esnulls. Default: 1000")
    prerank_opt.add_argument("--min-size",  dest="mins", action="store", type=int, default=15, metavar='int',
                             help="Min size of input genes presented in Gene Sets. Default: 15")
    prerank_opt.add_argument("--max-size", dest = "maxs", action="store", type=int, default=500, metavar='int',
                             help="Max size of input genes presented in Gene Sets. Default: 500")
    prerank_opt.add_argument("-w", "--weight", action='store', dest='weight', default=1.0, type=float, metavar='float',
                             help='Weighted_score of rank_metrics.For weighting input genes. Choose from {0, 1, 1.5, 2},default: 1',)
    prerank_opt.add_argument("-a", "--ascending", action='store_true', dest='ascending', default=False,
                             help='Rank metric sorting order. If the -a flag was chosen, then ascending equals to True. Default: False.')
    prerank_opt.add_argument("-s", "--seed", dest = "seed", action="store", type=int, default=None, metavar='',
                             help="Number of random seed. Default: None")
    prerank_opt.add_argument("-p", "--threads", dest = "threads", action="store", type=int, default=1, metavar='procs',
                           help="Number of Processes you are going to use. Default: 1")

    return

def add_incontext_parser(subparsers):
    """Add function 'incontext' argument parsers."""

    argparser_incontext = subparsers.add_parser("incontext", help="Run GSEA-InContext tool on preranked gene list and background gene lists.")

    # group for input files
    incontext_input = argparser_incontext.add_argument_group("Input files arguments")
    incontext_input.add_argument("-r", "--rnk", dest="rnk", action="store", type=str, required=True,
                             help="ranking metric file in .rnk format.Same with GSEA.")
    incontext_input.add_argument("-r", "--bg_rnks", dest="bg_rnks", action="store", type=str, required=True,
                             help="Single column file with all")
    incontext_input.add_argument("-g", "--gmt", dest="gmt", action="store", type=str, required=True,
                             help="Gene set database in GMT format. Same with GSEA.")
    incontext_input.add_argument("-l", "--label", action='store', nargs=2, dest='label',
                             metavar=('pos', 'neg'), type=str, default=('Pos','Neg'),
                             help="The phenotype label argument need two parameter to define. Default: ('Pos','Neg')")

    # group for output files
    incontext_output = argparser_incontext.add_argument_group("Output arguments")
    add_output_option(incontext_output)

     # group for General options.
    incontext_opt = argparser_incontext.add_argument_group("GSEA-InContext advanced arguments")
    incontext_opt.add_argument("-n", "--permu-num", dest = "n", action="store", type=int, default=1000, metavar='nperm',
                             help="Number of random permutations. For calculating esnulls. Default: 1000")
    incontext_opt.add_argument("--min-size",  dest="mins", action="store", type=int, default=15, metavar='int',
                             help="Min size of input genes presented in Gene Sets. Default: 15")
    incontext_opt.add_argument("--max-size", dest = "maxs", action="store", type=int, default=500, metavar='int',
                             help="Max size of input genes presented in Gene Sets. Default: 500")
    incontext_opt.add_argument("-w", "--weight", action='store', dest='weight', default=1.0, type=float, metavar='float',
                             help='Weighted_score of rank_metrics.For weighting input genes. Choose from {0, 1, 1.5, 2},default: 1',)
    incontext_opt.add_argument("-a", "--ascending", action='store_true', dest='ascending', default=False,
                             help='Rank metric sorting order. If the -a flag was chosen, then ascending equals to True. Default: False.')
    incontext_opt.add_argument("-s", "--seed", dest = "seed", action="store", type=int, default=None, metavar='',
                             help="Number of random seed. Default: None")
    incontext_opt.add_argument("-p", "--threads", dest = "threads", action="store", type=int, default=1, metavar='procs',
                           help="Number of Processes you are going to use. Default: 1")

    return

def add_enrichr_parser(subparsers):
    """Add function 'enrichr' argument parsers."""

    argparser_enrichr = subparsers.add_parser("enrichr", help="Using enrichr API to perform GO analysis.")

    # group for required options.
    enrichr_opt = argparser_enrichr.add_argument_group("Input arguments")
    enrichr_opt.add_argument("-i", "--input-list", action="store", dest="gene_list", type=str, required=True, metavar='geneSymbols',
                              help="Enrichr uses a list of Entrez gene symbols as input.")
    enrichr_opt.add_argument("-g", "--gene-sets", action="store", dest="library", type=str, required=True, metavar='gmt',
                              help="Enrichr library name required. see online tool for library names.")
    enrichr_opt.add_argument("--ds", "--description", action="store", dest="descrip", type=str, default='enrichr', metavar='strings',
                              help="It is recommended to enter a short description for your list so that multiple lists \
                              can be differentiated from each other if you choose to save or share your list.")
    enrichr_opt.add_argument("--cut", "--cut-off", action="store", dest="thresh", metavar='float', type=float, default=0.05,
                              help="Adjust-Pval cutoff, used for generating plots. Default: 0.05.")
    enrichr_opt.add_argument("-t", "--top-term", dest="term", action="store", type=int, default=10, metavar='int',
                              help="Numbers of top terms showed in the plot. Default: 10")
    #enrichr_opt.add_argument("--scale", dest = "scale", action="store", type=float, default=0.5, metavar='float',
    #                          help="scatter dot scale in the dotplot. Default: 0.5")
    # enrichr_opt.add_argument("--no-plot", action='store_true', dest='no_plot', default=False,
    #                           help="Suppress the plot output.This is useful only if data are interested. Default: False.")

    enrichr_output = argparser_enrichr.add_argument_group("Output figure arguments")
    add_output_option(enrichr_output)


    return

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("User interrupted me! ;-) Bye!\n")
        sys.exit(0)
