from rich import print
from openai import OpenAI
from openai import AsyncOpenAI
import re

prompt_example1 = """
2025.2.3
外面下着小雨，路上几乎没人，只有几把孤零零的伞缓缓移动。手机屏幕上是以太暴跌的新闻，我的账户余额只剩下三位数。窗外的冷清与我的落魄交织在一起

我不甘心，为什么我会这么失败？
从小镇做题家到考上武汉大学，再到香港大学的研究生，我明明每一步都在努力。可到现在，我却亏的一无所有

去年，我辞掉了工作，带着一年半攒下的20万，一头扎进了加密货币的世界。起初，一切都显得那么美好。每天盯盘、研究项目、分析趋势，感觉比上班自由多了，毕竟是在为自己打工。那段时间，我赚到了一点钱，还结识了一群朋友，大家一起玩，分享机会。

从年初到年底，我的状态一直不错，一共赚了100多万，但都没提现。直到12月，那会我有点跟不上市场pvp的节奏加上我判断市场会迎来一波山寨币的爆发期，于是决定抄底BOME。我幻想着能复刻去年PEPE的奇迹，从0.008一路抄到0.003，结果今天早上的暴跌直接让我爆仓了。其实我开的杠杆并不高，不到3倍。

我下注了我的所有，但还是没了。

最讽刺的是，我回家还让父母抄了我的底，让他们从0.004开始买 $bome，一直补到0.003，截止今天已经几乎腰斩，我自己亏钱也就算了，还带着父母一起亏，我真是出生啊，哎。

这个年过的如坐针毡，每天打开交易所都是账户的下跌，和亲戚朋友说自己在干什么工作，也显得毫无底气，明明每天都很累，却钱也没赚到，生活也过得苦，还收获了一些亲戚“读那么多书还不是没稳定工作”的嘲讽。

我真的很好奇，究竟谁还能在交易所赚钱？跌了5倍的币还能继续跌4倍，一上线就跌4-5倍？这样的情况下真的会有人进来赚到钱吗？

现在的心情真的很复杂，不甘心，却又迷茫得不知所措。明明感觉也已经努力，可结果却总是事与愿违。那些曾经让我热血沸腾的目标，如今像被雨打湿的纸，模糊得看不清方向。我不知道接下来该往哪里走，也不知道还能不能重新站起来。

现在看来，我的人生，彻底失败。
""".strip()

prompt_example2 = """
起初我只是想试试水，用一点闲钱玩玩。
狗狗币翻了十倍，SHIBA翻了二十倍，连一个名字都念不顺的山寨币，硬生生翻了五十倍。
账户从五千到五万，从五万到五十万，数字涨得太快，快到我开始觉得自己是个天才。
“别人亏钱是因为不懂，而你早就看透了市场。”
这是我对自己说的话。每一次赚到钱，我都更相信自己能赢下去。
后来我不再满足于现货了——现货赚钱太慢，杠杆才是正确的打开方式。
10倍、20倍、50倍，我的仓位越做越重。每一次回调都是加仓的机会，每一次拉升都让我欲罢不能。
我甚至开始想着，等账户上有了一百万，就把工作辞了，买车买房，彻底告别这该死的社畜生活。
可暴富的游戏，往往有一个致命的规则——它只会让你赢到愿意把所有筹码压上。
三天前，BTC开始大跌。
“没事，正常回调，主力洗盘。”我告诉自己，一边补仓，一边加杠杆，把最后的流动资金也砸了进去。
可跌势比想象中还快，市场像是被惊雷劈开，红色的数字一路狂泻。
30万，15万，8万……屏幕上的余额像漏水的水缸，无论我怎么捂，也止不住。
我手足无措地盯着K线，眼睁睁看着它踩过我的爆仓线。
凌晨三点，我的手机响了，是交易所发来的通知：
“您的账户已被强平，余额：0.00。”
那一刻，我坐在漆黑的房间里，像是一具被掏空的尸体。
手里攥着昨天刚点开的烟盒，里面只剩下一根。
我掏出打火机点燃，深吸一口，呛得咳嗽，眼泪莫名涌了出来。
“明天房租怎么交？”
“信用卡的账单怎么办？”
“还有爸妈那边的钱，说好的翻倍给他们的本金呢？”
问题一个接一个，我却不敢回答。我知道，我再也填不上这个窟窿了。
烟燃到尽头，我盯着桌上的手机发呆。
屏幕还停留在交易所的充值界面，心里有个声音在说：
“充点钱，开个小仓，翻本就能解套。”
我摇了摇头，摁灭烟头。可十几分钟后，手指还是点了充值键。
1000块，最后一点能凑出来的零头。这次一定能赢回来，一定能翻本，一定能……
屏幕亮着，充值成功，行情图一波波跳动，我却突然有点看不清了。
天快亮了，窗外的第一缕光照进来。我靠在椅子上，闭上眼，脑海里浮现一个荒唐的场景：
我站在一张巨大无比的赌桌前，所有人都在下注，赢的笑，输的哭，而我早就已经一无所有，却还在向赌场讨要“再来一次”的机会。
你问我为什么？
因为一旦开始赌，就再也停不下来了。
""".strip()

