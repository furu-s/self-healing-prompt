from openai import OpenAI
import anthropic
import datetime
import os
from dotenv import load_dotenv
import readline

load_dotenv()

# Global variables
# イテレーションの最大回数
max_iterations = 3

def safe_input(prompt):
    try:
        return input(prompt)
    except UnicodeDecodeError:
        # UnicodeDecodeErrorが発生した場合、空の文字列を返す
        print("入力エラーが発生しました。もう一度入力してください。")
        return ""
def write_to_file(timestamp, prompt, response, score, feedback, improved_prompt):
    logs_folder = "logs"

    # logsフォルダが存在しない場合は作成
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)

    filename = os.path.join(logs_folder, f"prompt_results_{timestamp}.txt")

    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"【元のプロンプト】\n{prompt}\n\n")
        file.write(f"【生成された応答】\n{response}\n\n")
        file.write(f"【評価】 {score}/10\n")
        file.write(f"【フィードバック】\n{feedback}\n\n")
        file.write(f"【改善されたプロンプト】\n{improved_prompt}\n")
        file.write(f"===========\n\n")


def score_response(response):
    # ユーザーに点数を入力してもらう
    print(f"生成された応答: {response}")
    while True:
        try:
            score = float(safe_input("応答の点数を0-10で入力してください: "))
            if 0 <= score <= 10:
                return score
            else:
                print("エラー: 点数は0から10の間で入力してください。")
        except ValueError:
            print("エラー: 有効な数字を入力してください。")


def feedback_response(response):
    # ユーザーに点数を入力してもらう
    print(f"生成された応答: {response}")
    feedback = safe_input("点数の理由を教えてください。改善点を具体的に指摘してください：")
    return feedback


def main():
    print("プロンプト改善を開始します！")
    initial_prompt = safe_input("初期プロンプトを入力してください: ")

    # 初期スコア
    best_score = 0

    # 初期プロンプト
    prompt = initial_prompt

    # 結果を記録するファイル名を生成
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    for i in range(max_iterations):
        print(f"\n実行:{i + 1}回目")
        response = use_claude(prompt)
        score = score_response(response)

        if score == 10:
            best_score = score
            print("評価が満点になったので終わります")
            break

        feedback = feedback_response(response)

        if score > best_score:
            best_score = score

        improved_prompt = improve_prompt_with_ai(prompt, response, score, feedback, 'claude')
        # 次のイテレーションのために改善されたプロンプトを使用する
        prompt = improved_prompt

        print(f"改善されたプロンプト: {improved_prompt}")

        # 各イテレーションの結果をファイルに書き出す
        write_to_file(timestamp, prompt, response, score, feedback, improved_prompt)


def use_claude(prompt):
    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )

    message = client.messages.create(
        # model="claude-3-haiku-20240307",
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        temperature=1,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text


def use_gpt(prompt):
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
        max_tokens=400
    )

    return chat_completion.choices[0].message.content


def deep_feedback_with_ai(feedback, ai_engine="gpt"):
    prompt = f"""
    フィードバック: {feedback}
    あなたはこのようなフィードバックを受け取りました。
    このフィードバックについてより深く考えなさい。要素分解をロジカルに行い、改善点を複数箇条書きで挙げなさい
    改善点:
    """

    if ai_engine == "gpt":
        improvement = use_gpt(prompt)
    elif ai_engine == "claude":
        improvement = use_claude(prompt)
    else:
        raise ValueError("ai_engineはgptかclaudeを指定してください")

    return improvement.strip().split("改善点:")[-1].strip()


def improve_prompt_with_ai(prompt, response, score, feedback, ai_engine="gpt"):
    deep_feedback = deep_feedback_with_ai(feedback, ai_engine)
    improvement_prompt = f"""
    現在のプロンプト: {prompt}
    生成された応答: {response}
    評価:10点満点中 {score}点です
    改善点：
    {deep_feedback}
    
    上記の情報を基に、評価を10点満点にするための新しいプロンプトを提案してください。
    改善されたプロンプトだけを出力しなさい。
    
    よいプロンプトとは
    ・明確な役割を持っていること
    ・出力結果が明確であること
    ・誰向けにどんな行動を期待しているのが明確であること
    が条件です。
    
    改善されたプロンプト:
    """

    if ai_engine == "gpt":
        improvement = use_gpt(improvement_prompt)
    elif ai_engine == "claude":
        improvement = use_claude(improvement_prompt)
    else:
        raise ValueError("ai_engineはgptかclaudeを指定してください")

    improved_prompt = improvement.strip().split("改善されたプロンプト:")[-1].strip()

    # 改善されたプロンプトが空の場合、元のプロンプトを返す
    if not improved_prompt:
        print("警告: AIが改善されたプロンプトを生成できませんでした。元のプロンプトを使用します。")
        return prompt

    return improved_prompt


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
