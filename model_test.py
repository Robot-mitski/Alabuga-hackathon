import joblib
loaded_model = joblib.load('model/model.pkl') # сохраненная модель
 
new_data = [[5.1, 3.5, 10, 1.0, 0.77, 3.555]]  # Пример новых данных
prediction = loaded_model.predict(new_data)
print(prediction)