
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import time
from matplotlib import animation
import math
with st.echo(code_location='below'):
      df = pd.read_csv(r"fide_historical.csv")
      st.title("Топ-100 шахматистов  2000-2017")
      if st.checkbox("Смешной котик", False):
            st.markdown(
                  "![](https://media4.giphy.com/media/DAmosupuFkPjG/giphy.gif?cid=ecf05e470gqrj7ki2xa870se1yaeb0bz6mbg842fhwwikeeq&rid=giphy.gif)")


      st.header("Таблица в выбранную дату")
      datetime = pd.to_datetime(df["ranking_date"], errors = 'coerce')

      y = st.selectbox("Выберите год", range(2000, 2018),1)
      def mfixed(y):
            monthspool = []
            for months in range(0, 13):
                  testdata = df[(datetime.dt.year == y) & (datetime.dt.month == months)]
                  if testdata.empty:
                        months += 1
                  else:
                        monthspool.append(months)
            return monthspool

      m = st.selectbox("Выберите месяц", mfixed(y))
      data = df[(datetime.dt.year == y) & (datetime.dt.month == m)]
      st.write(data)

      #ПЕРСОНАЛЬНЫЙ
      st.header("Персональный тренд")
      all_names = df["name"].unique()
      user_input = st.text_input("Введите фамилию и имя шахматиста через запятую")
      if  user_input:
            sli = st.slider('Выберите промежуток времени', 2000, 2017, (2000, 2017))
            person = df.loc[df['name'] == user_input]
            datetime = pd.to_datetime(person["ranking_date"], errors='coerce')
            capp = person[(datetime.dt.year >= sli[0]) & (datetime.dt.year <= sli[1])]
            print(capp)
            daterank = capp[['ranking_date', 'rating']]
            pers_chart = alt.Chart(daterank).mark_line().encode(
                  alt.X('ranking_date', scale = alt.Scale(zero=False)),
                  alt.Y('rating', scale = alt.Scale(zero=False))


            ).configure_line(
                  opacity = 1,
                  color = 'purple'
            )

      #Carlsen, Magnus
            st.write(pers_chart)

      #КОНЕЦ ПЕРСОНАЛЬНОГО

      #ПИРОЖОК
      st.header("Гроссмейстеры и где они обитают")
      sl = st.slider("Выберите год", 2000, 2017)
      dictdata = {}
      datetime = pd.to_datetime(df["ranking_date"], errors = 'coerce')
      newdata = df[datetime.dt.year == sl]
      for rows in newdata["country"]:
            count = 1
            if rows not in dictdata:
                  dictdata["{}".format(rows)] = count
            else:
                  dictdata["{}".format(rows)] += 1
      st.subheader("ТОП-10 стран, к которым принадлежат гроссмейстеры")
      newdf = pd.DataFrame(list(dictdata.items()), columns = ["country", "GMs"])
      stolbiki = go.Figure( data = [])
      pie = px.pie(newdf, values = newdf["GMs"][:10], names = newdf["country"][:10])
      st.plotly_chart(pie)
      #ПИРОЖОК ЗАКОНЧЕН

      if st.checkbox("Хочу посмотреть ТОП-5", False):

            sli = st.slider('Выберите промежуток времени, чтобы увидеть, как менялся ТОП-5', 2000, 2017, (2000, 2017))
            years = []
            for i in range(sli[0], sli[1] + 1):
                  years.append(i)
            print(years)
            datetime = pd.to_datetime(df["ranking_date"], errors='coerce')

            def barlist(sli):
                  C = []
                  for year in range (sli[0], sli[1] + 1):

                        topfive = df[datetime.dt.year == year][:5][['rating','name']]
                        print()
                        C.append(topfive)
                  return C

            def animate(i, year):
                  bars = alt.Chart(i, title="ТОП-5 на {} год".format(year)).mark_bar().encode(
                        alt.X('rating', axis=alt.Axis(title='Рейтинг'),
                              scale = alt.Scale(zero=False)),
                        alt.Y('name', axis=alt.Axis(title=''),
                              scale = alt.Scale(zero=False)),
                        color=alt.Color('name:N')).properties(
                        width=500,
                        height=400
                  )
                  st.write(bars)
            i = 0
            for datas in barlist(sli):
                  animate(datas, years[i])
                  i+=1
                  time.sleep(0.05)

      if st.checkbox("Хочу посмотреть соотношение возраста и рейтнига игроков", False):

            rankdatee = pd.to_datetime(df["ranking_date"], errors = 'coerce')
            birthdate = df["birth_year"]
            rankdate = rankdatee.dt.year
            agelist = []
            for year in range(2000, 2018):
                  testdata = df[(rankdate == year)]
                  pass
            rodilis = df['birth_year'].values
            rate = df['rating'].values
            daterate = rankdate.values
            vozrast = daterate - rodilis
            bil = []
            resdict = {}
            for i in range(11511):
                  tempsum = 0
                  count = 0
                  if vozrast[i] not in bil:
                        bil.append(vozrast[i])
                        for x in range(11511):
                              if vozrast[x] == vozrast[i]:
                                    count+=1
                                    tempsum += rate[x]
                                    meansum = tempsum / count

                        resdict[vozrast[i]] = math.floor(meansum)
                        meansum = 0

            sortdict = dict(sorted(resdict.items()))
            print(sortdict.values())
            print(sortdict.keys())
            znacheniya = list(sortdict.values())
            goda = list(sortdict.keys())
            mean = sum(znacheniya)/len(znacheniya)
            fig = plt.figure()
            plt.bar(goda,znacheniya, width=0.8)
            plt.ylim([2400, 2800])
            plt.axhline(y=mean, color='r', linestyle='-')
            plt.ylabel('Рейтинг игроков')
            plt.xlabel('Возраст игроков')
            st.write(fig)


