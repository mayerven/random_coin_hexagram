# Random Yao — ChatGPT Skill Bundle

This folder is the ChatGPT-oriented distribution of
`mayerven/random_coin_hexagram`.

It contains exactly one skill manifest and the executable casting script:

```text
random-yao/
├── SKILL.md
└── scripts/
    └── cast.py
```

## Build the uploadable ZIP

From the repository root:

```bash
python3 scripts/build_chatgpt_bundle.py
```

This creates:

```text
dist/random-yao-chatgpt.zip
```

The ZIP contains a single top-level folder named `random-yao`, which is the
portable structure expected by OpenAI skill upload flows.

## Install in ChatGPT

When Skills upload is available for your ChatGPT account/workspace:

1. Open **Plugins**.
2. Open the **Skills** tab.
3. Select **Create**.
4. Select **Upload from your computer**.
5. Upload `dist/random-yao-chatgpt.zip`.
6. Review the skill and choose **Install**.

Availability depends on the current ChatGPT plan, workspace configuration, and
rollout.

## Usage

After installation, ask naturally, for example:

```text
随机摇一卦：我现在是否适合主动推进这件事？
```

The skill uses Python's `secrets` module. The question text labels the cast but
does not affect randomness.
