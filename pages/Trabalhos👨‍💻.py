from turtle import width
import pandas as pd
import plotly.express as px
import streamlit as st


def make_columns(number_cols, images_array, user_names=None):
    if number_cols != len(images_array):
        raise ValueError("The arrays and columns must be the same size")
    
    cols = st.columns(number_cols)

    for i in range(len(images_array)):
        with cols[i]: 
            user_name = user_names[i].split("/")
            user_name = user_name[-1]
            st.image(images_array[i], use_column_width = True)    
            st.markdown(f"[{user_name}]({user_names[i]})")

def show_code(toogle_boolean, code):
    if toogle_boolean: 
        st.code(code)
    
def update_the_axis(plot, title_x,title_y):
    plot.update_xaxes(title_text = title_x)
    plot.update_yaxes(title_text = title_y)

st.title("*The Dream team*")

df = pd.read_csv("./data/vgsales.csv")

images = ["https://avatars.githubusercontent.com/u/72263429?v=4", "https://avatars.githubusercontent.com/u/64994893?v=4", "https://avatars.githubusercontent.com/u/105646257?v=4"] #Imagens para exibir em tela

the_boys = ["https://github.com/hermeson883", "https://github.com/gabrielsoares40940","https://github.com/victordsl"] # Imagens do github do pessoal

make_columns(3, images, the_boys) # Função para automatizar a criação de colunas


st.divider()
st.markdown("""
    > **Gostaria, primeiramente, de deixar meus agradecimentos aos meus amigos acima que me ajudaram a desenvolver os projetos listados aqui. Sem eles, certamente não seria possivel cumprir o projeto apresentado aqui com a qualidade, empenho e carinho demonstrados aqui.**
""")
st.divider()

st.header("*Tópicos de Big Data*")

st.write("""Para começar, um dos projeto mais divertidos e interessantes que tivemos que fazer ao longo desse ano com certeza foi a cadeira de Topicos de Big Data com python, onde tivemos a oportunidades de conhecer varias ferramentas e conceitos voltados para a análise de dados como:  """)

st.write("""
    1. [:violet[Pandas]](https://spark.apache.org/docs/latest/api/python/index.html)
    2. [:orange[PySpark]](https://spark.apache.org/docs/latest/api/python/index.html)
    3. [Smtplib](https://docs.python.org/3/library/smtplib.html)
    4. [:rainbow[5V's]](https://acuvate.com/blog/understanding-the-5vs-of-big-data/)
""")

st.write("""
    Ao final do semestre tivemos que realizar uma projeto final envolvendo uma análise exploratoria de dados em algum dataset do <a href="https://www.kaggle.com/datasets/gregorut/videogamesales" style="color: rgb(32, 190, 255);">Kaggle</a>.  
    Nossas escolha foi para uma base de dados chamada de **'video game sales'**, onde há varios registros envolvendo jogos de diversas empresas e entre varios anos de lançamento fora também os registros das vendas em varias partes do mundo.
""", unsafe_allow_html=True)

st.header("*Video Game Sales* :video_game::joystick:")

if st.button("Click em mim!!!", help="Show database"):
    st.divider()
    st.dataframe(df.style.format({
        "Year": "{:.0f}"
    }))
    st.divider()

st.header("*Pegando os valores únicos*")
st.write("""
    Uma das primeiras coisas que fizemos foi verificar a quantidade de plataformas que teriamos que lidar. O resultado veremos a seguir:
""")


unique_values = df["Platform"].unique()
unique_values = pd.DataFrame(unique_values, columns = ["Consoles"])
anos_unicos = pd.DataFrame(df["Year"].unique(), columns=["Anos"])
st.write(unique_values)

st.write("""
    O mesmo se aplica para os anos: 
""")

st.dataframe(anos_unicos.style.format({
    "Anos" : "{:.0f}"
}))

st.header("*Gráficos* :bar_chart:")
st.write("""
    Feito mais alguns tratamentos e explorações em volta da base começamos a fazer o que mais queriamos que era os **gráficos**.  
    Para tal usamos a lib **[plotly express](https://plotly.com/python/)** pela sua capacidade de gerar gráficos belos e riquíssimos em detalhes.
""")


fig = px.histogram(df, x="Platform",
             y = 'Global_Sales',
             color = "Platform")
fig.update_layout(title_text='Consoles mais vendidos em todo mundo (Em milhões)', title_x=0.2, autosize=True)


update_the_axis(fig,title_x="vendas Globais", title_y="Plataforma")

st.plotly_chart(fig, use_container_width=True)

on_off = st.toggle("Show me the code!")

show_code(on_off, """
    fig = px.histogram(df, x="Platform",
                y = 'Global_Sales',
                color="Platform")
    fig.update_layout(title_text='Consoles mais vendidos em todo mundo (Em milhões)', title_x=0.2, yaxis_title="Vendas globais", xaxis_title = "Console")""")


platform_global_sales = df.groupby(['Publisher'], as_index=False)['Global_Sales'].sum()

