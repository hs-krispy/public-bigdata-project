## EDA

#### 최근 5개년 서울시 교통사고 현황

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rc('font', family="Malgun Gothic")
plt.rcParams.update({'font.size': 13})

file = pd.read_csv(file_path, sep="\t", index_col=0, encoding="UTF-8",
                   names=["지역", "발생건수", "자동차 1만대당 발생건수", "사망자수", "인구 10만명당 사망자수", "부상자수", "인구 10만명당 부상자수"])

file.drop(columns=["부상자수", "인구 10만명당 부상자수", "자동차 1만대당 발생건수", "인구 10만명당 사망자수"], inplace=True)
file = file[file.지역 == "합계"]
print(file)
#         지역    발생건수 사망자수
# 2016.0  합계  40,039  348
# 2017.0  합계  38,625  343
# 2018.0  합계  38,795  304
# 2019.0  합계  39,258  250
# 2020.0  합계  35,227  219

file.index = range(2016, 2021)
file["발생건수"] = file["발생건수"].str.replace(",", "")
colors = ["blue", "orange"]
titles = ["사고건수", "사망자"]
ext = ["건", "명"]
fig, axes = plt.subplots(2, 1, figsize=(12, 17), constrained_layout=True)
for idx, (ax, c, t, e) in enumerate(zip(axes.flatten(), colors, titles, ext)):
    fig = file.iloc[:, [idx + 1]].astype(np.int32).plot.bar(rot=0, legend=False, title=f"서울시 연도별 교통사고 현황 ({t})", ax=ax, color=c)
    file.iloc[:, [idx + 1]].astype(np.int32).plot(ax=ax, use_index=False, color=c, legend=False)
    for patch in fig.patches:
        fig.annotate(round(patch.get_height()), (patch.get_x() + patch.get_width() / 2, patch.get_height()),
                     ha='center', va='center', size=12, xytext=(-1, 8), textcoords='offset points')
    ax.set_ylabel(f"({e})", rotation=0, labelpad=15)
    ax.set_xlabel("(연도)")
plt.show()
```

- 최근 5년동안 발생한 서울시내 교통사고 발생빈도와 사망자 수
- 사고건수가 계속해서 감소하는 모습을 보이다가 2020년에 대폭 감소
  - 사고건소의 감소로 인해 자연스럽게 사망자도 감소

<img src="https://user-images.githubusercontent.com/58063806/128025855-68b3a17b-e07f-4f65-bc56-50ef5d172c1c.png" width=70% />

```python
df = pd.DataFrame({"사고건수": [3114, 3196, 3331, 4064, 4016],
                   "사망자수": [48, 45, 35, 43, 41],
                   "중상자수": [958, 976, 986, 1142, 1098]},
                  index=range(2016, 2021))

fig = df.plot.bar(grid=True, title="서울시 연도별 이륜차 교통사고현황", figsize=(12, 7))
df.plot(ax=fig, linestyle="solid", use_index=False, legend=False)
fig.set_xlabel("(연도)")
for bar in fig.patches:
    fig.annotate(round(bar.get_height()),
                       (bar.get_x() + bar.get_width() / 2,
                        bar.get_height()), ha='center', va='center',
                       size=10, xytext=(-1, 8),
                       textcoords='offset points')
plt.show()
```

- 최근 5년동안 발생한 서울시내 이륜차 교통사고 발생빈도와 사망자, 중상자 수
- 하지만 이륜차의 경우는 교통사고의 경향과는 달리 사고건수가 계속해서 증가하는 모습을 보임
  - 사망자는 큰 차이없음

<img src="https://user-images.githubusercontent.com/58063806/128026270-327257b5-3468-4e86-957d-d34490ab7e39.png" width=70% />



#### 서울시 구별 교통사고 위험지수 (ARI)

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rc("font", family="Malgun Gothic")
df = pd.read_excel(file_path)

df.drop(index=0, inplace=True)
df = df[df.시도 == "서울"]
df["사고건수 합"] = df["2018"] + df["2019"] + df["2020"]
df["KSI"] = df.iloc[:, 2:-1].sum(axis=1) - df["사고건수 합"]
df.drop(index=2, columns=["시도"], inplace=True)
df.columns = ["시군구", "2018(사고건수)", "2018(사망자)", "2018(중상자)",
              "2019(사고건수)", "2019(사망자)", "2019(중상자)", "2020(사고건수)", "2020(사망자)", "2020(중상자)", "사고건수 합", "KSI"]
df["ARI"] = df["KSI"] ** 2 + df["사고건수 합"] ** 2
df["ARI"] = df["ARI"].transform(lambda x: np.sqrt(x))
df.to_excel("서울시 구별 ARI.xlsx", index=False, encoding="CP949")

df = pd.read_excel("서울시 구별 ARI.xlsx")
color = ["grey"] * df.shape[0]
df.sort_values(by="ARI", axis=0, inplace=True)
color[0] = "red"
color[-1] = "blue"
fig = df["ARI"].plot.bar(figsize=(15, 8), title="서울시 구별 교통사고 위험지수", color=color)
for idx, bar in enumerate(fig.patches):
    if idx == 0 or idx == df.shape[0] - 1:
        fig.annotate(round(bar.get_height()), (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                     ha='center', va='center', size=12, xytext=(-1, 8), textcoords='offset points')
plt.xticks(range(25), df["시군구"].values, rotation=45)
plt.show()
```

