from collections import defaultdict
from pathlib import Path
import pandas as pd

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

    cards = defaultdict(list)
    for measure_id, measure in measures.items():
        card = Card(measure_id.split('.')[-1])
        cards["id"].append(measure_id.split('.')[-1])
        cards["name"].append(card["name"])
        cards["score"].append(card["score"])
        cards["orthogonal-invariant"].append(
            "True" if "orthogonal" in card["invariances"] else "False"
        )
        cards["isotropic-scaling-invariant"].append(
            "V" if "isotropic-scaling" in card["invariances"] else ""
        )

        print(card)

    cards_df = pd.DataFrame(cards)
    if save_path:
        cards_df.to_csv(save_path, index=False)
    else:
        print(cards_df)


if __name__ == "__main__":
    save_path = Path(__file__).parent / "data" / "cards" / "measures.csv"
    measure_properties_table(save_path=save_path)
