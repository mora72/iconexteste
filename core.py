import mysql.connector
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from selenium import webdriver

connection = mysql.connector.connect(host='127.0.0.1', port='3308', user='root', password='',
                                     database='numbers', charset='utf8mb4')

query = "select * from core_filmes"

frame = pd.read_sql(query, connection)
# pd.set_option('display.expand_frame_repr', False)
# print(frame)
# frame['genero'].value_counts(0)

frame['rec'] = frame.receita / 1000000
frame2 = frame[frame.ano >= 2000].groupby(by='genero').sum().sort_values('rec', ascending=False)
# plt.figure(figsize=(19,9))
frame3 = frame2.head(5)
sns.barplot(x=frame3.index, y=frame3['rec'])
plt.savefig('imgbase.png')
qtde = frame[frame.ano == 2020].count()['id']
receita = frame[frame.ano == 2020].sum()['rec']

with open('base.html', 'r') as file:
    conteudo = file.read()

conteudo = conteudo.replace('XXX', str(qtde))
conteudo = conteudo.replace('YYY', f'{receita:10,.2f}')

with open('basefim.html', 'w') as file:
    file.write(conteudo)

htmlresult = webdriver.Firefox()
htmlresult.get('file:///C:/Users/carlo/PycharmProjects/iconexteste/basefim.html')
htmlresult.save_screenshot('pastaimg/basefim.png')
htmlresult.quit()