prompt0 = f"""
通过以下文章分析“爆仓文学”的情节设计、写作手法、情感表达等写作方法。最终告诉我如何写作爆仓文学，要求是尽可能简单易懂可操作的写作指南，无需输出赏析部分。
<Example>
```
{prompt_example1}
```
</Example>
<Example>
```
{prompt_example2}
```
</Example>
""".strip()

prompt_ins = """
参考写作指南和例文，依据要求，写一篇爆仓文学。注意，作品中的具体数值、时间、金额等细节不得与例文相同，情节设计不得与指南相同，必须增加指南中未有举例的元素，主题可以是任意投资产品，也可以是加密货币，减少使用修辞手法。
输出格式如下：
```
<Topic>
主题，什么时候在什么产品上爆仓
</Topic>
<Content>
内容
</Content>
```
""".strip()
prompt_guide = """
一、基础构建
1. 采用三步结构:逆袭铺垫 → 致命失误 → 彻底崩盘
2. 使用日记体(日期开头)增加真实感
3. 主角设置标准模板:
   - 农村/小镇出身
   - 有985/海外名校背景
   - 原生家庭拮据
   - 等等

二、场景要素模板
1. 天气必选:冬夜寒雨/台风暴雨/大雾弥漫(对应阴郁情绪)
2. 账户描写公式:
   - 余额:3位数的尾数(例:672.83)
   - 杠杆倍数:精确到小数点后一位(例:3.3倍)
   - 等等
3. 道具清单:
   - 亮着冷光的电子设备
   - 未拆封的外卖包装
   - 发皱的香烟盒
   - 等等

三、情绪输出模板
1. 两段式自问:
   "我X年前明明...(例:裸考上清华)→ 现在却...(例:负债百万)"
2. 必加悔恨指标:
   - 转移父母养老金
   - 隐瞒恋人实情
   - 毁约朋友合作
   - 等等
3. 社会鞭挞三件套:
   - 催婚亲戚的讥讽
   - 前同事的成功朋友圈
   - 房东的催租消息
   - 等等

四、技术指标(关键)
1. 收益曲线例如:
   20万→130万→670万→爆仓归零
2. 必出现专业术语:
   - 插针/清算
   - RSI超卖
   - 市商吃单
   - 等等
3. 精确时间锚点:
   "从0.008补到0.003"类具体数值

五、结尾可选句式
1. 物象隐喻:
   "屏幕绿光投射在积水/雪地/瓷砖上"
2. 身体反应:
   "太阳穴突跳/指尖发抖/口腔血腥味"
3. 收尾定式:
   "XX年X月X日,我的人生/尊严/希望就此清零"
4. 等等

实操提示:取3项基础模板+2个情绪指标+1组技术参数组合使用,场景要素任选三种搭配,用手机备忘录格式写作效果最佳。
""".strip()
prompt1 = f"""
<Instruction>
{prompt_ins}
</Instruction>
<Guide>
{prompt_guide}
</Guide>
<Example>
{prompt_example1}
</Example>
<Example>
{prompt_example2}
</Example>
""".strip()


