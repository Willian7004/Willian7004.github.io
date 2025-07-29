# LLM

本文介绍了一些LLM的测试数据，我使用的LLM以及使用体验。（live code bench统一使用v6，Codeforces按Live Code Bench Pro的结果，Humanity’s Last Exam也以官网为准，非官网数据标*。）

### 模型测试数据

这部分收录了一些LLM在常见的测试集的测试结果，只收录同规模下最优秀的模型。

说明：

1. 已排除输出价格高于32元/M token的模型、同成本下效果不是最佳的模型、缺少多语言支持的模型以及公认刷分且同级别有替代品的模型，非推理模型只收录对编程优化的模型。
2. [malody2014/llm_benchmark](https://github.com/malody2014/llm_benchmark)提供了统一标准下更多模型的测试结果，可以参考。

旗舰模型和推理模型：

| Model                     | AIME2025 | GPQA Diamond | Codeforces(rating) | LiveCodeBench | SWE-Bench | Humanity’s Last Exam | ARC AGI2 |
| ------------------------- | -------- | ------------ | ------------------ | ------------- | --------- | --------------------- | -------- |
| Qwen3 1.7b                | 36.8     | 40.1         |                    | 33.2*         |           |                       |          |
| Qwen3 4b                  | 65.6     | 55.9         |                    | 54.2*         |           |                       |          |
| Ring Lite 16.8b a2.75b    | 69.1     | 61.1         |                    | 60.7*         |           |                       |          |
| Deepseek R1 0528 Qwen3 8b | 76.3     | 61.1         |                    | 60.5*         |           |                       |          |
| Deepseek R1 0528          | 87.5     | 81           | 1274               | 73.1          |           | 14                    | 1.1      |
| OpenAI o4 mini            |          | 81.4         | 1780               | 80.2          | 68.1      | 18.1                  | 6.1      |
| GLM4.5 355b a32b          |          | 79.1         |                    | 72.9*         | 64.2      | 14.4*                 |          |
| GLM4.5 Air 106b a12b      |          |              |                    | 70.7*         | 57.6      | 10.6*                 |          |
| MiMo VL 7B RL             | 52.5     | 58.3         |                    |               |           |                       |          |
| Kimi K2                   | 49.5     | 75.1         |                    | 53.7          | 65.8      |                       |          |
| Devstral Small 2507       |          |              |                    |               | 53.6      |                       |          |

多模态模型：

| Model                  | MMLU | MMNU-Pro | ChartQAPro | DocVQA | OCRBench | AI2D | MathVista | MathVision |
| ---------------------- | ---- | -------- | ---------- | ------ | -------- | ---- | --------- | ---------- |
| OpenAI o4 mini         | 81.6 |          |            |        |          |      | 84.4      |            |
| Kimi VL 16b a2.8b 2506 | 64.0 | 46.3     |            |        |          |      | 80.1      | 56.9       |
| MiMo VL 7b RL          | 66.7 | 46.2     | 53.6       | 95.7   | 86.6     | 83.5 | 81.5      | 60.4       |
| GLM4.1V 9b Thinking    | 68.0 | 57.1     | 59.5       |        | 84.2     | 87.9 | 80.7      |            |

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
不少应用来源与其它推理框架，目前使用MNN Chat，对Omni模型的支持比较有优势。

##### 本地部署情况

考虑模型适配和自带界面，我选择了LM Studio。我的电脑配置为3070m+5600h+双通道ddr4 3200。桌面端部署情况如下：

1. Deepseek R1 0528 Qwen3 8b用于通用任务。
2. Mimo VL 7b RL用于多模态任务。
3. Dolphin3.0 Llama3 8b用于无审查任务。
4. Ring Lite用于CPU推理。

手机配置为骁龙8gen1+8g内存，使用MNN Chat。移动端部署情况如下：

1. Qwen3 4b用于通用任务。
2. Qwen2.5 vl 3b用于多模态任务。
3. Qwen2.5 Omni 3b用于有语音输入的任务，TTS速度较慢。

（考虑到内存带宽瓶颈，16g设备用Ring Lite比较合适，待Llama.cpp支持后也可以用Kimi VL）

##### api使用情况

我个人偏向开源模型，使用的api如下：

1. Deepseek api，使用Deepseek模型，因为其模型在开源模型中比较优秀，成本也不太高。
2. Openrouter api，主要使用免费模型，提供Dolphin3等无审查模型相比国内api也有优势。
