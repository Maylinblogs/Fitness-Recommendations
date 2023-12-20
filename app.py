import logging



# Create a logger
logger = logging.getLogger('my_logger')

from flask import Flask, render_template, request
import pandas as pd

from processing import predict_patient_score

app = Flask(__name__)

# Load the fitness dataset
fitness_data = pd.read_csv('fitness.csv')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_user_info', methods=['POST'])
def get_user_info():
    try:
        user_id = int(request.form['user_id'])

        # Retrieve user information based on user_id
        user_data = fitness_data[fitness_data['User_ID'] == user_id]

        if not user_data.empty:
            # Calculate the number of times the user has done sports
            num_sports = user_data['Exercise_Type'].count()

            # Get the user's age
            user_age = user_data['Age'].iloc[0]

            return render_template('index.html', user_id=user_id, num_sports=num_sports, user_age=user_age)
        else:
            return render_template('index.html', error='User not found.')

    except Exception as e:
        return render_template('index.html', error=str(e))


@app.route('/process_patient_info', methods=['POST'])
def process_patient_info():
    try:
        # checklist
        age = int(request.form['age'])
        weight = float(request.form['weight'])
        sex = request.form['sex']
        exercise_frequency = request.form['exercise_frequency']
        healthy_diet = request.form['healthy_diet']
        exercise_duration = request.form['exercise_duration']

        # single choice
        time_preference = request.form['time_preference']
        exercise_preference = request.form['exercise_preferences']

        # multiple choice
        diet_barriers = ';'.join(request.form.getlist('diet_barriers'))
        # ';'.join(
        exercise_motivation = ';'.join(request.form.getlist('exercise_motivation'))

        patient_data = pd.DataFrame({
            'Age': [age],
            'Weight': [weight],
            'Sex': [sex],
            'Exercise_Frequency': [exercise_frequency],
            'Time_Preference': [time_preference],
            'Exercise_Duration': [exercise_duration],
            'Healthy_Diet': [healthy_diet],
            'Diet_Barriers': [diet_barriers],
            'Exercise_Preference': [exercise_preference],
            'Exercise_Motivation': [exercise_motivation],
        })

        # Save the data to a new CSV file
        patient_data.to_csv('patient_data1.csv', index=False)

        try:
            prediction = predict_patient_score(patient_data)
            if prediction== 1:
                prediction=f'''
                    **Unfit :**
                    1. **Diet:**
                       - Slow and steady changes to your diet are recommended. Start by reducing processed foods, sugary snacks, and excessive calorie intake.
                       - Increase water consumption and consider consulting with a nutritionist for a gradual dietary plan.
                    
                    \n2. **Sport/Activity:**
                       - Begin with light activities such as walking or gentle stretching. Aim for at least 30 minutes of activity most days of the week.
                       - Consult with a fitness professional to design a safe and progressive exercise plan.
                    
                    \n3. **Gradual Progress:**
                       - Set realistic goals and celebrate small victories to stay motivated.
                       - Consistency is key. Focus on creating a sustainable routine rather than pushing yourself too hard initially.
                       - Monitor your progress and adjust your plan based on your body's response.
                    
                    \n4. **Support System:**
                       - Consider involving a friend, family member, or a fitness buddy to provide support and accountability.
                       - Seek guidance from fitness professionals or healthcare providers if needed.
                    
                    Remember, the key is to approach fitness as a gradual and sustainable lifestyle change. Adjust your approach based on how your body responds and seek professional guidance when needed.
                    '''
            elif prediction== 2:
                prediction=f'''
                    **Average :**
                    1. **Diet:**
                       - Focus on portion control and choose whole, nutrient-dense foods.
                       - Limit processed foods, added sugars, and excessive fats. Consider consulting with a nutritionist for personalized guidance.
                       - Increase water intake and maintain hydration.\n
                    
                    2. **Sport/Activity:**
                       - Engage in moderate-intensity exercises like brisk walking, jogging, or weight training.
                       - Aim for at least 150 minutes of moderate-intensity exercise per week, along with flexibility exercises.
                       - Gradually increase the intensity and duration of your workouts.\n
                    
                    3. **Progressive Approach:**
                       - Set realistic goals and track your progress.
                       - Gradually increase the intensity and duration of your workouts to challenge your body.
                       - Consider incorporating interval training to boost cardiovascular fitness.\n
                    
                    4. **Mindful Eating:**
                       - Be mindful of portion sizes and avoid overeating.
                       - Pay attention to hunger and fullness cues to regulate your food intake.
                       - Continue shifting towards whole, unprocessed foods.\n
                    
                    5. **Lifestyle Integration:**
                       - Look for opportunities to be active throughout the day.
                       - Join group classes, sports leagues, or workout with friends for added motivation.
                       - Allow time for proper rest and recovery between workouts.
                    
                    Remember, the key is to be consistent with your efforts and make gradual improvements over time. Adjust your plan based on your individual responses and consult with professionals if needed.
                    '''
            elif prediction==3:
                prediction= f'''**Good ):**
                    1. **Diet:**
                       - Continue with a balanced diet, paying attention to portion control.
                       - Incorporate more plant-based foods, lean meats, and healthy fats.
                       - Include pre- and post-workout nutrition to support energy levels.
                    
                    \n2. **Sport/Activity:**
                       - Maintain a regular exercise routine with a mix of cardio and strength training.
                       - Explore different activities such as swimming, cycling, or group fitness classes.
                       - Gradually increase the intensity and duration of your workouts.
                    
                    \n3. **Variety and Progression:**
                       - Explore different forms of physical activity to keep things interesting.
                       - Gradually increase the intensity and duration of your workouts for continued progress.
                       - Set realistic goals and celebrate achievements to stay motivated.
                    
                    
                    \n4. **Mindful Living:**
                       - Focus on stress management techniques, such as mindfulness or relaxation exercises.
                       - Ensure sufficient sleep for recovery and overall well-being.
                    
                    Remember, consistency and gradual progression are key. Adjust your approach based on how your body responds and consult with professionals if needed.
                    '''
            elif prediction==4:
                prediction== f'''
                    **Very Good (Fitness Level:):**
                    1. **Diet:**
                       - Continue with a well-balanced diet, paying attention to nutrient optimization.
                       - Plan meals in advance to ensure a consistent intake of nutrients.
                       - Consider consulting with a nutritionist for personalized advice.
                    
                    \n2. **Sport/Activity:**
                       - Progress to more advanced training techniques, such as high-intensity interval training (HIIT) or periodization.
                       - Tailor your training to enhance performance in specific sports or activities.
                       - Incorporate active recovery and flexibility exercises into your routine.
                    
                    \n3. **Holistic Wellness:**
                       - Integrate holistic wellness practices, such as regular massage, chiropractic care, or other recovery modalities.
                       - Explore mind-body practices like Pilates or Tai Chi to enhance body awareness.
                       - Prioritize sleep as a crucial component of recovery.
                    
                    \n4. **Lifestyle Integration:**
                       - Engage in social fitness activities to enhance motivation.
                       - Use your fitness level to explore new physical challenges and activities.
                       - Continuously learn and stay updated on the latest advancements in fitness.
                    
                    Remember, your fitness journey is unique, and these recommendations can be tailored based on your preferences and specific goals.
                    '''
            elif prediction==5:
                prediction= f'''
                **Excellent (Fitness Level:):**
                1. **Diet:**
                   - Fine-tune your nutrition to support optimal performance and recovery.
                   - Consider working with a nutritionist to tailor your diet to your specific needs.
                   - Optimize nutrient timing around workouts for enhanced performance and recovery.
                   - Consider targeted supplements based on individual goals and requirements.
                
                \n2. **Sport/Activity:**
                   - Fine-tune your training program to align with specific fitness goals or performance objectives.
                   - Incorporate advanced training techniques such as plyometrics, advanced strength training, and specialized conditioning drills.
                   - Implement periodization to ensure continuous progress and prevent overtraining.
                
                \n3. **Recovery and Regeneration:**
                   - Develop a comprehensive recovery plan that includes advanced recovery modalities like massage, foam rolling, and cryotherapy.
                   - Prioritize sleep as a crucial component of recovery. Ensure adequate sleep duration and quality.
                   - Integrate active recovery days with low-intensity activities to promote circulation, flexibility, and mental well-being.
                
                \n4. **Holistic Wellness:**
                   - Incorporate advanced mind-body practices such as mindfulness meditation, biofeedback, or visualization techniques to enhance mental focus and performance.
                   - Build a team of health and wellness professionals, including physiotherapists, sports psychologists, and nutrition experts, to provide holistic support.
                
                \n5. **Lifestyle Integration:**
                   - Integrate functional fitness activities that mimic real-life movements to enhance overall strength, balance, and coordination.
                   - Set specific and measurable fitness goals. Regularly reassess and adjust goals as needed.
                   - Stay updated on the latest advancements in fitness, nutrition, and wellness. Continue learning and evolving.
                
                Remember, while achieving an excellent fitness level is commendable, it's crucial to balance intensity with sustainability and overall well-being. Listen to your body, prioritize recovery, and adjust your approach based on how you feel and any changes in goals or lifestyle.
                '''
            else:
                prediction="HMM"


            logger.debug(f'Prediction: {prediction}')
        except Exception as e:
            logger.error(f'Error in prediction: {e}')

        return render_template('patient_info_result.html', prediction=prediction)

    except Exception as e:
        return render_template(
            'patient_info_result.html',
            age=age,
            weight=weight,
            sex=sex,
            exercise_frequency=exercise_frequency,
            exercise_preferences=exercise_preference,
            time_preference=time_preference,
            exercise_duration=exercise_duration,
            healthy_diet=healthy_diet,
            diet_barriers=diet_barriers,
            exercise_motivation=exercise_motivation,
        )


if __name__ == '__main__':
    app.run(debug=True)
