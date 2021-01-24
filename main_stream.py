import streamlit as st
from PIL import Image
import requests
import random

# I. Following the steps above, find the annual cost to operate an electric kettle.

# 1. Estimate of time used: The kettle is used several times per day, for about 1 total hour.

# 2. electricity_usage: The electricity_usage is on the label and is listed at 1500 W.

# 3. Daily energy consumption:
# (1,500 W × 1) ÷ 1,000 = 1.5 kWh

# 4. Annual energy consumption: The kettle is used almost every day of the year.
# 1.5 kWh × 365 = 547.5 kWh

# 5. Annual cost: The utility rate is 11 cents per kWh.
# 547.5 kWh × $0.11/kWh = $60.23/year

class appliance(object):
    def __init__(self, time_used, water_usage=None, electricity_usage=None, natural_gas_usage=None):
        self.water_usage = water_usage
        self.electricity_usage = electricity_usage
        self.natural_gas_usage = natural_gas_usage
        self.time_used = time_used
        if electricity_usage is not None:
            self.energy_consumption = electricity_usage * time_used
        if water_usage is not None:
            self.energy_consumption = water_usage * time_used

class home(object):
    def __init__(self, electricity_cost=None, zip_code=None, total_electricity_use=0,
                 total_water_use=0, electricity_total_cost=0):
        self.electricity_cost = electricity_cost
        self.zip_code = zip_code
        self.total_water_use = total_water_use
        self.total_electricity_use = total_electricity_use
        self.electricity_total_cost = electricity_total_cost
        self.appliance_list = []

    #@st.cache
    def update_electric_prices(self):
        self.electricity_cost = random.uniform(0.11, 0.3)

    #@st.cache
    def region_characteristics(self):
        #Use zip code
        if None:
            self.uses_heating = True
            self.uses_cooling = False

    def add_appliances(self, time_used, water_usage=None, electricity_usage=None, natural_gas_usage=None):
        self.appliance_list.append(appliance(time_used, water_usage, electricity_usage, natural_gas_usage))

    def total_energy_consumption(self):
        for app in self.appliance_list:
            if app.electricity_usage is not None:
                self.total_electricity_use += app.electricity_usage * app.time_used * 365
        self.electricity_total_cost = self.total_electricity_use * self.electricity_cost

    def total_water_consumption(self):
        for app in self.appliance_list:
            if app.water_usage is not None:
                self.total_water_use += app.water_usage * app.time_used * 365

    @st.cache()
    def calculate_solar_generation(self):
        self.add_appliances(5, electricity_usage= -random.randint(1,50))
        #Use zipcode somehow

    def furnace_load_calculation(self):
        self.add_appliances(2, electricity_usage=18000)

    def ac_load_calculation(self):
        self.add_appliances(3, electricity_usage=3500)

#https://www.energy.gov/eere/why-energy-efficiency-upgrades
class main_streamlit(object):
    def __init__(self):
        self.house = home()

    def create_main_page(self):
        st.markdown(
            """ <style>
                    div[role="radiogroup"] >  :first-child{
                        display: none !important;
                    }
                </style>
                """,
            unsafe_allow_html=True
        )
        col1, col2, col3, col4 = st.beta_columns([4,4,4,12])
        with col1:
            self.house.zip_code = st.text_input("Enter Zip Code")
            if len(self.house.zip_code) > 0:
                self.house.update_electric_prices()
            fur = st.radio('Furnace Type', ['-','electric','gas','heatpump'])
            if fur == 'gas':
                st.radio('Furnace Efficiency', ['-','90% Efficiency','92% Efficiency'])
            elif fur == 'electric':
                self.house.furnace_load_calculation()
            air_con = st.number_input("Air Conditioner SEER",8,20)
            therm = st.radio("Smart Thermostat",['-',"Yes", "No"])
            panels = st.radio("Add Solar Panels", ('-',"Yes","No"))
            if panels == "Yes":
                self.house.calculate_solar_generation()
            wa_heat = st.radio("Water Heater Type",['-',"Tank Water Heater", "Tankless Water Heater"])
            if wa_heat == "Tankless Water Heater":
                self.house.add_appliances(1.5,electricity_usage=4000)
            elif wa_heat == "Tank Water Heater":
                self.house.add_appliances(3,electricity_usage=4000)
            clothes_dryer = st.radio("Dryer Type",['-',"Electric Dryer", "Clothesline"])
            if clothes_dryer == "Electric Dryer":
                self.house.add_appliances(.25,electricity_usage=3000)

        # with col2:

        # with col3:

        with col3:
            img = Image.open("house.jpg")
            basewidth = 500
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth,hsize), Image.ANTIALIAS)
            st.image(img,width=None)
            self.house.total_water_consumption()
            self.house.total_energy_consumption()
            st.write(f'You are using {self.house.total_water_use} Gallons of water a year')
            st.write(f'You are using {self.house.total_electricity_use} kWh a year, for a cost of {self.house.electricity_total_cost}')


if __name__ == '__main__':
    main = main_streamlit()
    main.create_main_page()