---
name: ml-research
description: Python機械学習研究プロジェクトに関するタスクで使用。
             データ前処理・モデル実装・評価・可視化・実験管理が対象。
allowed-tools: Read, Grep, Glob, Bash
---

# ML Research Skill

## When to Use
- src/data/ のデータ読み込み・前処理を実装・修正するとき
- src/models/ にモデルを定義・追加するとき
- src/evaluation/ に評価指標・メトリクスを追加するとき
- 実験の再現性に関わるコードを書くとき

## Core Patterns

### データ読み込み
```python
from pathlib import Path
from typing import Any
import numpy as np

DATA_DIR = Path("data")  # 相対パスで定義

def load_dataset(split: str) -> np.ndarray:
    """データセットを読み込む。

    Args:
        split: データ分割名（"train" | "val" | "test"）

    Returns:
        データ配列
    """
    path = DATA_DIR / "processed" / f"{split}.npy"
    return np.load(path)
```

### 再現性確保
```python
import random
import numpy as np

RANDOM_SEED = 42  # 定数化

def set_seed(seed: int = RANDOM_SEED) -> None:
    """乱数シードを固定して再現性を確保する。"""
    random.seed(seed)
    np.random.seed(seed)
    # PyTorch 使用時: torch.manual_seed(seed)
```

### 単位明記の例
```python
LEARNING_RATE = 1e-3        # dimensionless
BATCH_SIZE = 32             # samples
MAX_EPOCHS = 100            # epochs
PATIENCE = 10               # epochs (early stopping)
INPUT_SIZE_PX = 224         # pixels
```

## Do / Don't
DO:
- 実験ごとに configs/ に YAML 設定ファイルを作り、ハイパーパラメータを管理する
- テストでは小さなダミーデータを使い、外部ファイルに依存しない
- モデル保存先は `data/` 以下（git 管理外）

DON'T:
- ハイパーパラメータをコード中にハードコードしない
- GPU 専用コードを書かない（`device = torch.device("cuda" if torch.cuda.is_available() else "cpu")`）
- `data/raw/` を直接編集・上書きしない
