import streamlit as st
import plotly.express as px
import pandas as pd

def top_n_emitters(df, year, nb_displayed=10):
    
    #years filter
    result = df[df['Year'] == year]  
    
    #sort the values and keep nb_displayed
    result = result.sort_values(by='CO2 Per Capita (metric tons)', ascending=False)
    result = result.head(nb_displayed)
    
    #create the fig
    fig = px.bar(result, x='Country Name', y='CO2 Per Capita (metric tons)', title=f'Top {nb_displayed} CO2 per capita emitters in {year}')
    
    #return the fig
    return fig

def main():

    st.title('Which countries have the highest CO2 per capita emissions ?')

    df = pd.read_csv('/home/mathieujayet/code/matjayet/student-challenges/curriculum/03-Data-Analysis/06-Dashboards-with-Dash-Plotly/data/CO2_per_capita.csv', sep=';')

    year = st.slider('Choose the year', int(df['Year'].min()), int(df['Year'].max()), int(df['Year'].mean()))
    
    nb_displayed = st.selectbox('How many countries do you want to include ?', [3,5,10,20,30], index=2)

    fig_bar = top_n_emitters(df, year, nb_displayed)
    st.plotly_chart(fig_bar)

    fig_scatter = px.scatter_geo(df[df['Year']==year].dropna(subset=["CO2 Per Capita (metric tons)"]), 
    locations="Country Code",
    hover_name="Country Name",
    color="CO2 Per Capita (metric tons)",
    size="CO2 Per Capita (metric tons)",
    title=f'CO2 per capita emissions in {year}',
    projection="natural earth")

    fig_scatter.update_layout(#showlegend=False,
                            title={'font': {'size': 20},
                            'y':0.9,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'},
                            coloraxis_showscale=True,
                            coloraxis_colorbar=dict(
                            title={'text': 'CO2 Per Capita (metric tons)',
                            'side' : 'bottom'},  # Optional: Title for the color legend
                            # tickvals=[df_mean['CO2 Per Capita (metric tons)'].min(), df_mean['CO2 Per Capita (metric tons)'].max()],  # Optional: Set ticks for the color scale
                            #ticktext=["Low", "High"],  # Optional: Customize tick labels
                            tickfont=dict(size=12),  # Optional: Set font size for ticks
                            #x=1.05,  # Position the colorbar to the right (values > 1 move it outside the plot area)
                            y=0, # Keep it vertically centered
                            #xanchor='left',
                            yanchor="top",  # Anchor it in the middle vertically
                            tickangle=45 , # Optional: Set the angle of tick labels,
                            orientation='h'
    ))
    st.plotly_chart(fig_scatter)
if __name__ == '__main__':
    main()