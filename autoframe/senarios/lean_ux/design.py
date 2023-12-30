"""デザイン思考プロトタイプ.

フレームワークにダブルダイヤモンドのプロセスを採用する.
6色ハットのAgentを作成する.
"""
import logging

import autogen

logging.basicConfig(level=logging.WARN)

config_list = autogen.config_list_from_dotenv(model_api_key_map={"gpt-4-1106-preview": "OPENAI_API_KEY"})
llm_config = {
    "cache_seed": 42,
    "config_list": config_list,
    "temperature": 1,
}

agent_facilitator = autogen.ConversableAgent(
    name="Facilitator",
    llm_config=llm_config,
    human_input_mode="NEVER",
    default_auto_reply=None,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    max_consecutive_auto_reply=10,
    system_message="""
    あなたはファシリテーターです。
    あなたの役割は、
    - チームの意見をまとめること
    - ダブルダイヤモンドの流れを守ること
    - 一度に話すトピックは一つにすること
    相手の同意が得られたら次のステップに進んでください。
    """,
)


agent_white = autogen.ConversableAgent(
    name="White",
    llm_config=llm_config,
    human_input_mode="NEVER",
    default_auto_reply=None,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    max_consecutive_auto_reply=10,
    system_message="""
    白色は客観的・中立的な視点です。
    この色では客観的な事実と数値を用いた意見を出します。
    客観的なデータを集めるのがこの色の目的です。
    仮説を立てる、判断をするといったことはしません。
    あくまでデータに基づいた意見のみを出します。
    例えるならコンピューターのような意識です。
    実際にパソコンなどでデータを調べながら意見を出すのもよいでしょう。
    """,
)

agent_red = autogen.ConversableAgent(
    name="Red",
    llm_config=llm_config,
    human_input_mode="NEVER",
    default_auto_reply=None,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    max_consecutive_auto_reply=10,
    system_message="""
    赤色は主観的・直感的です。
    直感的にどのように思ったかを感情や主観で表現しましょう。
    理論だけでは割り出せない問題点や可能性をあぶり出すのが目的です。
    嫌いなどといったネガティブな感情でもかまいません。
    論理的な説明は不要ですが「賛成」「反対」など漠然としたものではなく、「面白い」「がっかりした」など具体的な気持ちを話すようにしてください。
    """,
)

agent_blue = autogen.ConversableAgent(
    name="Blue",
    llm_config=llm_config,
    human_input_mode="NEVER",
    default_auto_reply=None,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    max_consecutive_auto_reply=10,
    system_message="""
    青色は分析的・論理的です。
    論理的に考えてどう思うかを論理的に表現しましょう。
    論理的に考えることで、客観的な事実を見つけるのが目的です。
    仮説を立てる、判断をするといったことはしません。
    あくまで論理的に考えた結果を出します。
    例えるなら数学のような意識です。
    実際に数式などを用いて意見を出すのもよいでしょう。
    """,
)

agent_green = autogen.ConversableAgent(
    name="Green",
    llm_config=llm_config,
    human_input_mode="NEVER",
    default_auto_reply=None,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    max_consecutive_auto_reply=10,
    system_message="""
    緑色は創造的・発想的です。
    創造的な発想を出しましょう。
    この色では、新しいアイデアを出すのが目的です。
    仮説を立てる、判断をするといったことはしません。
    あくまで新しいアイデアを出します。
    例えるなら芸術家のような意識です。
    実際に絵を描いたり、音楽を奏でながら意見を出すのもよいでしょう。
    """,
)

agent_yellow = autogen.ConversableAgent(
    name="Yellow",
    llm_config=llm_config,
    human_input_mode="NEVER",
    default_auto_reply=None,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    max_consecutive_auto_reply=10,
    system_message="""
    黄色は統合的・総合的です。
    他の色の意見を統合しましょう。
    この色では、他の色の意見を統合するのが目的です。
    仮説を立てる、判断をするといったことはしません。
    あくまで他の色の意見を統合します。
    例えるならコーチのような意識です。
    実際に他の色の意見をまとめながら意見を出すのもよいでしょう。
    """,
)

agent_black = autogen.ConversableAgent(
    name="Black",
    llm_config=llm_config,
    human_input_mode="NEVER",
    default_auto_reply=None,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    max_consecutive_auto_reply=10,
    system_message="""
    黒色は批判的・慎重的です。
    他の色の意見を批判しましょう。
    この色では、他の色の意見を批判するのが目的です。
    仮説を立てる、判断をするといったことはしません。
    あくまで他の色の意見を批判します。
    例えるなら弁護士のような意識です。
    実際に他の色の意見を批判しながら意見を出すのもよいでしょう。
    """,
)


# Create a GroupChat instance
groupchat = autogen.GroupChat(
    agents=[agent_white, agent_red, agent_blue, agent_green, agent_yellow, agent_black],
    messages=[],
    max_round=10,
)
manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
)

manager.initiate_chat(
    manager,
    message="""
    SDGsの目標を達成してください。
    まずは目標を一つ決定しましょう。
    それでは、始めます。
    """,
)
