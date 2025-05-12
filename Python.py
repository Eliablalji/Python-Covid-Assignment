import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Data Collection & Loading ---
# Load the data from the CSV file
# Replace 'owid-covid-data.csv' with the actual path to your downloaded file
df = pd.read_csv('owid-covid-data.csv')

# --- 2. Data Loading & Exploration ---
# Check the columns in the DataFrame
print("Columns:", df.columns)

# Preview the first few rows of the DataFrame
print("\nPreview of data:")
print(df.head())

# Identify missing values in each column
print("\nMissing values per column:")
print(df.isnull().sum())

# Get data types of columns
print("\nData types of columns:")
print(df.dtypes)

# --- 3. Data Cleaning ---
# Handle missing numeric values by filling them with the mean
for col in df.select_dtypes(include=['number']):
    df[col] = df[col].fillna(df[col].mean())

# Handle missing values in other columns (fill with 'Unknown')
for col in df.select_dtypes(exclude=['number']):
    df[col] = df[col].fillna('Unknown')

# Convert the 'date' column to datetime objects
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.dropna(subset=['date'])

# Filter countries of interest
countries_of_interest = ['Kenya', 'USA', 'India']
df_filtered = df[df['location'].isin(countries_of_interest)].copy()

# Set 'date' as index for time series analysis
df_filtered.set_index('date', inplace=True)

# --- 4. Exploratory Data Analysis (EDA) ---
print("\n--- Exploratory Data Analysis ---")

# Plot total cases over time for selected countries
plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    country_data = df_filtered[df_filtered['location'] == country]
    plt.plot(country_data.index, country_data['total_cases'], label=country)
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.title('Total COVID-19 Cases Over Time')
plt.legend()
plt.grid(True)
plt.show()

# Plot total deaths over time
plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    country_data = df_filtered[df_filtered['location'] == country]
    plt.plot(country_data.index, country_data['total_deaths'], label=country)
plt.xlabel('Date')
plt.ylabel('Total Deaths')
plt.title('Total COVID-19 Deaths Over Time')
plt.legend()
plt.grid(True)
plt.show()

# Compare daily new cases between countries
plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    country_data = df_filtered[df_filtered['location'] == country]
    plt.plot(country_data.index, country_data['new_cases'], label=country)
plt.xlabel('Date')
plt.ylabel('Daily New Cases')
plt.title('Daily New COVID-19 Cases')
plt.legend()
plt.grid(True)
plt.show()

# Calculate the death rate (total_deaths / total_cases)
df_filtered['death_rate'] = df_filtered['total_deaths'] / df_filtered['total_cases']

# Visualize death rate over time
plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    country_data = df_filtered[df_filtered['location'] == country]
    plt.plot(country_data.index, country_data['death_rate'], label=country)
plt.xlabel('Date')
plt.ylabel('Death Rate (Total Deaths / Total Cases)')
plt.title('COVID-19 Death Rate Over Time')
plt.legend()
plt.grid(True)
plt.show()

# Line charts (cases & deaths over time) - already done above

# Bar charts (top countries by total cases)
latest_data = df.groupby('location')['total_cases'].max().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=latest_data.values, y=latest_data.index)
plt.xlabel('Total Cases')
plt.ylabel('Country')
plt.title('Top 10 Countries by Total COVID-19 Cases (Latest)')
plt.show()

# --- 5. Visualizing Vaccination Progress ---
print("\n--- Visualizing Vaccination Progress ---")

# Plot cumulative vaccinations over time for selected countries
plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    country_data = df_filtered[df_filtered['location'] == country]
    plt.plot(country_data.index, country_data['total_vaccinations'], label=country)
plt.xlabel('Date')
plt.ylabel('Total Vaccinations')
plt.title('Cumulative COVID-19 Vaccinations Over Time')
plt.legend()
plt.grid(True)
plt.show()

# Compare % vaccinated population (assuming 'people_vaccinated_per_hundred' is available)
if 'people_vaccinated_per_hundred' in df_filtered.columns:
    plt.figure(figsize=(12, 6))
    for country in countries_of_interest:
        country_data = df_filtered[df_filtered['location'] == country]
        plt.plot(country_data.index, country_data['people_vaccinated_per_hundred'], label=country)
    plt.xlabel('Date')
    plt.ylabel('Percentage of Population Vaccinated')
    plt.title('Percentage of Population Vaccinated Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()
else:
    print("\n'people_vaccinated_per_hundred' column not found. Cannot plot percentage vaccinated population.")

# Line charts (already done above for cumulative vaccinations)

# --- 6. Optional: Build a Choropleth Map ---
print("\n--- Optional: Choropleth Map Visualization ---")
print("Note: Building a choropleth map requires the 'plotly.express' library and internet connectivity to fetch map data.")
print("Uncomment the following section if you have 'plotly.express' installed and want to create this visualization.")

"""
import plotly.express as px

# Get the latest total cases by country
latest_cases = df.groupby('iso_code')['total_cases'].max().reset_index()

# Create the choropleth map
fig = px.choropleth(latest_cases,
                    locations='iso_code',
                    color='total_cases',
                    hover_name='iso_code',
                    color_continuous_scale=px.colors.sequential.Plasma,
                    title='Total COVID-19 Cases by Country (Latest)')
fig.show()

# If you want to visualize vaccination rates, you'd need to find a column with that data
# and adapt the above code.
"""

print("\nChoropleth map code is commented out. Uncomment to run if you have plotly installed.")

# --- 7. Insights & Reporting ---
print("\n--- Insights & Reporting ---")
print("Based on the visualizations and analysis, you can now write down your key insights.")
print("For example:")
print("- The trend of total cases and deaths has increased over time in the selected countries.")
print("- The rate of new daily cases shows peaks and troughs, indicating waves of infection.")
print("- The death rate provides a perspective on the severity of the pandemic in different countries.")
print("- Vaccination campaigns have led to an increase in the percentage of the population vaccinated over time (where data is available).")
print("- Comparing the timelines and slopes of these graphs across countries can reveal differences in the pandemic's progression and response.")

print("\nRemember to use markdown cells in your Jupyter Notebook to write your narrative explanations and highlight any anomalies or interesting patterns you observe.")