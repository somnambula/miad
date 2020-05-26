import pandas as pd

file = pd.read_csv('mlbootcamp5_train.csv', sep=';', index_col='id')

gender = file.groupby('gender').mean()['height']

if gender[1] > gender[2]:
    male = 1
    female = 2
else:
    male = 2
    female = 1

count_people = file['gender'].value_counts()

print('\tTask 1')
print(f'\t\tMale(id={male}) - {count_people[male]}. Female(id={female}) - {count_people[female]}. ')

print('\tTask 2')
print(
    f'\t\tMale alco - {file.groupby("gender").mean()["alco"][male]}. Female alco - {file.groupby("gender").mean()["alco"][female]}'
)

print('\tTask 3')
print(
    f"\t\tIn {round((file.groupby('gender')['smoke'].mean()[2] * 100) / (file.groupby('gender')['smoke'].mean()[1] * 100))} times"
)

print('\tTask 4')
print(
    f"\t\tDiff in {round(abs(file.groupby(['smoke'])['age'].median()[1] / 30 - file.groupby(['smoke'])['age'].median()[0] / 30))} month"
)

print('\tTask 5')
file.insert(loc=len(file.columns), column='age_years', value=round(file['age'] / 365))

first = file.query(
    f'60.0 <= age_years <=  64.0 and gender == {male} and smoke == 1 and ap_hi<120 and cholesterol == 1')

second = file.query(
    f'60.0 <= age_years <=  64.0 and gender == {male} and smoke == 1 and ap_hi>=160 and ap_lo < 180 and cholesterol == 3')

first = len(first) / len(first[first['cardio'] == 1])
second = len(second) / len(second[second['cardio'] == 1])

print('\t\tFirst group percent: ', round(first, 2))
print('\t\tSecond group percent: ', round(second, 2))

print('\tTask 6')
bmi_min = 18.5
bmi_max = 25

file.insert(loc=len(file.columns), column='BMI', value=file['weight'] / (file['height'] / 100) ** 2)

# print(file)

print('\t\tTask 6.1')
if file['BMI'].median() > bmi_max:
    print('\t\t\t', True)
else:
    print('\t\t\t', False)

print('\t\tTask 6.2')
g_bmi = file.groupby('gender')['BMI'].mean()
if g_bmi[male] > g_bmi[female]:
    print('\t\t\t', True)
else:
    print('\t\t\t', False)

print('\t\tTask 6.3')
a_bmi = file.groupby('cardio')['BMI'].mean()
if a_bmi[0] > g_bmi[1]:
    print('\t\t\t', True)
else:
    print('\t\t\t', False)

m_bmi = file.groupby(['gender', 'alco', 'cardio'])['BMI'].mean()

print('\t\tTask 6.4')
if bmi_min <= m_bmi[male][0][0] <= bmi_max:
    print('\t\t\t', True)
else:
    print('\t\t\t', False)


# test task
first_fat = file.query(f'30.0 <= BMI < 35.0')
print('First fat state: ', len(first_fat), 'peoples')
second_fat = file.query(f'35.0 <= BMI < 40.0')
print('Second fat state: ', len(second_fat), 'peoples')
third_fat = file.query(f'BMI >= 40.0')
print('Third fat state: ', len(third_fat), 'peoples')
