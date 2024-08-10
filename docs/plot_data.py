from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from diffscore import Dataset
from diffscore.analysis.decoding import decoder_logistic
import diffscore_exp
import diffscore_exp.exp.benchmark_metrics.eigenspectrum


def neural_data_decoding_accuracy(dataset_id):
    dataset = Dataset(dataset_id)

    if isinstance(dataset, tuple):
        X, conditions = dataset
    else:
        X = dataset
    
    if dataset_id == "Mante2013" or "siegel15" in dataset_id:
        print("Mante2013 dataset detected. Using only the 'context' condition")
        conditions = [{"context": c["context"]} for c in conditions]

    decoder = decoder_logistic

    labels = conditions[0].keys()
    assert len(labels) == 1, f"Only one label is supported for now, got {labels}"

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
        "cka-angular-score",
        "nbs",
        "procrustes-angular-score",
        "linreg",
        # "rsa-correlation-corr",
        "ridge-lambda100-r2#5folds_cv"
    ]

    for data_path in data_dir.iterdir():
        # load csv
        res = pd.read_csv(data_path / "scores_vs_decoding_acc.csv")

        dataset_id = res["dataset"].unique()[0]
        # if dataset_id == "Mante2013":
        #     # skip mante because has more than one variable
        #     continue

        ref_acc = neural_data_decoding_accuracy(dataset_id)


        # TODO: don't hardcode chance level
        if dataset_id in ["Hatsopoulos2007", "MajajHong2015"]:
            chance_level = 1/8
        else:
            chance_level = 1/2
        

        # filter measures
        res = res[res["measure"].isin(measures)]

        if dataset_id == "Mante2013" or "siegel15" in dataset_id:
            target_label = "decode.context"
        else:
            # assert only one column with "decode." prefix
            target_cols = [col for col in res.columns if col.startswith("decode.")]
            assert len(target_cols) == 1, f"Only one target column is supported for now, got {target_cols}"
            # rename the column with "decode.{label}"
            target_label = res.columns[-1]
        res = res.rename(columns={target_label: "var_decoding_accuracy"})

        colors = diffscore_exp.make("color.scores")
        # plot
        plt.figure(figsize=(2.8, 2), dpi=130)
        ax = sns.lineplot(
            data=res,
            x="score",
            y="var_decoding_accuracy",
            hue="measure",
            palette=colors,
            linewidth=2.5
        )

        plt.axhline(ref_acc, color="black", linestyle="--", alpha=1, label="Neural data")
        plt.axhline(chance_level, color="dimgray", linestyle="--", alpha=1, label="Chance level")

        for measure in measures:
            if measure not in res["measure"].values:
                continue

            threshold = chance_level + (ref_acc - chance_level)*0.9
            score_at_threshold = np.interp(threshold, res[res["measure"] == measure]["var_decoding_accuracy"], res[res["measure"] == measure]["score"])
            # plt.axvline(score_at_threshold, color=colors[measure], linestyle="--", alpha=1, label="Threshold")
            # draw a dot at the threshold right above the x-axis
            # y_value = np.min(res["var_decoding_accuracy"]) - 0.01
            y_value = chance_level - 0.05
            plt.scatter(score_at_threshold, y_value, color=colors[measure], marker="o", s=3, zorder=10)

        ax.legend_.remove()
        plt.xlim(0, 1)
        plt.ylim(None, 1)
        plt.xlabel("Optimized score", fontsize=10)
        plt.ylabel("Decoding accuracy", fontsize=10)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.tight_layout()
        # plt.legend()
        plt.savefig(data_path / "scores_vs_decoding_acc.png")
        plt.savefig(data_path / "scores_vs_decoding_acc.pdf")

        # plot legend on separate figure
        plt.figure(figsize=(2, 2), dpi=130)
        handles, labels = ax.get_legend_handles_labels()
        plt.legend(handles, labels, loc="center", frameon=False)
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(data_path / "scores_vs_decoding_acc_legend.png")
        plt.savefig(data_path / "scores_vs_decoding_acc_legend.pdf")