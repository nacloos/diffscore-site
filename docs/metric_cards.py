from collections import defaultdict
from pathlib import Path
import pandas as pd
import numpy as np

import diffscore
from diffscore import Measure, Card


def measure_properties_table(save_path=None):
    """
    Table with measure id, name, invariances, and references.
    """
    measures = Measure("*")
    # take only scoring measures
    measures = {
        k: v for k, v in measures.items() if "score" in Card(k.split('.')[-1])["props"]
    }

    invariances = [
        "permutation",
        "orthogonal",
        "invertible-linear",
        "isotropic-scaling",
        "translation",
        "affine"
    ]

    cards = defaultdict(list)
    for measure_id, measure in measures.items():
        card = Card(measure_id.split('.')[-1])
        cards["id"].append(measure_id.split('.')[-1])
        cards["name"].append(card["name"])
        cards["score"].append(card["score"])

        for invariance in invariances:
            cards[invariance].append(invariance in card["invariances"])
        print(card)

    cards_df = pd.DataFrame(cards)
    if save_path:
        cards_df.to_csv(save_path, index=False)
    else:
        print(cards_df)


def measure_backend_consistency(save_dir=None):
    def test_measure_equal(measure1, measure2, n_repeats):
        scores1 = []
        scores2 = []
        for i in range(n_repeats):
            X = np.random.rand(20, 10, 50)
            Y = np.random.rand(20, 10, 50)
            score1 = measure1(X, Y)
            score2 = measure2(X, Y)
            scores1.append(score1)
            scores2.append(score2)

        # return relative error
        # return np.mean(np.abs(np.array(scores1) - np.array(scores2)) / np.array(scores1))
        return np.mean(np.abs(np.array(scores1) - np.array(scores2)))


    measures = Measure("*")

    results = defaultdict(list)
    for measure_id, measure in measures.items():
        print("Measure:", measure_id)
        other_backends = diffscore.make(f"measure.*.{measure_id.split('.')[-1]}")
        for other_measure_id, other_measure in other_backends.items():
            print(other_measure_id)
            relative_error = test_measure_equal(measure, other_measure, 50)
            print("Relative error:", relative_error)
            results["measure"].append(measure_id.split('.')[-1])
            results["backend"].append(other_measure_id.split('.')[1])
            results["relative_error"].append(relative_error)

    results_df = pd.DataFrame(results)

    # backend = index, measure = columns, relative_error = values (add NaN for missing values)
    results_df = results_df.pivot(index="backend", columns="measure", values="relative_error")
    # order columns alphabetically
    results_df = results_df.reindex(sorted(results_df.columns), axis=1)
    # order rows alphabetically
    results_df = results_df.reindex(sorted(results_df.index), axis=0)

    import seaborn as sns
    import matplotlib.pyplot as plt
    print(len(results_df.columns), len(results_df.index))

    plt.figure(figsize=(10, 5), dpi=500)
    sns.heatmap(results_df, cmap="viridis_r", cbar=True, linewidths=2,
                linecolor='white', cbar_kws={"shrink": 0.5, "label": "Mean Absolute Error"})
    plt.ylabel("Backends", fontsize=10)
    plt.xlabel("Measures", fontsize=10)
    plt.gca().xaxis.tick_top()
    plt.gca().xaxis.set_label_position('top')
    plt.xticks(rotation=45, ha='left', fontsize=8)
    plt.yticks(rotation=0, va='center', fontsize=8)
    plt.axis('scaled')
    plt.tight_layout()


    if save_dir:
        results_df.to_csv(save_dir / "backends_matrix.csv", index=False)
        plt.savefig(save_dir / "backends_matrix.png")
    print(results_df)

    # data for d3 heatmap
    # replace nans with -1
    results_df = results_df.fillna(-1)

    # retransform into columns table
    results_df = results_df.stack().reset_index()
    # results_df.columns = ["backend", "measure", "relative_error"]
    results_df.columns = ["variable", "group", "value"]
    if save_dir:
        results_df.to_csv(save_dir / "backends.csv", index=False)


if __name__ == "__main__":
    save_path = Path(__file__).parent / "data" / "cards"
    # measure_properties_table(save_path=save_path / "measures.csv")
    measure_backend_consistency(save_dir=save_path)