- KSI : 사망자 + 중상자 수
- ARI : sqrt(KSI<sup>2</sup> + 사고건수<sup>2</sup>) / n(연도수)
- 강남구가 가장 높은 ARI

<img src="https://user-images.githubusercontent.com/58063806/128029126-a7e044de-a408-4056-a02f-6c88a94ac122.png" width=90% />

#### 서울시 지점, 시간대별 교통량 

```python
import pandas as pd
import re
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
plt.rc("font", family="Malgun Gothic")
df = pd.read_excel("C:/Users/user/Desktop/프로젝트/06월 서울시 교통량 조사자료.xlsx", sheet_name="2021년 06월")

# 차량전용도로는 제외
match = df["지점명"].apply(lambda x: re.search(r"분당수서로|우면산로|신월여의지하도로|강남순환로|올림픽대로|강변북로|제물포길|양재대로|서부간선|동부간선|내부순환로|북부간선|언주로|IC|고속도로", str(x)))
filtered = match.apply(lambda x: x is None)
df = df.loc[filtered, :]
Mean = df.pivot_table(df.columns[6:], index="지점명", aggfunc="mean")
Sum = df.pivot_table(df.columns[6:], index="지점명", aggfunc="mean").sum(axis=1)
fig, axes = plt.subplots(3, 3, figsize=(15, 15), constrained_layout=True)
res = Mean.div(Sum, axis=0)
res["sum"] = Sum
res.sort_values(by="sum", ascending=False, inplace=True)
# 0 ~ 23시
res = res.loc[:, df.columns[6:]]
# 상위 11개 대교 제외하고 차상위 9개 구간
for i, ax in enumerate(axes.flatten()):
    ax.set_title(res.index[11 + i])
    ax.plot(range(24), [1 / 24] * 24, "r--")
    res.iloc[11 + i, :].plot.bar(ax=ax, rot=45)

plt.show()
```

<img src="https://user-images.githubusercontent.com/58063806/128717256-342a7f26-c2ea-4255-aa67-5a8c2d030b53.png" width=100% />

#### 시간대별 이륜차 사고 비율

```python
import pandas as pd
import matplotlib.pyplot as plt

plt.rc("font", family="Malgun Gothic")
plt.figure(figsize=(15, 8))
df = pd.read_excel("C:/Users/user/Desktop/프로젝트/서울시 동별 이륜차 사고건수 (2017~2019).xlsx")
df["사고일시"] = df["사고일시"].apply(lambda x: x.split(" ")[3])
p_df = df["사고일시"].value_counts() / df.shape[0]
print(p_df.cumsum())
q1 = p_df[p_df.cumsum() > 0.25].index[0]
q2 = p_df[p_df.cumsum() > 0.5].index[0]
q3 = p_df[p_df.cumsum() > 0.75].index[0]
q1_index = p_df.index.tolist().index(q1)
q2_index = p_df.index.tolist().index(q2)
q3_index = p_df.index.tolist().index(q3)
plt.plot(range(q1_index, 24), [p_df[p_df.index == q1]] * (24 - q1_index), "r--")
plt.text(14, p_df[p_df.index == q1], "over 25%", fontdict={"fontsize" : "x-large", "fontfamily": "Malgun Gothic"})
plt.plot(range(q2_index, 24), [p_df[p_df.index == q2]] * (24 - q2_index), "r--")
plt.text(14, p_df[p_df.index == q2], "over 50%", fontdict={"fontsize" : "x-large", "fontfamily": "Malgun Gothic"})
plt.plot(range(q3_index, 24), [p_df[p_df.index == q3]] * (24 - q3_index), "r--")
plt.text(14, p_df[p_df.index == q3], "over 75%", fontdict={"fontsize" : "x-large", "fontfamily": "Malgun Gothic"})
p_df.plot.bar(rot=45)
plt.title("시간별 이륜차 사고 비율")
plt.show()
```

<img src="https://user-images.githubusercontent.com/58063806/128716699-f5aa7420-c501-48cf-bead-479860262ec3.png" width=90% />

