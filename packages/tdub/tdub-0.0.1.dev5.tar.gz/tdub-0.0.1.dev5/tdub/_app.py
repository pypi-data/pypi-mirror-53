import argparse
import logging
import json

import dask
from dask.distributed import Client, Lock
from dask.utils import SerializableLock
from dask.dataframe import to_parquet

from tdub.frames import stdregion_dataframes
from tdub.art import run_pulls, run_stacks
from tdub import setup_logging

def parse_args():
    # fmt: off
    parser = argparse.ArgumentParser(prog="tdub", description="tdub CLI")
    subparsers = parser.add_subparsers(dest="action", help="Action")

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("--debug", action="store_true", help="set logging level to debug")

    # regions2parquet = subparsers.add_parser("regions2parquet", help="create parquet output for individual regions", parents=[common_parser])
    # regions2parquet.add_argument("files", type=str, nargs="+", help="input ROOT files")
    # regions2parquet.add_argument("prefix", type=str, help="output file name prefix")
    # regions2parquet.add_argument("-b","--branches", type=str, nargs="+", default=None, help="Branches")
    # regions2parquet.add_argument("-t","--tree-name", type=str, default="WtLoop_nominal", help="ROOT tree name")

    stacks = subparsers.add_parser("stacks", help="create matplotlib stack plots from TRExFitter output", parents=[common_parser])
    stacks.add_argument("workspace", type=str, help="TRExFitter workspace")
    stacks.add_argument("-o", "--out-dir", type=str, help="output directory for plots")
    stacks.add_argument("--lumi", type=str, default="139", help="Integrated lumi. for text")
    stacks.add_argument("--do-postfit", action="store_true", help="produce post fit plots as well")
    stacks.add_argument("--skip-regions", type=str, default=None, help="skip regions based on regex")
    stacks.add_argument("--band-style", type=str, choices=["hatch", "shade"], default="hatch", help="band art")
    stacks.add_argument("--legend-ncol", type=int, choices=[1, 2], default=1, help="number of legend columns")

    pulls = subparsers.add_parser("pulls", help="create matplotlib pull plots from TRExFitter output", parents=[common_parser])
    pulls.add_argument("workspace", type=str, help="TRExFitter workspace")
    pulls.add_argument("config", type=str, help="TRExFitter config")
    pulls.add_argument("-o", "--out-dir", type=str, help="output directory")
    pulls.add_argument("--no-text", action="store_true", help="don't print values on plots")

    optimize = subparsers.add_parser("optimize", help="Gaussian processes minimization for HP optimization")
    optimize.add_argument("region", type=str, help="Region to train")
    optimize.add_argument("nlomethod", type=str, help="NLO method samples to use", choices=["DR", "DS", "Both"])
    optimize.add_argument("datadir", type=str, help="Directory with ROOT files")
    optimize.add_argument("-o", "--out-dir", type=str, default="_optim", help="output directory for saving optimizatin results")
    optimize.add_argument("-n", "--n-calls", type=int, default=15, help="number of calls for the optimization procedure")
    optimize.add_argument("-r", "--esr", type=int, default=20, help="early stopping rounds for the training")

    fold = subparsers.add_parser("fold", help="Perform a folded training")
    fold.add_argument("optimdir", type=str, help="directory containing optimization information")
    fold.add_argument("datadir", type=str, help="Directory with ROOT files")
    fold.add_argument("-o", "--out-dir", type=str, default="_folded", help="output directory for saving optimizatin results")
    fold.add_argument("-s", "--seed", type=int, default=414, help="random seed for folding")
    fold.add_argument("-n", "--n-splits", type=int, default=3, help="number of splits for folding")

    # fmt: on
    return (parser.parse_args(), parser)


# def _parquet_regions(args, log):
#     import numexpr

#     numexpr.set_num_threads(1)
#     frames = stdregion_dataframes(args.files, args.tree_name, args.branches)
#     log.info("Executing queries:")
#     for k, v in frames.items():
#         log.info(f"  - {v.name}: {v.selection}")
#     for region, frame in frames.items():
#         name = region.name
#         output_name = f"{args.prefix}_{name}.parquet"
#         log.info(f"saving one at a time ({output_name})")
#         to_parquet(frame.df, output_name, engine="auto")
#     return 0


def _optimize(args):
    from tdub.train import gp_minimize_auc

    return gp_minimize_auc(
        args.region,
        args.nlomethod,
        args.datadir,
        output_dir=args.out_dir,
        n_calls=args.n_calls,
        esr=args.esr,
    )


def _foldedtraining(args):
    from tdub.train import folded_training, prepare_from_root
    from tdub.utils import quick_files

    with open(f"{args.optimdir}/summary.json", "r") as f:
        summary = json.load(f)
    nlo_method = summary["nlo_method"]
    qfiles = quick_files(f"{args.datadir}")
    if nlo_method == "DR":
        tW_files = qfiles["tW_DR"]
    elif nlo_method == "DS":
        tW_files = qfiles["tW_DS"]
    elif nlo_method == "Both":
        tW_files = qfiles["tW_DR"] + qfiles["tW_DS"]
        tW_files.sort()
    else:
        raise ValueError("nlo_method must be 'DR' or 'DS' or 'Both'")

    X, y, w, cols = prepare_from_root(tW_files, qfiles["ttbar"], summary["region"])
    folded_training(
        X,
        y,
        w,
        cols,
        summary["best_params"],
        {"verbose": 20},
        args.out_dir,
        kfold_kw={"n_splits": args.n_splits, "shuffle": True, "random_state": args.seed},
    )
    return 0


def cli():
    args, parser = parse_args()
    if args.action is None:
        parser.print_help()
        return 0

    setup_logging()
    log = logging.getLogger("tdub.cli")

    if args.action == "regions2parquet":
        return _parquet_regions(args, log)
    elif args.action == "stacks":
        return run_stacks(args)
    elif args.action == "pulls":
        return run_pulls(args)
    elif args.action == "optimize":
        return _optimize(args)
    elif args.action == "fold":
        return _foldedtraining(args)
    else:
        parser.print_help()
