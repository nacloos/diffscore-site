from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from diffscore import Dataset
from diffscore.analysis.decoding import decoder_logistic


def neural_data_decoding_accuracy(dataset_id):
    dataset = Dataset(dataset_id)

    if isinstance(dataset, tuple):
        X, conditions = dataset
    else:
        X = dataset

    decoder = decoder_logistic

    labels = conditions[0].keys()
    assert len(labels) == 1, "Only one label is supported for now"

    ref_acc_results = {}
    for label in labels:
        cond = [c[label] for c in conditions]

        ref_acc = decoder(X, cond)["score"]
        ref_acc = np.mean(ref_acc)  # mean over time dimension
        print("Reference accuracy for label", label, ":", ref_acc)

        ref_acc_results[label] = ref_acc

    mean_ref_acc = np.mean(list(ref_acc_results.values()))
    print("Mean reference accuracy:", mean_ref_acc)
    return mean_ref_acc


if __name__ == "__main__":
    data_dir = Path(__file__).parent / "data" / "benchmarks"

    # measures to plot
    measures = [
        "cka",
        "nbs",
        "procrustes-angular-score",
        "ridge-lambda100-r2#5folds_cv",
    ]

    for data_path in data_dir.iterdir():
        # load csv
        res = pd.read_csv(data_path / "scores_vs_decoding_acc.csv")

        dataset_id = res["dataset"].unique()[0]
        if dataset_id == "Mante2013":
            # skip mante because has more than one variable
            continue

        ref_acc = neural_data_decoding_accuracy(dataset_id)

        # filter measures
        res = res[res["measure"].isin(measures)]

        # rename the column with "target.{label}"
        target_label = res.columns[-1]
        res = res.rename(columns={target_label: "var_decoding_accuracy"})

        # plot
        plt.figure(figsize=(2.8, 2), dpi=130)
        ax = sns.lineplot(
            data=res,
            x="score",
            y="var_decoding_accuracy",
            hue="measure",
        )

        plt.axhline(ref_acc, color="black", linestyle="--", alpha=1, label="Neural data")

        ax.legend_.remove()
        plt.xlim(0, 1)
        plt.ylim(None, 1)
        plt.xlabel("Score")
        plt.ylabel("Decoding accuracy")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.legend()
        plt.tight_layout()

        plt.savefig(data_path / "scores_vs_decoding_acc.png")
        plt.savefig(data_path / "scores_vs_decoding_acc.pdf")
