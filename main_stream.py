import streamlit as st
from PIL import Image
import requests
import random

def _max_width_():
    max_width_str = f"max-width: 2000px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

class appliance(object):
    def __init__(self, time_used, water_usage=None, electricity_usage=None, natural_gas_usage=None):
        self.water_usage = water_usage
        self.electricity_usage = electricity_usage
        self.natural_gas_usage = natural_gas_usage
        self.time_used = time_used

class home(object):
    def __init__(self, electricity_cost=.1, zip_code=None, total_electricity_use=0,
                 total_water_use=0, electricity_total_cost=0):
        self.electricity_cost = electricity_cost
        self.zip_code = zip_code
        self.total_water_use = total_water_use
        self.total_electricity_use = total_electricity_use
        self.electricity_total_cost = electricity_total_cost
        self.appliance_list = []

    @st.cache
    def update_electric_prices(self):
        self.electricity_cost = random.uniform(0.11, 0.13)

    @st.cache
    def region_characteristics(self):
        #Use zip code
        if None:
            self.uses_heating = True
            self.uses_cooling = False

    def add_appliances(self, time_used, water_usage=None, electricity_usage=None, natural_gas_usage=None):
        self.appliance_list.append(appliance(time_used, water_usage, electricity_usage, natural_gas_usage))

    def total_energy_consumption(self):
        if len(self.appliance_list) != 0:
            for app in self.appliance_list:
                if app.electricity_usage is not None:
                    self.total_electricity_use += app.electricity_usage * app.time_used * 365
            self.total_electricity_use = self.total_electricity_use / 1000
            self.electricity_total_cost = round((self.total_electricity_use) * self.electricity_cost,2)

    def total_water_consumption(self):
        if len(self.appliance_list) != 0:
            for app in self.appliance_list:
                if app.water_usage is not None:
                    self.total_water_use += app.water_usage * app.time_used * 365
        self.total_water_use = round(self.total_water_use,2)

    @st.cache()
    def calculate_solar_generation(self):
        self.add_appliances(5, electricity_usage= -random.randint(250,300))
        #Use zipcode somehow

    def furnace_load_calculation(self):
        self.add_appliances(2, electricity_usage=1800)

    def ac_load_calculation(self):
        self.add_appliances(3, electricity_usage=3500)

    def generate_recommendations(self, show_length, therm):
        if show_length > .15:
            st.write("Take shorter showers, or install a low flow showerhead")
            st.write("Amazon [link](https://www.amazon.com/High-Sierras-Efficiency-Showerhead-Available/dp/B001W2CEYA/ref=sr_1_7?dchild=1&keywords=low+flow+shower+head&qid=1611505674&sr=8-7)")
        elif therm == 'No':
            st.write("Purchase a smart thermostat, you could decrease your coolsing/heating costs by 10-15%")
            st.write("Amazon [link](https://www.amazon.com/Google-Nest-Thermostat-Smart-Programmable/dp/B08HRPDYTP/ref=sr_1_5?)")

#https://www.energy.gov/eere/why-energy-efficiency-upgrades
class main_streamlit(object):
    def __init__(self):
        self.house = home()

    def create_main_page(self):
        _max_width_()
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
                self.house.ac_load_calculation()
            elif fur == 'electric':
                self.house.furnace_load_calculation()
                self.house.ac_load_calculation()
            elif fur =='heatpump':
                self.house.add_appliances(4,electricity_usage=350)
            therm = st.radio("Smart Thermostat",['-',"Yes", "No"])
            if therm == "Yes":
                self.house.add_appliances(2,electricity_usage=-180)
            panels = st.radio("Add Solar Panels", ('-',"Yes","No"))
            if panels == "Yes":
                self.house.calculate_solar_generation()
            wa_heat = st.radio("Water Heater Type",['-',"Tank Water Heater", "Tankless Water Heater"])
            if wa_heat == "Tankless Water Heater":
                self.house.add_appliances(1.5,electricity_usage=3000)
            elif wa_heat == "Tank Water Heater":
                self.house.add_appliances(3,electricity_usage=4000)
            
        with col2:
            clothes_dryer = st.radio("Dryer Type",['-',"Electric Dryer", "Clothesline"])
            if clothes_dryer == "Electric Dryer":
                self.house.add_appliances(.25,electricity_usage=3000)
            insul_effic = st.radio("Home recently inspected", ['-','Yes','No'])
            if insul_effic == 'No':
                self.house.add_appliances(1, electricity_usage=3000)
            lights = st.radio("Energy Efficient Lighting",['-','Yes','No'])
            if lights == 'Yes':
                self.house.add_appliances(4, electricity_usage=25*12)
            else:
                self.house.add_appliances(4, electricity_usage=100*12)
            show_length = st.number_input("Length of Showers (min)",0) / 60
            self.house.add_appliances(show_length,water_usage=2.5)
            sprinkler_usage = st.radio("Sprinklers",['-','Yes','No'])
            if sprinkler_usage == 'Yes':
                self.house.add_appliances(.2,water_usage=1020)

        with col3:
            if clothes_dryer == "Electric Dryer":
                img = Image.open("dryer.jpg")
            elif clothes_dryer == "Clothesline":
                img = Image.open("clothesline.jpg")
            elif panels == "Yes":
                img = Image.open("image2.jpg")
            elif therm == 'Yes':
                img = Image.open("image3.jpg")
            else:
                img = Image.open("house.jpg")
            basewidth = 500
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth,hsize), Image.ANTIALIAS)
            st.image(img,width=None)
            self.house.total_water_consumption()
            self.house.total_energy_consumption()
            st.write(f'You are using {self.house.total_water_use} Gallons of water a year')
            st.write(f'You are using {self.house.total_electricity_use} kWh a year, for a cost of ${self.house.electricity_total_cost}')
            if st.button("Generate Recommendations"):
                self.house.generate_recommendations(show_length,therm)


if __name__ == '__main__':
    main = main_streamlit()
    main.create_main_page()