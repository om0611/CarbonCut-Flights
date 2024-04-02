import pandas as pd

interested_airports = {'CGO', 'GRU', 'CAI', 'MXP', 'KUL', 'BRU', 'BLR', 'PEK', 'ORD', 'SIN', 'DME', 'PTY', 'MIA',
                       'DUB', 'XIY', 'FLL', 'PVG', 'ICN', 'SAW', 'SFO', 'MNL', 'CLT', 'SVO', 'SYD', 'NRT', 'CPH',
                       'CGK', 'ZRH', 'FCO', 'LIS', 'CMN', 'YYZ', 'IAH', 'SHA', 'TPE', 'IST', 'JNB', 'ATH', 'LAX',
                       'AMS', 'BOM', 'OSL', 'NBO', 'LGW', 'DEL', 'DXB', 'VIE', 'FRA', 'HGH', 'MEX', 'CNF', 'VCP',
                       'BKK', 'MEL', 'HND', 'ARN', 'MUC', 'AEP', 'SZX', 'PHX', 'BOG', 'CTU', 'SEA', 'DOH', 'CAN',
                       'LIM', 'ADD', 'MCO', 'ATL', 'CDG', 'SGN', 'SCL', 'MAN', 'ALG', 'MAD', 'LHR', 'CPT', 'JFK'}

df = pd.read_csv('CSV Files/airports-code@public.csv')
filtered_df = df[df['Airport Code'].isin(interested_airports)]

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv('CSV Files/78_airport_info.csv', index=False)
