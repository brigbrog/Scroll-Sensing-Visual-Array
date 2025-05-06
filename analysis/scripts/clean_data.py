import os
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(SCRIPT_DIR, "../raw")
EDITED_DIR = os.path.join(SCRIPT_DIR, "../edited")


def clean_csv(file_path, participant_map=None):
    df = pd.read_csv(file_path, dtype={"participant": str})

    if participant_map and "participant" in df.columns:
        df["participant"] = df["participant"].astype(str).map(participant_map)

    # remove extra col
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # change to sec
    df["timestamp"] = df["timestamp"] / 1000

    # rename
    df = df.rename(
        columns={
            "timestamp": "time_sec",
            "scroll delta": "scroll_freq",
            "tap": "is_tap",
            "design friction": "friction_type",
            "content type": "content_type",
        }
    )

    df = df.drop(columns=["run"], errors="ignore")

    return df


def process_data():
    os.makedirs(EDITED_DIR, exist_ok=True)

    for file_name in os.listdir(RAW_DIR):
        if not file_name.endswith(".csv"):
            continue

        input_path = os.path.join(RAW_DIR, file_name)

        # Choose participant mapping based on file name
        if "first" in file_name:
            participant_map = {"00": 1, "01": 2}
        elif "second" in file_name:
            participant_map = {"00": 3, "01": 4}
        else:
            participant_map = {}

        cleaned_df = clean_csv(input_path, participant_map)

        # Split into separate CSVs by participant
        for participant_id, participant_df in cleaned_df.groupby("participant"):
            part_filename = f"p{participant_id}.csv"
            output_path = os.path.join(EDITED_DIR, part_filename)

            participant_df = participant_df.drop(
                columns=["participant"], errors="ignore"
            )
            participant_df.to_csv(output_path, index=False)

            print(f"Saved participant {participant_id} to {output_path}")

'''
if __name__ == "__main__":
    process_data()
'''