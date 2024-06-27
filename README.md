# AI-Assisted Prompt Improver

AI-Assisted Prompt Improverは、人工知能を活用してプロンプトを繰り返し改善するPythonスクリプトです。OpenAIのGPT-3.5とAnthropicのClaude AIモデルを使用して、ユーザーのフィードバックに基づいてプロンプトを最適化します。

## 機能

- 初期プロンプトの入力
- AIモデル（GPTまたはClaude）を使用したレスポンス生成
- ユーザーによるレスポンスの評価とフィードバック
- AIを使用したフィードバックの分析と要素分解
- 改善されたプロンプトの生成
- 結果のログ記録

## 必要条件

- Python 3.6以上
- OpenAI API キー
- Anthropic API キー

## インストール

1. リポジトリをクローンします：
```
git clone https://github.com/yourusername/ai-assisted-prompt-improver.git
cd ai-assisted-prompt-improver
```

2. 必要なパッケージをインストールします
```
pip install -r requirements.txt
```

3. .envファイルを作成し、API キーを設定します
```
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

## 使用方法

スクリプトを実行するには、次のコマンドを使用します
```
python main.py
```
画面の指示に従って、初期プロンプトを入力し、生成されたレスポンスを評価してフィードバックを提供してください。

## カスタマイズ

- `max_iterations`変数を変更することで、プロンプト改善の最大回数を調整できます。
- AIモデルの選択やパラメータは`use_claude`および`use_gpt`関数内で変更できます。

## ライセンス

このプロジェクトは[MITライセンス](LICENSE)の下で公開されています。

## 貢献

バグ報告、機能リクエスト、プルリクエストを歓迎します。大きな変更を加える前に、まずissueを開いて議論することをお勧めします。

## 作者

[Your Name] - [Your Email]

プロジェクトリンク: https://github.com/yourusername/ai-assisted-prompt-improver
