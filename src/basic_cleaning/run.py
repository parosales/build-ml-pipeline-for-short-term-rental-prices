#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd
#import pandas_profiling


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    #run = wandb.init(project="nyc_airbnb", group="basic_cleaning", save_code=True)
    logger.info("Download input artifact and load into dataframe")

    local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(local_path)

    #profile = pandas_profiling.ProfileReport(df)
    #profile.to_widgets()

    logger.info("Clean the data")
    # Drop outliers
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    logger.info("Save artifact into W&B")
    df.to_csv(args.output_artifact, index=False)
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(args.output_artifact)
    run.log_artifact(artifact)

    run.finish()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Input artifact from W&B",
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Output artifact to be stored in W&B",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="The type of the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Description of the output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="Minimum price to be considered in the pipeline",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="Maximum price to be considered in the pipeline",
        required=True
    )


    args = parser.parse_args()

    go(args)
