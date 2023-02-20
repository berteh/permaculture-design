import numpy as np
import pandas as pd
import random

class PlantData():

    def __init__(self):
        # Maybe make this a static element (outside the init) so that it can be edited??
        self.data = pd.read_csv('../scrapers/pfaf/all_plants.csv')
        self.filtered_df = pd.DataFrame()

    def search(self, value): # called from TextInput on_text_validate (Enter)

        self.results_df = self.data[self.data['CommonName'].str.lower().str.contains(value.text.lower().replace(" ", "|"), na=False)]

        self.results_dict = {plant_series[1]['CommonName'].split(',')[0]: plant_series[1].drop(columns='CommonName')\
            for plant_series in self.results_df.iterrows()}

        rv = self.root.ids.left_panel.ids.second_screen.ids.rv
        if len(self.results_dict) > 0:
            rv.data = [{'text': plant} for plant in self.results_dict.keys()]
        else:
            rv.data = [{'text': 'No results found'}]

        # Unselect RecycleView selection if selected
        try:
            rv.layout_manager.deselect_node(rv.layout_manager.selected_nodes[-1])
        except IndexError:
            pass

        # Clear plant attributes from previous search
        self.root.ids.left_panel.ids.second_screen.ids.plant_attrs.text = ''

    def filter_plants(self, family=None, genus=None, species=None, common_name=None, growth_rate=None,
                  hardiness_zones=None, height=None, width=None, plant_type=None, pollinators=None,
                  leaf=None, flower=None, ripen=None, reproduction=None, soils=None, pH=None,
                  preferences=None, tolerances=None, habitat=None, habitat_range=None,
                  edibility=None, medicinal=None, other_uses=None, pfaf=None):

        # Define the list of valid pollinators
        valid_pollinators = ['bees', 'insects', 'wind', 'flies', 'lepidoptera']

        # Filter by each column if a value is provided
        # Starting with full dataframe self.data
        if family is not None:
            self.filtered_df = self.data[self.data['Family'] == family]
        if genus is not None:
            self.filtered_df = self.filtered_df[self.filtered_df['Genus'] == genus]
        if species is not None:
            self.filtered_df = self.filtered_df[self.filtered_df['Species'] == species]
        if common_name is not None:
            self.filtered_df = self.filtered_df[self.filtered_df['CommonName'] == common_name]
        if growth_rate is not None:
            self.filtered_df = self.filtered_df[self.filtered_df['GrowthRate'] == growth_rate]
        if hardiness_zones is not None:
            if isinstance(hardiness_zones, int) and 2 <= hardiness_zones <= 12:
                self.filtered_df = self.filtered_df[self.filtered_df['HardinessZones'] == hardiness_zones]
            else:
                raise ValueError('HardinessZones must be an integer between 2 and 12')
        if height is not None:
            self.filtered_df = self.filtered_df[self.filtered_df['Height'] == height]
        if width is not None:
            self.filtered_df = self.filtered_df[self.filtered_df['Width'] == width]
        if plant_type is not None:
            self.filtered_df = self.filtered_df[self.filtered_df['Type'] == plant_type]
        if pollinators is not None:
            if isinstance(pollinators, list) and all(p in valid_pollinators for p in pollinators):
                self.filtered_df = self.filtered_df[self.filtered_df['Pollinators'].apply(lambda x: all(p in x.split(', ') for p in pollinators))]
            else:
                raise ValueError(f'Pollinators must be a list of any combination of {valid_pollinators}')
        if leaf is not None:
            self.filtered_df = self.filtered_df[self.filtered_df['Leaf'] == leaf]
        if flower is not None:
            self.filtered_df = self.filtered_df[self.filtered_df['Flower'] == flower]
        if ripen is not None:
            self.filtered_df = self.filtered_df[self.filtered_df['Ripen'] == ripen]
        if reproduction is not None:
            self.filtered_df = self.filtered_df[self.filtered_df['Reproduction'] == reproduction]
        if soils is not None:
            self.filtered_df = self.filtered_df[self.filtered_df['Soils'] == soils]
        if pH is not None:
            self.filtered_df = self.filtered_df[self.filtered_df['pH'] == pH]
        if preferences is not None:
            self.filtered_df = self.filtered_df[self.filtered_df['Preferences'] == preferences]
        if tolerances is not None:
            self.filtered_df = self.filtered_df[self.filtered_df['Tolerances'] == tolerances]
        if habitat is not None:
            self.filtered_df = self.filtered_df[self.filtered_df['Habitat'] == habitat]
        if habitat_range is not None:
            self.filtered_df = self.filtered_df[self.filtered_df['HabitatRange'] == habitat_range]
        if edibility is not None:
            self.filtered_df = self.filtered_df[self.filtered_df['Edibility'] == edibility]
        if medicinal is not None:
            self.filtered_df = self.filtered_df[self.filtered_df['Medicinal'] == medicinal]
        if other_uses is not None:
            self.filtered_df = self.filtered_df[self.filtered_df['OtherUses'] == other_uses]
        if pfaf is not None:
            self.filtered_df = self.filtered_df[self.filtered_df['PFAF'] == pfaf]

        return self.filtered_df

class MyDesign:
    # Takes length, width and units args from design layout
    def __init__(self, length, width, units):
        self.length = length
        self.width = width
        self.units = units
        self.area = length * width
        self.overlap = 0
        # I'll use a list to store data, create dataframe when needed
        self.data = []

    def add_plant(self, common_name, x_pos, y_pos, height, width):
        self.data.append({
            'common_name': common_name, # should change to latin name as unique id
            'x, y': (x_pos, y_pos),
            'height': height,
            'width': width
        })

    def to_dataframe(self):
        df = pd.DataFrame(self.data)
        # Use groupby latin_name to sum plants
        ### *** THIS DOESNT WORK. NEED TO MAINTAIN INDIVIDUAL X- Y- POS AND COUNT TOTALS *** ###
        return df.groupby('common_name').agg({
            'common_name': 'count', 'x, y': 'unique', 'height': 'mean', 'width': 'mean'
        })
