# DeepSink

DeepSink V1 是基于 DeepSeek R1 Distill Qwen 7B 的爆仓文学生成器。

## 使用方法

使用 vllm 启动服务:

```bash
vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-7B \
    --port 8001 \
    --enforce-eager \
    --max_model_len 4096 \
    --enable-lora \
    --max-lora-rank 128 \
    --lora-modules deepsink-v1=beautyyuyanli/deepsink-v1-adapter
```

Base model 也可以使用 `casperhansen/deepseek-r1-distill-qwen-7b-awq`。

使用 OpenAI API 调用:

```python
from openai import OpenAI

oai = OpenAI(api_key="DUMMY", base_url="http://localhost:8001/v1")

response = oai.chat.completions.create(
    model="deepsink-v1",
    messages=[
        {
            "role": "user",
            "content": "依据给定的主题，写一篇爆仓文学：2077年川普胜选连任导致“XI币”暴跌爆仓",
        },
    ],
    temperature=0.9,
    top_p=0.7,
    presence_penalty=1.2,
    stream=True,
)

for chunk in response:
    print(chunk.choices[0].delta.content, end="", flush=True)
```

prompt 格式为 `依据给定的主题，写一篇爆仓文学：{主题}`。

## 样例

<details>
<summary>依据给定的主题，写一篇爆仓文学：2077年川普胜选连任导致“XI币”暴跌爆仓</summary>
<"think">
我应该这样设计写作思路:首先,我要构建一个以2077年为背景,并涉及川普连任导致“XI币”暴跌爆仓的高风险投资故事。为了增强故事的紧张感和现实感,我决定采用倒叙和插叙结合的方式,从主人公被强制平仓的当下开始,逐步揭示他 how the story unfolds.  我要运用大量的细节描写,例如环境、声音、感官等,来营造真实的场景,比如断网的手机、刺眼的红光等。

在情节设计上,我会注重故事的起承转合,通过关键事件(如抵押贷款、投资、初爆、后续追责)来推动剧情发展。同时,我会运用一些象征性的元素,例如霓虹灯象征着希望与光明,而红光则暗示着危机和警示。为了更有效地传达人物的内心活动,我需要运用一些文学技巧,例如隐喻、象征、对比等,让读者能够更深入地理解人物的情感变化。

在情感表达方面,我会通过人物的内心独白和动作来展现其情绪,例如主人公在地铁里焦虑的颤抖、手机推送的新闻等。我会设置一个主要的冲突——即川普连任导致的市场崩盘,以及由此引发的连锁反应,来增强故事的悲剧色彩。同时,我也会通过细节描写,例如银行账户余额、抵押合同等,来强化人物的经济压力,从而更有效地传达他们的痛苦和绝望。

为了使故事更具张力,我会穿插一些伏笔,例如开头提到的家人被指控,以及末段出现的家人被逮捕的细节,这些都会增加故事的悬疑氛围。此外,我会使用一些技术性的术语,例如“16倍杠杆”、“K线图”等,来增强故事的专业性,并反映主人公的专业背景。

最后,我会对故事进行多角度的反思,探讨个人贪婪、社会问题以及科技对人类的影响,以此提升故事的深度和思想性。我会确保故事不仅有情节上的起伏,还有在情感和思考上的双重满足。
<"/think">

地铁站里突然亮起红光,手机推送的新闻弹窗刚弹出就被覆盖。屏幕右下角跳动着"爆仓通知",抵押贷款的16倍杠杆已经击穿0.84美元的强平线。我握着冰凉的金属门把手,喉咙发紧的时候,听见身后的火车轰鸣声越来越近。

三个月前还说好的XICoin能破30,现在账户余额只显示0.25。最可笑的是项目方明明承诺的12小时出K线图,三天后就有人发出了第24个垂直跌停。我在工位上敲代码时看见经理冲进办公室,他手指砸键盘的声音清脆得像是砸向屏幕。

其实第一次接触加密货币是在三月,用自己学C++赚的五万块。我把钱全换成了XICoin,当它冲到0.92的时候开16倍多单,四小时就浮盈两百万。后来发现是做市商的算法漏洞,但是该换的单子还是先换了十倍,到0.84的时候又加了两百万保证金。

昨天晚上给银行打电话,催收员第三次强调要加大执行力度。他们之前抵押我的 apartment,说是做空头寸追加保证金。现在账户里有12.7万,其中一半是三年前LTC老用户推荐的"社区治理"计划,现在变成债务。

最让我崩溃的是川普连任的消息。六月初推特突然弹出交易量激增的提示,这个做市商原本就不是专业团队。当价格跌破0.84的支撑位时,我却因为1000元的手续费差错而亏了整整两百万。那天晚上查了十分钟 BINANCE的K线图,发现三个月前的突破都是分时图的假突破,而我正好在所有平台都看到社区成员在喊"再反抽0.88"。

现在护士带着拿着《The New York Times》的老人走进电梯,她紫色的药袋掉在地上碎成一堆。电梯门开了又关,空调吹来的风裹挟着塑料袋的刺鼻气味。我在墙角看着墙壁上贴着的窗户玻璃,镜面上映出走廊的红光,像是打翻了的酒瓶。

桌上还放着今天刚签完的抵押合同,最后一栏写着"由BENJAMIN WILSON负责监控"。我摸了摸口袋里的信用卡,刷掉的金额刚好够买下一周的麦片和咖啡。
</details>

## Data Generation

Using OpenRouter to generate data.

Env to set:
- `HF_TOKEN`
- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`

```bash
python -m deepsink.scripts.data_pipe --help
```

## Training

```bash
cd LLaMA-Factory
llamafactory-cli train ../lora_sft.yaml
```
