# Importación de plataformas
import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

# Base de datos a utilizar
emp_data = pd.read_csv('https://raw.githubusercontent.com/cindylozano/DataScienceTLG/Streamlit/Employee_data.csv')

# Lista de las columnas identificadas para conservar en análisis
columns_to_keep = ['name_employee', 'performance_score', 'salary', 'position', 
                   'average_work_hours', 'birth_date', 'gender', 'marital_status',
                   'hiring_date', 'satisfaction_level', 'last_performance_date', 
                   'absences', 'age']

emp_data = emp_data[columns_to_keep]

# Variables iniciales
initial_gender = None
initial_score = (float(emp_data['performance_score'].min()), float(emp_data['performance_score'].max()))
initial_marital_status = None

# Variables para almacenar selecciones
selected_gender = initial_gender
selected_score = initial_score
selected_marital_status = initial_marital_status
min_selected_score, max_selected_score = selected_score

# Despliegue de un título y una breve descripción de la aplicación web
st.title('Desempeño de colaboradores Marketing')
st.markdown('Esta es una aplicación web que muestra el análisis del desempeño de los colaboradores del área de Marketing de Socialize your Knowledge. :brain::bulb::bar_chart:')
 
# Despliegue del logotipo de la empresa en la aplicación web
logo = ('https://raw.githubusercontent.com/cindylozano/DataScienceTLG/Streamlit/SYN_logo.png')
st.sidebar.image(logo, use_column_width=True)

# Encabezado de los filtros
st.sidebar.write('Panel de filtros')

# Despliegue de un control para seleccionar el género del empleado
selected_gender = st.sidebar.radio('Selecciona el género:', emp_data['gender'].unique(), index=None if initial_gender is None else emp_data['gender'].to_list().index(initial_gender))
st.sidebar.write(f'Género seleccionado: {selected_gender!r}' if selected_gender else 'Género seleccionado: None')

# Despliegue de un control para seleccionar un rango del puntaje de desempeño del empleado
selected_score = st.sidebar.slider('Selecciona rango del puntaje de desempeño:',
                               min_value=float(emp_data['performance_score'].min()),
                               max_value=float(emp_data['performance_score'].max()),
                               value=(selected_score[0], selected_score[1])
                               )
min_selected_score, max_selected_score = selected_score
st.sidebar.write(f'Rango de desempeño seleccionado: {min_selected_score!r} - {max_selected_score!r}' if min_selected_score != selected_score[0] or max_selected_score != selected_score[1] else 'Rango de desempeño seleccionado: None')

# Despliegue de un control para seleccionar el estado civil del empleado
selected_marital_status = st.sidebar.selectbox('Selecciona estado civil:', emp_data['marital_status'].unique(), index=None if initial_marital_status is None else emp_data['marital_status'].to_list().index(initial_marital_status))
st.sidebar.write(f'Estado civil seleccionado: {selected_marital_status!r}' if selected_marital_status else 'Estado civil seleccionado: None')

# Botón para restablecer filtros
reset_button = st.sidebar.button('Restablecer Filtros')

# Restablecer filtros si el botón ha sido presionado
if reset_button:
    selected_gender = initial_gender
    selected_score = initial_score
    selected_marital_status = initial_marital_status
    min_selected_score, max_selected_score = selected_score
  
# Dataframe filtrado por los controles
filtered_data = emp_data.copy()
if selected_gender:
    filtered_data = filtered_data[filtered_data['gender'] == selected_gender]
if selected_marital_status:
    filtered_data = filtered_data[filtered_data['marital_status'] == selected_marital_status]
if selected_score:
    filtered_data = filtered_data[(filtered_data['performance_score'] >= min_selected_score) & 
                               (filtered_data['performance_score'] <= max_selected_score)]

# Gráfico de la distribución de los puntajes de desempeño
fig_score = px.histogram(filtered_data, x='performance_score', color_discrete_sequence=px.colors.qualitative.T10)
fig_score.update_layout(
        xaxis_title='Puntaje de desempeño',
        yaxis_title='Colaboradores',
        title='Distribución de los puntajes de desempeño'
        )
st.plotly_chart(fig_score, use_container_width=True)

# Gráfico del promedio de horas trabajadas por el género del empleado
fig_hours = px.box(filtered_data, x='gender', y='average_work_hours', color='gender', color_discrete_sequence=px.colors.qualitative.T10)
fig_hours.update_layout(
        xaxis_title='Género del colaborador',
        yaxis_title='Promedio de horas',
        title='Promedio de horas trabajadas por género'
        )
st.plotly_chart(fig_hours, use_container_width=True)

# Gráfico de la edad de los empleados con respecto al salario de los mismos
fig_age_salary = px.histogram(filtered_data, x='age', y='salary', nbins=8, color_discrete_sequence=px.colors.qualitative.T10)
fig_age_salary.update_layout(
    xaxis_title='Edad del colaborador',
    yaxis_title='Salario del colaborador',
    title='Relación de la edad y salario del colaborador'
    )

st.plotly_chart(fig_age_salary, use_container_width=True)

# Gráfico de la relación del promedio de horas trabajadas versus el puntaje de desempeño
min_avg_work_hours = emp_data['average_work_hours'].min()
max_avg_work_hours = emp_data['average_work_hours'].max()

fig_hours_score = alt.Chart(filtered_data).mark_circle(filled=True).encode(
                      alt.X('average_work_hours',
                        scale=alt.Scale(domain=(min_avg_work_hours, max_avg_work_hours)),
                        title='Promedio de horas'),
                      alt.Y('performance_score:O',
                        scale=alt.Scale(type='ordinal'),
                        title='Puntaje de desempeño'),
                      alt.Color('gender'),
                      tooltip = [alt.Tooltip('name_employee'),
                            alt.Tooltip('gender'),
                            alt.Tooltip('position')
                            ]
                      ).properties(title='Relación del desempeño y las horas trabajadas')
st.altair_chart(fig_hours_score, use_container_width=True)

# Conclusión del análisis
st.header('Conclusión del análisis')
st.write('De acuerdo con el análisis realizado se observa que el puntaje de desempeño de los colaboradores se encuentra en su mayoría alrededor de un 3 de calificación. El promedio de horas trabajadas por género es ligeramente mayor en las colaboradoras. Respecto al rango salarial, se observa que los colaboradores de entre 30-39 años de edad son en quienes se concentra el mayor presupuesto. Finalmente, respecto al desempeño y horas trabajadas, no hay colaboradores con más de 4,472 horas que muestren bajo desempeño (1).')