import pandas as pd

from load import read_pickle_file

processor = read_pickle_file('processor.pkl')
model = read_pickle_file('lgbm.pkl')


def predict_patient_score(data: pd.DataFrame):
    motivations = [
        'I want to be fit',
        'I want to increase muscle mass and strength',
        'I want to lose weight',
        'I want to be flexible',
        'I want to relieve stress',
        'I want to achieve a sporting goal',
        "I'm not really interested in exercising"
    ]

    for motivation in motivations:
        column_name = motivation.replace(' ', '_').lower()  # Convert to lowercase and replace spaces with underscores
        data[column_name] = data['Exercise_Motivation'].str.contains(motivation).astype(int)

    # Mapping dictionary
    Exercise_Frequency = {
        'never': 1,
        '1 to 2 times a week': 2,
        '2 to 3 times a week': 3,
        '3 to 4 times a week': 4,
        '5 to 6 times a week': 5,
        'everyday': 6,
        # Add more mappings as needed
    }

    # Apply mapping to the 'Frequency' column
    data['Exercise_Frequency'] = data['Exercise_Frequency'].str.lower().map(Exercise_Frequency)

    # Apply mapping to the 'Time_Preference' column
    time_preference_mapping = {
        'early morning': 1,
        'afternoon': 2,
        'evening': 3,
        # Add more mappings as needed
    }

    # Apply mapping to the 'Time_Preference' column
    data['Time_Preference'] = data['Time_Preference'].str.lower().map(time_preference_mapping)

    # Mapping dictionary for Exercise_Duration
    exercise_duration_mapping = {
        '30 minutes': 30,
        '1 hour': 60,
        '2 hours': 120,
        '3 hours and above': 180,  # Adjust this value based on your preference
        "I don't really exercise": 0,  # Assign a value for 'I don't really exercise'
        # Add more mappings as needed
    }

    # Apply mapping to the 'Exercise_Duration' column
    data['Exercise_Duration'] = data['Exercise_Duration'].map(exercise_duration_mapping)

    # Mapping dictionary for Healthy_Diet
    healthy_diet_mapping = {
        'Yes': 1,
        'No': 0,
        'Not always': 0.5,  # Assign a value for 'Not always' (you can adjust this based on your preference)
        # Add more mappings as needed
    }

    # Apply mapping to the 'Healthy_Diet' column

    data['Healthy_Diet'] = data['Healthy_Diet'].map(healthy_diet_mapping)

    #
    age_mapping = {
        '19 to 25': 1,
        '15 to 18': 2,
        '26 to 30': 3,
        '30 to 40': 4,
        '40 and above': 5,
        # Add more mappings as needed
    }

    # Apply mapping to the 'Age' column
    data['Age'] = pd.cut(
        data['Age'],
        bins=[0, 18, 25, 30, 40, float('inf')],
        labels=age_mapping.values(),
        include_lowest=True,
        right=False)

    exercise_forms = [
        'Walking or jogging',
        'Gym',
        'Swimming',
        'Yoga',
        'Zumba dance',
        'Lifting weights',
        'Team sport',
        "I don't really exercise"
    ]

    for form in exercise_forms:
        column_name = form.replace(' ', '_').lower()  # Convert to lowercase and replace spaces with underscores
        data[column_name] = data['Exercise_Preference'].str.contains(form).astype(int)

    # List of columns to be deleted
    columns_to_delete = ['Exercise_Preference', 'Exercise_Motivation', 'Diet_Barriers']

    # Drop the specified columns
    data = data.drop(columns=columns_to_delete, errors='ignore')

    transformed_data = processor.transform(data)

    prediction = model.predict(transformed_data)

    return prediction
