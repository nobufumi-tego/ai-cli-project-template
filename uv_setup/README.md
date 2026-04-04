# Python ML Environment (uv + JupyterLab)

uvを使ってWindows / macOS / Linuxに機械学習テスト環境を自動構築するインストーラーです。

## 含まれるパッケージ

| カテゴリ | パッケージ |
|---|---|
| Jupyter | JupyterLab, ipywidgets, ipykernel |
| データ処理 | NumPy, Pandas, Polars |
| 機械学習 | scikit-learn, XGBoost, LightGBM |
| 深層学習 | PyTorch, torchvision (CPU) |
| 可視化 | Matplotlib, Seaborn, Plotly |
| ユーティリティ | tqdm, joblib, SciPy |

## 使い方

### Windows

```bat
install.bat
```

またはPowerShellで直接：
```powershell
Set-ExecutionPolicy Bypass -Scope Process
.\install.ps1
```

### macOS / Linux

```bash
chmod +x install.sh start_jupyter.sh
./install.sh
```

### JupyterLab の起動

**Windows:**
```bat
start_jupyter.bat
```

**macOS / Linux:**
```bash
./start_jupyter.sh
```

## ファイル構成

```
uv_setup/
├── install.sh          # macOS / Linux インストーラー
├── install.ps1         # Windows インストーラー (PowerShell)
├── install.bat         # Windows インストーラー (ダブルクリック用)
├── start_jupyter.sh    # JupyterLab 起動 (macOS/Linux)
├── start_jupyter.ps1   # JupyterLab 起動 (Windows PowerShell)
├── start_jupyter.bat   # JupyterLab 起動 (Windows ダブルクリック用)
├── pyproject.toml      # 依存パッケージ定義
├── notebooks/          # サンプルノートブック
│   └── ml_quickstart.ipynb
└── .venv/              # 仮想環境 (インストール後に生成)
```

## 要件

- **uv**: 未インストールの場合は自動でインストールされます
- **Python 3.11+**: uvが自動でダウンロードします
- **インターネット接続**: パッケージのダウンロードに必要
- **空きディスク容量**: 約5〜8GB（PyTorchを含む）

## カスタマイズ

`pyproject.toml` の `dependencies` を編集して必要なパッケージを追加/削除できます。
変更後は再度インストールスクリプトを実行してください。

### GPU版PyTorchを使う場合

`pyproject.toml` の torch 行を削除し、インストール後に手動で：
```bash
# CUDA 12.1の例
uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```
