# LLM

本文介绍了一些LLM的测试数据，我使用的LLM以及使用体验。（live code bench统一使用v6，Codeforces按Live Code Bench Pro的结果，Humanity’s Last Exam也以官网为准，非官网数据标*。）

### 模型测试数据

这部分收录了一些LLM在常见的测试集的测试结果，只收录同规模下最优秀的模型。

说明：

1. 已排除输出价格高于32元/M token的模型、同成本下效果不是最佳的模型、缺少多语言支持的模型以及公认刷分（MoE 40b以内，Dense 20b以内且同级别没有更好用的模型时仍收录）的模型，非推理模型只收录对编程优化或者有推理特性的模型。
2. [malody2014/llm_benchmark](https://github.com/malody2014/llm_benchmark)提供了统一标准下更多模型的测试结果，可以参考。

旗舰模型和推理模型：

| Model                  | AIME2025 | GPQA Diamond | Codeforces(rating) | LiveCodeBench | SWE-Bench | Humanity’s Last Exam | ARC AGI2 |
| :--------------------- | -------- | ------------ | ------------------ | ------------- | --------- | --------------------- | -------- |
| Qwen3 4b 2507          | 62.0     | 47.4         |                    | 35.1          |           |                       |          |
| Qwen3 4b 2507 thinking | 81.3     | 65.8         |                    | 55.2          |           |                       |          |
| Deepseek V3.1          | 88.4     | 80.1         |                    | 74.8          | 66.0      |                       |          |
| GPT5 Mini              | 91.1     | 82.3         |                    |               | 71.0      | 16.7                  | 4.5      |
| GPT OSS 120b           | 92.5     | 80.1         |                    |               | 62.4      |                       |          |
| GPT OSS 20b            | 91.7     | 71.5         |                    |               | 60.7      |                       |          |
| GLM4.5 355b a32b       |          | 79.1         |                    | 72.9          | 64.2      | 14.4*                 |          |
| GLM4.5 Air 106b a12b   |          |              |                    | 70.7          | 57.6      | 10.6*                 |          |
| Kimi K2                | 49.5     | 75.1         |                    | 53.7          | 65.8      |                       |          |

多模态模型：

| Model              | MMLU | MMNU-Pro | ChartQAPro | DocVQA | OCRBench | AI2D | MathVista | MathVision |
| ------------------ | ---- | -------- | ---------- | ------ | -------- | ---- | --------- | ---------- |
| GPT5 Mini          | 81.6 | 74.1     |            |        |          |      | 84.4      |            |
| MiMo VL 7b RL 2508 | 70.6 |          |            |        | 88.6     |      |           |            |
| GLM4.5V 106b a12b  | 75.4 | 65.2     | 64.0       |        | 86.5     | 88.1 | 84.6      | 65.6       |

无审查模型：

这类模型比较少没有专门的测试数据，通常与基底模型接近，目前Dolphin3系列比较完善，也可以选择最新模型的去对齐版本。

无审查模型在角色扮演等任务有优势，也可以用于处理成人等题材的内容。

### 模型推理

##### 推理框架

桌面端：

1. Transformers兼容性强，但优化较差。
2. Ollama基于llama.cpp，稳定性和显存优化较好，但对多模态模型的支持比上游慢。
3. LM Studio同样基于llama.cpp，兼容性与上游一致，提供图形界面并集成RAG功能。
4. VLLM注重张量并行和并发优化，对多模态模型的兼容性也有优势。
5. KTransformer注重异构计算，长上下文和并发速度相比CPU部署有一定优势。

移动端：

1. MNN Chat推理速度较快，对Omni模型的支持比较有优势但支持的模型数量较少。
2. Pocketpal基于llama.cpp对移动端优化的llama.rn，支持的模型多一些。
3. Chatterui也基于llama.rn，速度比Pocketpal快一些但有时候会出现兼容性问题。

##### 本地部署情况

考虑模型适配和自带界面，我选择了LM Studio。我的电脑配置为3070m+5600h+双通道ddr4 3200。桌面端部署情况如下：

1. Deepseek R1 0528 Qwen3 8b用于通用任务。
2. Mimo VL 7b RL用于多模态任务。
3. Gemma3 12b abliterated v2用于无审查任务。
4. Qwen3 30b a3b 2507/Qwen3 Coder 30b a3b用于CPU推理（thinking版本由于速度问题暂不部署）。

手机配置为骁龙8gen1+8g内存，目前只进行测试性部署。

（考虑到内存带宽瓶颈，16g设备用Ring Lite比较合适，待Llama.cpp支持后也可以用Kimi VL）

##### api使用情况

我个人偏向开源模型，使用的api如下：

1. Deepseek api，使用Deepseek模型，因为其模型在开源模型中比较优秀，成本也不太高。
2. Openrouter api，主要使用免费模型，提供Dolphin3等无审查模型相比国内api也有优势。