platform_global_sales = platform_global_sales.sort_values(by = 'Global_Sales', ascending=False).head(10)

st.header("""
    *Quem mais vendeu?*
""")

fig2 = px.histogram(
    x=platform_global_sales['Publisher'],
    y = platform_global_sales['Global_Sales'],
    title="Top 10 empresas que mais venderam jogos",
    color = platform_global_sales["Publisher"],
)

update_the_axis(fig2, title_y="Faturamento global", title_x="Empresas que mais venderam")

fig2.update_layout(title_x=0.2)

st.plotly_chart(fig2, use_container_width=True)


top_10_enterprise_sales_show = st.toggle("Show me the code!!")

show_code(top_10_enterprise_sales_show, """platform_global_sales = df.groupby(['Publisher'], as_index=False)['Global_Sales'].sum()

platform_global_sales = platform_global_sales.sort_values(by = 'Global_Sales', ascending=False).head(10)

fig = px.histogram(
    x=platform_global_sales['Publisher'],
    y = platform_global_sales['Global_Sales'],
    title="Top 10 empresas que mais venderam jogos",
    color = platform_global_sales["Publisher"],
)

fig.update_layout(yaxis_title="Faturamento global", xaxis_title = "Empresas que mais venderam",  title_x=0.5)

fig.show()""")


st.header("""
    *Qual gênero foi mais jogado?*
""")



plot_genrer = df.loc[df["Genre"].isin(["Action","Sports","Shooter","Role-Playing","Racing"])]
plot_genrer = plot_genrer.groupby(["Genre", "Year"], as_index=False)["Global_Sales"].sum()
line_plot = px.line(plot_genrer, x = "Year", y = 'Global_Sales', color = 'Genre', title='Generos de jogos mais vendidos')

update_the_axis(line_plot, title_x="Anos", title_y="Vendas Globais")

st.plotly_chart(line_plot, use_container_width=True)

genre_toggle = st.toggle("Show me the code!!!")
show_code(genre_toggle, """
plot_genrer = df.loc[df["Genre"].isin(["Action","Sports","Shooter","Role-Playing","Racing"])]
plot_genrer = plot_genrer.groupby(["Genre", "Year"], as_index=False)["Global_Sales"].sum()
line_plot = px.line(plot_genrer, x = "Year", y = 'Global_Sales', color = 'Genre', title='Generos de jogos mais vendidos')
st.write(line_plot)
""")

st.header("*Qual foi o jogo que mais vendeu?*")

st.write("""
    Talvez a pergunta mais feita por nós com certeza foi está: "Tá mais e aí? qual jogo mais vendeu? Foi da Sony ou Microsoft?" **Porém...** ,para nossa, supresa quem mais vendeu foi um jogo da **Nintendo**. Mas você pode falar o seguinte: "Foi então o Super Mario ou Zelda ou então Donkey Kong?"  A resposta para todas essas peguntas segue sendo não! Pois o jogo mais vendido de **todos os tempos** na verdade é o [Wii sports](https://www.denofgeek.com/games/wii-sports-best-selling-nintendo-game-ever-explained-retrospective/).
""")

most_saled_game = px.bar(df.head(10), x="Rank", y="Global_Sales",color="Platform", hover_data=["Name"], title="Top 10 jogos mais vendidos")

most_saled_game.update_yaxes(title_text="Vendas Globais")


expander = st.expander("Mas por quê?")
expander.write("""
    O motivo para que o **'Wii Sports'** seja o jogo mais vendido de todos se deve ao fato de que ele era um jogo que já vinha com o console na hora da sua compra, então esse fator acaba por inflacionar MUITO os números de um jogo de sports que é um mercado 'nichado', ou seja, destinado a um publico em específico, além da simplicidade do Wii Sports comparado a outros grandes titulos da empresa.

    > Wii sports se torna o jogo mais 'vendido' de todos os tempos https://www.nintendoblast.com.br/2009/05/wii-sports-se-torna-o-jogo-mais-vendido.html  
      Why Wii Sports Is the Best-Selling Nintendo Game Ever https://www.denofgeek.com/games/wii-sports-best-selling-nintendo-game-ever-explained-retrospective/
""")
    

st.header("Conclusão...")

st.write("""
    Bom esse só foi um pedacinho de todo o nosso trabalho que tivemos que fazer ao longo de todo o semestre caso tenha se interessado poderá ver o nosso [github](https://github.com/hermeson883/Big_Data_Work/blob/main/Games_sales.ipynb) para ter acesso a **TODO** o código fonte que foi mostrado (e não mostrado 😅) aqui.
""")

st.header("Bibliografia")

st.markdown("""
    1. [Streamlit emoji shortcodes](https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app)

    2. [Streamlit documentation](https://docs.streamlit.io)

    3. [Plotly Python Graphing Library](https://plotly.com/graphing-libraries/)

    4. [Pandas](https://pandas.pydata.org/pandas-docs/stable/reference/frame.html)
""")