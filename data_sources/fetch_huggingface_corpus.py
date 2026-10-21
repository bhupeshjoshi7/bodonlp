"""
Download and extract Bodo splits from Hugging Face open datasets
(e.g., ai4bharat/IndicCorpV2, facebook/flores200, cis-lmu/GlotCC-V1).
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def main():
    print("Checking Hugging Face datasets library...")
    try:
        from datasets import load_dataset
        print("datasets library is installed. Fetching sample Bodo (brx_Deva) text...")
        # Load small split or streaming sample
        ds = load_dataset("ai4bharat/IndicCorpV2", "brx_Deva", split="train", streaming=True)
        samples = []
        for i, row in enumerate(ds):
            if i >= 10:
                break
            samples.append(row["text"])
            print(f"Sample {i+1}: {row['text'][:80]}...")
            
        out_file = ROOT / "data_sources" / "raw_texts" / "hf_indiccorp_sample.txt"
        out_file.parent.mkdir(parents=True, exist_ok=True)
        with open(out_file, "w", encoding="utf-8") as f:
            for s in samples:
                f.write(s + "\n")
        print(f"Saved Hugging Face samples to {out_file}")
    except ImportError:
        print("Note: Hugging Face 'datasets' package is not installed.")
        print("To download web-scale Bodo corpora directly from Hugging Face, run:")
        print("  pip install datasets")
    except Exception as e:
        print(f"Dataset streaming notice: {e}")


if __name__ == "__main__":
    main()
