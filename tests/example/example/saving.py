from pathlib import Path



def save_data(titles: list, output_path: Path):

    with open(output_path, "w") as f:
        f.write("\n".join(titles))