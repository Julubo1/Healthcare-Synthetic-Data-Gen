import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# Configuratie
NUM_PATIENTS = 50
NUM_EPISODES = 80  # Zorgtrajecten / DBC's
NUM_ACTIVITIES = 500 # Tijdregistraties / Verrichtingen
OUTPUT_DIR = 'output'

# Initialiseer Faker voor Nederlandse data
fake = Faker('nl_NL')
Faker.seed(42) # Zorgt ervoor dat je elke keer dezelfde 'random' data krijgt (handig voor testen)

def generate_patients(n):
    """Genereert een lijst met fictieve patiënten."""
    patients = []
    for _ in range(n):
        gender = random.choice(['M', 'V'])
        first_name = fake.first_name_male() if gender == 'M' else fake.first_name_female()
        last_name = fake.last_name()
        
        patients.append({
            'patient_id': fake.unique.random_number(digits=6),
            'bsn': fake.ssn(),
            'full_name': f"{last_name}, {first_name}",
            'gender': gender,
            'birth_date': fake.date_of_birth(minimum_age=18, maximum_age=90),
            'city': fake.city(),
            'email': fake.email()
        })
    return pd.DataFrame(patients)

def generate_episodes(n, patients_df):
    """Genereert zorgtrajecten gekoppeld aan patiënten."""
    episodes = []
    patient_ids = patients_df['patient_id'].tolist()
    
    diagnoses = ['Depressie', 'Angststoornis', 'PTSS', 'Persoonlijkheidsstoornis', 'ADHD', 'Autisme Spectrum']
    care_types = ['Klinisch', 'Ambulant', 'Deeltijd']

    for _ in range(n):
        start_date = fake.date_between(start_date='-2y', end_date='today')
        
        # 70% kans dat het traject is afgesloten, 30% loopt nog
        if random.random() < 0.7:
            duration = random.randint(30, 365)
            end_date = start_date + timedelta(days=duration)
            status = 'Gesloten'
        else:
            end_date = None
            status = 'Open'

        episodes.append({
            'episode_id': fake.unique.random_number(digits=8),
            'patient_id': random.choice(patient_ids),
            'diagnosis': random.choice(diagnoses),
            'care_type': random.choice(care_types),
            'start_date': start_date,
            'end_date': end_date,
            'status': status,
            'practitioner': fake.name() # Hoofdbehandelaar
        })
    return pd.DataFrame(episodes)

def generate_activities(n, episodes_df):
    """Genereert tijdsregistraties/verrichtingen binnen de looptijd van trajecten."""
    activities = []
    
    product_codes = [
        {'code': 'BEH001', 'desc': 'Intakegesprek', 'minutes': 60},
        {'code': 'BEH002', 'desc': 'Individuele therapie', 'minutes': 45},
        {'code': 'BEH003', 'desc': 'Systeemtherapie', 'minutes': 90},
        {'code': 'ADM001', 'desc': 'Verslaglegging', 'minutes': 15},
        {'code': 'DIA001', 'desc': 'Diagnostiek', 'minutes': 120},
    ]

    episodes_list = episodes_df.to_dict('records')

    for _ in range(n):
        episode = random.choice(episodes_list)
        
        # Bepaal een datum BINNEN het traject
        episode_start = episode['start_date']
        episode_end = episode['end_date'] if episode['end_date'] else datetime.today().date()
        
        # Zorg dat activiteit datum niet voor start ligt
        days_diff = (episode_end - episode_start).days
        if days_diff < 0: days_diff = 0
        
        random_days = random.randint(0, days_diff)
        activity_date = episode_start + timedelta(days=random_days)
        
        product = random.choice(product_codes)

        activities.append({
            'activity_id': fake.unique.random_number(digits=10),
            'episode_id': episode['episode_id'],
            'date': activity_date,
            'product_code': product['code'],
            'description': product['desc'],
            'duration_minutes': product['minutes'],
            'registrant': fake.first_name() # Naam van medewerker
        })
    
    return pd.DataFrame(activities)

def main():
    print("🚀 Start genereren zorgdata...")
    
    # Maak output map
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 1. Patiënten
    print(f" - {NUM_PATIENTS} patiënten genereren...")
    df_patients = generate_patients(NUM_PATIENTS)
    df_patients.to_csv(f'{OUTPUT_DIR}/patients.csv', index=False)
    
    # 2. Zorgtrajecten
    print(f" - {NUM_EPISODES} zorgtrajecten genereren...")
    df_episodes = generate_episodes(NUM_EPISODES, df_patients)
    df_episodes.to_csv(f'{OUTPUT_DIR}/episodes.csv', index=False)

    # 3. Activiteiten
    print(f" - {NUM_ACTIVITIES} activiteiten genereren...")
    df_activities = generate_activities(NUM_ACTIVITIES, df_episodes)
    df_activities.to_csv(f'{OUTPUT_DIR}/activities.csv', index=False)

    print(f"✅ Klaar! Bestanden staan in de map '{OUTPUT_DIR}/'.")
    print("   - patients.csv")
    print("   - episodes.csv")
    print("   - activities.csv")

if __name__ == "__main__":
    main()
