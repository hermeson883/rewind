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

st.title("*The Dream team*")
images = ["https://avatars.githubusercontent.com/u/72263429?v=4", "https://avatars.githubusercontent.com/u/64994893?v=4", "https://avatars.githubusercontent.com/u/105646257?v=4"] #Imagens para exibir em tela

the_boys = ["https://github.com/hermeson883", "https://github.com/gabrielsoares40940","https://github.com/victordsl"] # Imagens do github do pessoal

make_columns(3, images, the_boys) # Função para automatizar a criação de colunas


st.divider()
st.markdown("""
    > **Gostaria, primeiramente, de deixar meus agradecimentos aos meus amigos acima que me ajudaram a desenvolver os projetos listados aqui. Sem eles, certamente seria possivel cumprir os projetos apresentados aqui com a qualidade e empenho demonstrados aqui.**
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
    Nossas escolha foi para uma base de dados chamada de **'video game sales'**, onde há varios registros envolvendo jogos de diversas plataformas e entre varios anos de lançamento fora também os registros das vendas em varias partes do mundo.
""", unsafe_allow_html=True)

st.header("*Video Game Sales* 🎮:joystick:")
df = pd.read_csv("./data/vgsales.csv")

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
st.dataframe(unique_values)

st.write("""
    O mesmo se aplica para os anos: 
""")

st.dataframe(anos_unicos.style.format({
    "Anos" : "{:.0f}"
}))

st.header("*Gráficos* :bar_chart:")
st.write("""
    Feito mais alguns tratamentos na base começamos a fazer o que mais queriamos que era os **gráficos**.  
    Para tal usamos o **[plotly express](https://plotly.com/python/)** pela sua capacidade de gerar gráficos belos e riquíssimos em detalhes.
""")


fig = px.histogram(df, x="Platform",
             y = 'Global_Sales',
             color="Platform")
fig.update_layout(title_text='Consoles mais vendidos em todo mundo (Em milhões)', title_x=0.2, yaxis_title="Vendas globais", xaxis_title = "Console")

st.plotly_chart(fig)
on = st.toggle("Show me the code!")
show_code(on, """
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

fig2.update_layout(yaxis_title="Faturamento global", xaxis_title = "Empresas que mais venderam",  title_x=0.2)

st.plotly_chart(fig2)


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
st.write(line_plot)

genre_toggle = st.toggle("Show me the code!!!")
show_code(genre_toggle, """
plot_genrer = df.loc[df["Genre"].isin(["Action","Sports","Shooter","Role-Playing","Racing"])]
plot_genrer = plot_genrer.groupby(["Genre", "Year"], as_index=False)["Global_Sales"].sum()
line_plot = px.line(plot_genrer, x = "Year", y = 'Global_Sales', color = 'Genre', title='Generos de jogos mais vendidos')
st.write(line_plot)
""")


st.header("Conclusão...")

st.write("""
    Bom esse só foi um pedacinho de todo o noss trabalho que tivemos que fazer ao longo de todo o semestre caso tenha se interessado poderá ver o nosso github para ter acesso a **TODO** o código fonte que foi mostrado (e não mostrado 😅) aqui.
""")

st.header("Bibliografia")

st.markdown("""
    1. [Streamlit emoji shortcodes](https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app)

    2. [Streamlit documentation](https://docs.streamlit.io)

    3. [Plotly Python Graphing Library](https://plotly.com/graphing-libraries/)

    4. [Pandas](https://pandas.pydata.org/pandas-docs/stable/reference/frame.html)
""")
