# S2.1: Import the necessary Python modules and create the 'prediction()' function as directed above.
# Importing the necessary Python modules.
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, mean_squared_log_error
# Define the 'prediction()' function.
@st.cache()

def prediction(car_df, car_width, engine_size, horse_power, drive_wheel_fwd, car_company_buick):
    X = car_df.iloc[:,:-1]
    y = car_df['price']
    X_train, X_test, y_train, y_test =train_test_split(X,y,test_size=0.3,random_state=42) 

    lin_reg = LinearRegression()
    lin_reg.fit(X_train,y_train)
    score = lin_reg.score(X_train,y_train)

    price = lin_reg.predict([[car_width, engine_size, horse_power, drive_wheel_fwd, car_company_buick]])
    price = price[0]

    y_test_pred = lin_reg.predict(X_test)
    test_r2_score = r2_score(y_test,y_test_pred)
    test_mae = mean_absolute_error(y_test,y_test_pred)
    test_msle = mean_squared_log_error(y_test,y_test_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test,y_test_pred))

    return price,score,test_r2_score,test_mae,test_msle,test_rmse


# S2.2: Define the 'app()' function as directed above.
def app(car_df):    
    st.markdown("<p style='color:blue;font-size:25px'>This app uses <b>LINEAR REGRESION</b>to predict the price of the car based on the user inputs",unsafe_allow_html=True) 
    st.subheader("select values")
    car_wid = st.slider("Car Width", float(car_df['carwidth'].min()), float(car_df['carwidth'].max()))    
    eng_siz = st.slider("Engine Size", float(car_df['enginesize'].min()), float(car_df['enginesize'].max()))    
    hor_pow = st.slider("Horse Power", float(car_df['horsepower'].min()), float(car_df['horsepower'].max()))        
    drw_fwd = st.radio("Is it a Forward Dive Wheel CAr:", ("yes", "no"))  
    if drw_fwd =="yes" :
        drw_fwd =1
    else:
        drw_fwd = 0
    com_bui = st.radio("is it a manufactured by buick ?",("yes","no"))
    if com_bui =="yes" :
        com_bui =1
    else:
        com_bui = 0
    
    # When 'Predict' button is clicked, the 'prediction()' function must be called 
    # and the value returned by it must be stored in a variable, say 'price'. 
    # Print the value of 'price' and 'score' variable using the 'st.success()' and 'st.info()' functions respectively.
    if st.button("predict"):
        st.subheader("Prediction results:")
        price,score,car_r2,car_mae,car_msle,car_rmse = prediction(car_df, car_wid, eng_siz, hor_pow, drw_fwd, com_bui)

        
        st.success("The predicted price of the car: ${:,}".format(int(price)))
        st.info("Accuracy score of this model is: {:2.2%}".format(score))
        st.info(f"R-squared score of this model is: {car_r2:.3f}")  
        st.info(f"Mean absolute error of this model is: {car_mae:.3f}")  
        st.info(f"Mean squared log error of this model is: {car_msle:.3f}")  
        st.info(f"Root mean squared error of this model is: {car_rmse:.3f}")