prompt2 = f"""
<Instruction>
{prompt_ins}
</Instruction>
<Example>
{prompt_example1}
</Example>
<Example>
{prompt_example2}
</Example>
""".strip()

prompt_think = """
<Instruction>
通过以下文章分析“爆仓文学”的情节设计、写作手法、情感表达等写作方法。无需输出结果，回复"Done"即可
</Instruction>
<Example>
{prompt_example1}
</Example>
""".strip()

prompt_think_fix = """
<Instruction>
将以下文章的赏析替换为第一人称，即“作者”替换为“我”，去除原本的赏析者“我”，并将赏析的语言改为作者叙述写作思路的语言。
输出格式如下：
```
<Think>
我应该这样设计写作思路，...
</Think>
```
</Instruction>
<Comment>
{comment}
</Comment>
""".strip()


def get_response(
    prompt: str, model: str = "deepseek/deepseek-r1", debug: bool = True
) -> tuple[str, str]:
    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        extra_body={
            "include_reasoning": True,
            "provider": {"order": ["Fireworks", "Nebius"]},
        },
        stream=True,  # Enable streaming
    )

    # Print the main content
    doing_reasoning = True
    thinking = ""
    answer = ""
    for chunk in response:
        if chunk.choices[0].delta.content and doing_reasoning:
            doing_reasoning = False
            if debug:
                print("-" * 100)
        try:
            content = (
                chunk.choices[0].delta.model_extra["reasoning"]  # type: ignore
                if not chunk.choices[0].delta.content
                else chunk.choices[0].delta.content
            )
        except Exception:
            content = None
        if content:
            if doing_reasoning:
                thinking += content
            else:
                answer += content
            if debug:
                print(content, end="", flush=True)
    return thinking.strip(), answer.strip()


async def aget_response(
    prompt: str, model: str = "deepseek/deepseek-r1"
) -> tuple[str, str]:
    client = AsyncOpenAI()
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        extra_body={
            "include_reasoning": True,
            "provider": {"order": ["Fireworks", "Nebius"]},
        },
    )
    return (
        (
            response.choices[0].message.model_extra.get("reasoning", "")
            if response.choices[0].message.model_extra
            else ""
        ),
        response.choices[0].message.content or "",
    )


async def clone_article() -> tuple[str, str]:
    _thinking, answer = await aget_response(prompt=prompt2)

    # Extract topic and content using regex
    topic_match = re.search(r"<Topic>\s*(.*?)\s*</Topic>", answer, re.DOTALL)
    content_match = re.search(r"<Content>\s*(.*?)\s*</Content>", answer, re.DOTALL)

    if not topic_match or not content_match:
        raise ValueError("Failed to extract topic or content from response")

    return topic_match.group(1), content_match.group(1)


async def build_think(article: str) -> str:
    thinking, _answer = await aget_response(
        prompt=prompt_think.format(prompt_example1=article)
    )
    _thinking, answer = await aget_response(
        prompt=prompt_think_fix.format(comment=thinking),
        model="google/gemini-flash-1.5",
    )
    fixed_match = re.search(r"<Think>\s*(.*?)\s*</Think>", answer, re.DOTALL)
    if not fixed_match:
        raise ValueError("Failed to extract think from response")
    return fixed_match.group(1)


async def build_pipeline() -> tuple[str, str, str]:
    topic, content = await clone_article()
    think = await build_think(article=content)
    return topic, think, content


if __name__ == "__main__":
    import asyncio

    topic, think, content = asyncio.run(build_pipeline())
    print(topic)
    print(think)
    print(content)
