import colorsys
import copy
import ctypes
import hashlib
import json
import math
import os
import calendar
import subprocess
import threading
import urllib.request
import sys
from datetime import date
import uuid
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageDraw, ImageOps, ImageChops


PALETTE = {
    "bg_outer":      "#5C4A93",
    "panel_fill":    "#473B72",
    "panel_border":  "#8874C9",
    "tag_fill":      "#2E2550",
    "badge_fill":    "#F2A93B",
    "badge_border":  "#8B5A2B",
    "title_fill":    "#FFA63D",
    "title_outline": "#B85C00",
    "label_text":    "#C9B8F0",
    "bar_track":     "#2B3D22",
    "bar_fill":      "#7ED957",
    "bar_border":    "#3C7A2E",
    "swatch_bg":     "#F4F4F4",
    "card_fill":     "#5A4A8E",
    "card_border":   "#8874C9",
    "row_fill":      "#3A2F5C",
    "row_border":    "#2B2148",
    "header_band":        "#8B6F47",
    "header_band_border": "#5C4A30",
    "value_text":    "#FFFFFF",
    "value_outline": "#2B2148",
    "pill_text":     "#3FA9E0",
    "pill_outline":  "#173145",
    "name_fill":     "#FBBB28",
    "name_outline":  "#722509",
    "name_shadow":   "#3A1204",
    "lair_bg":       "#403365",
    "info_card_fill": "#685991",
}

RARITY_COLORS = {
    "Common":    "#B5B5B5",
    "Uncommon":  "#52C724",
    "Rare":      "#1AB7FF",
    "Epic":      "#B622FF",
    "Legendary": "#FF990A",
    "Relic":     "#FF1C2B",
}
RARITY_LIST = list(RARITY_COLORS.keys())
RARITY_DEFAULT_COLOR = "#9499F7"

SPECIES_CAN_FLY = {
    'Aeroseys': True,
    'Aethereus': True,
    'Alatura': True,
    'Allpehourn': True,
    'Amaris': True,
    'Amoonita': True,
    'Ancient Aranga': True,
    'Ancient Skriffei': True,
    'Ancient Tosknir': True,
    'Andronaut': True,
    'Araneaix': True,
    'Aranga': True,
    'Archogine': True,
    'Arielisces': True,
    'Astraeisis': True,
    'Atravanta': True,
    'Aurutentia': True,
    'Avarakuma': True,
    'Avefir': True,
    'Ayatrice': True,
    'Balgunyur': True,
    'Betevial': True,
    'Bylendarach': True,
    'Caelydris': True,
    'Calimaki': True,
    'Canyarches': True,
    'Carnealgon': True,
    'Casirius': True,
    'Catruca': True,
    'Caudembris': True,
    'Caunaris': True,
    'Chameleaf': True,
    'Chippychiip': True,
    'Chronocus': True,
    'Chrysaloom': False,
    'Cirquemaar': True,
    'Cogitergosyn': True,
    'Constello': True,
    'Corrupted Chronocus': True,
    'Cosmalisk': True,
    'Cryptillow': True,
    'Cutiepatoo': True,
    'Cybernid': True,
    'Cynphion-Noire': True,
    'Desygual': True,
    'Diraixos': True,
    'Djaevelhest': True,
    'Dratheros': True,
    'Dysuva': True,
    'Eisendrache': True,
    'Eryndiorn': True,
    'Eteralix': True,
    'Fabledrak': True,
    'Falugeis': True,
    'Fayrah': True,
    'Featherfang': True,
    'Fernifex': True,
    'Firifeller': True,
    'Fleurianthus': False,
    'Flornymphis': True,
    'Fueguin': True,
    'Fulong': True,
    'Garutagoyle': True,
    'Gaulyra': False,
    'Geoteryx': True,
    'Glaquacus': True,
    'Goelica': True,
    'Goliatomb': True,
    'Gordigourd': True,
    'Guilmoros': True,
    'Gundrakken': True,
    'Gyngefared': True,
    'Gyrocopter': True,
    'Harvitius': True,
    'Hexalios': True,
    'Hielochiim': True,
    'Hoarusn': True,
    'Hongliang': True,
    'Ignicaris': True,
    'Impiavolo': True,
    'Iridesia': True,
    'Karukiri': True,
    'Khalknirik': True,
    'Khorgeryn': True,
    'Kikien': True,
    'Kostragula': True,
    'Ladonix': True,
    'Lepilon': True,
    'Livalient': True,
    'Lucklif': True,
    'Lum Luenh': True,
    'Lumenigh': True,
    'Lunaesol': True,
    'Lyria': True,
    'Makoura': True,
    'Mallopii': True,
    'Malupentys': True,
    'Mechanoxide': False,
    'Mielebee': True,
    'Mistrasune': True,
    'Moixaura': True,
    'Mosuraki': True,
    'Motorouk': False,
    'Mountain Dragon': True,
    'Nadaler': True,
    'Nakahii': False,
    'Nightmare Paranox': True,
    'Noctorius': True,
    "Nor'gan": True,
    'Nyxavoid': True,
    'Onagajin': True,
    'Oroalas': True,
    'Ortarouk': False,
    'Ovicirus': True,
    'Pagulau': True,
    'Paladianos': True,
    'Pananisea': True,
    'Paranox': True,
    'Paukiki': True,
    'Penguitus': True,
    'Phocaphan': True,
    'Phyllantis': True,
    'Polairistel': True,
    'Putrefacceum': True,
    'Quahtona': True,
    'Quasaldrus': True,
    'Quetzaloctli': True,
    'Radidon': True,
    'Raikami': True,
    'Rhyndac': True,
    'Riyu': True,
    'Robodon': True,
    'Roborus X': True,
    'Rozora': False,
    'Scrawei': True,
    'Seikarin': True,
    'Sentalius': True,
    'Silvestratus': True,
    'Skelltor': True,
    'Skriffei': True,
    'Skyrix': True,
    'Smokgien': True,
    'Snoballista': True,
    'Solarizon': True,
    'Soukeyi': True,
    'Source Dragon of Energy': True,
    'Source Dragon of Motion': True,
    'Stellaris': True,
    'Stratalix': True,
    'Stymelisk': True,
    'Suiikipon': True,
    'Sunfloris': True,
    'Syliru': True,
    'Taligris': True,
    'Tarotta': True,
    'Tempiritus': True,
    'Tenebis': True,
    'Terruak': True,
    'Thorkonyx': True,
    'Tianma': True,
    'Tlalocun': True,
    'Torneidus': True,
    'Tosknir': True,
    'Trametos': True,
    'Trilinaris': True,
    'Tronat': True,
    'Tsukuizan': True,
    'Uheailes': True,
    'Valkiero': True,
    'Varana': False,
    'Veidreki': True,
    'Venid': True,
    'Verdrakor': True,
    'Verscervus': True,
    'Viridik': True,
    'Volkumos': True,
    'Voltagen': True,
    'Voltstorm': True,
    'Vulcoramor': True,
    'Vulpiruth': True,
    'Vyreas': True,
    'Woodluma': True,
    'Wuonghou': True,
    'Xellatruce': True,
    'Xerthos': True,
    'Yaruakura': True,
    'Yggdraten': False,
    'Yueshi': True,
    'Yulereinn': True,
    'Zinthros': False,
}


LEGACY_EXAMPLE_ACCOUNTS = {"tamaraa123", "DragonTamerSuu", "WobblyPengu"}


COLOR_HEX_MAP = {
    'White': '#FFFFFF',
    'Snowflake': '#F7F9F9',
    'Whisp': '#EAEDEF',
    'Whale': '#D0CFD7',
    'Mist': '#C3C8CD',
    'Storm': '#A1ABB3',
    'Silver': '#AFAFAF',
    'Gravel': '#888F8D',
    'Felt': '#9C8E8D',
    'Bluesteel': '#6A7185',
    'Stone': '#636268',
    'Tin': '#5A6050',
    'Spirit': '#545365',
    'Gloom': '#595451',
    'Coal': '#4C4C4C',
    'Gabbro': '#4D484F',
    'Asphalt': '#413C40',
    'Ash': '#3B3736',
    'Basalt': '#332D25',
    'Scoria': '#302722',
    'Boulder': '#26262C',
    'Black': '#1A1A1B',
    'Pitch': '#0E1011',
    'Night': '#1F1A23',
    'Depth': '#22263D',
    'Blackberry': '#471A43',
    'Berry': '#4C2A4F',
    'Loulou': '#553348',
    'Lilac': '#6E235D',
    'Amarklor': '#551199',
    'Grape': '#863290',
    'Petal': '#9778BE',
    'Satin': '#7F6195',
    'Haunted': '#5C415D',
    'Ghost': '#735B77',
    'Lavender': '#8E7F9E',
    'Amethyst': '#A794B2',
    'Dart': '#AA96A6',
    'Pansy': '#E1CDFE',
    'Bubble': '#CCA4E0',
    'Plum': '#DA4FFF',
    'Purple': '#9C50D3',
    'Royal': '#7958B1',
    'Eggplant': '#993BD1',
    'Midnight': '#7930B5',
    'Urchin': '#5317B5',
    'Jelly': '#4D2C89',
    'Smog': '#3F2B66',
    'Sapphire': '#0D0A5B',
    'Angler': '#2B0D88',
    'Bluebell': '#2D237A',
    'Aster': '#484AA1',
    'Smoke': '#525195',
    'Uranus': '#4866D5',
    'Rain': '#757ADB',
    'Periwinkle': '#9499F7',
    'Stream': '#7895C1',
    'Aegean': '#4E6EA0',
    'Harpy': '#444F69',
    'Blue': '#324BA9',
    'Denim': '#212B5F',
    'Morpho': '#023489',
    'Raindrop': '#023AE2',
    'Marine': '#1C51E7',
    'Ocean': '#2F83FF',
    'Drip': '#6394DD',
    'Cool': '#76A8FF',
    'Sky': '#AEC8FF',
    'Cloud': '#89A4C0',
    'Aluminum': '#556979',
    'Iron': '#2F4557',
    'Dream': '#263746',
    'Abyss': '#0D1E25',
    'Trench': '#0B2D46',
    'Twilight': '#0A3D67',
    'Mountain': '#094869',
    'Azure': '#2B768F',
    'Shell': '#0086CE',
    'Cerulean': '#00B4D5',
    'Icecap': '#9CDDD3',
    'Winter': '#B3E1F1',
    'Glacier': '#E0FFFF',
    'Glow': '#91FFF7',
    'Cyan': '#00FFF1',
    'Bermuda': '#77DDDA',
    'Lagoon': '#09E0C7',
    'Plankton': '#18D3A9',
    'Turquoise': '#3CA2A4',
    'History': '#3A8684',
    'Spruce': '#8DBCB4',
    'Water': '#72C4C4',
    'Glass': '#9AEAEF',
    'Pistachio': '#E2FFE6',
    'Dolphin': '#B3FFD8',
    'Mint': '#9AFFC7',
    'Seafoam': '#B2E2BD',
    'Caterpillar': '#A6DBA7',
    'Jade': '#61AB89',
    'Spearmint': '#148E67',
    'Essence': '#1F565D',
    'Rainforest': '#233253',
    'Seaweed': '#153F4B',
    'Algae': '#114D41',
    'Forest': '#1F483A',
    'Hydra': '#005D48',
    'Emerald': '#20603F',
    'Shamrock': '#236825',
    'Pear': '#66903C',
    'Jungle': '#1E361A',
    'Swamp': '#1E2716',
    'Root': '#1F281D',
    'Moonrock': '#495547',
    'Snake': '#425035',
    'Camo': '#51684C',
    'Prismarine': '#4D6A6E',
    'Scale': '#516760',
    'Ivy': '#687F67',
    'Mantis': '#97AF8B',
    'Micah': '#A7B08C',
    'Pea': '#9BFF9D',
    'Synthesizer': '#03FF7D',
    'Malachite': '#87E34D',
    'Fern': '#7ECE73',
    'Stem': '#7BBD5D',
    'Green': '#629C3F',
    'Grass': '#567C34',
    'Clover': '#3ABB3B',
    'Cactus': '#8ECE56',
    'Leaf': '#A5E32D',
    'Toxin': '#C6FF00',
    'Uranium': '#CDFE6C',
    'Corrosion': '#9FFF00',
    'Peridot': '#E8FCB4',
    'Cabbage': '#D1E572',
    'Chartreuse': '#B4CD3D',
    'Prehistoric': '#A9A032',
    'Alligator': '#828335',
    'Olive': '#697135',
    'Murk': '#4B4420',
    'Bark': '#7E7645',
    'Amber': '#C18E1B',
    'Sponge': '#BEA55D',
    'Haze': '#D1B045',
    'Swallowtail': '#D1B300',
    'Lemon': '#FFE63B',
    'Wasp': '#F9E255',
    'Yolk': '#F7FF6F',
    'Banana': '#FFEC80',
    'Honey': '#FDD68B',
    'Squash': '#FDE9AC',
    'Sanddollar': '#EDE8B0',
    'Mellow': '#FFFDEA',
    'Lychee': '#FDF1E1',
    'Creme': '#FFEFDC',
    'Pelt': '#F7DEBF',
    'Ivory': '#FFD297',
    'Peanut': '#F6BF6C',
    'Gold': '#F2AD0C',
    'Marigold': '#FFB53C',
    'Apricot': '#FA912B',
    'Poppy': '#FF8500',
    'Yam': '#FF984F',
    'Orange': '#FFA147',
    'Peach': '#FFB576',
    'Silt': '#FCC4AD',
    'Sahara': '#F0B392',
    'Pecan': '#E29C7A',
    'Saffron': '#D5602B',
    'Chestnut': '#CB732D',
    'Bronze': '#B2560D',
    'Sandstone': '#B24407',
    'Carrot': '#FF5500',
    'Fire': '#EF5C23',
    'Pumpkin': '#FF6841',
    'Sunrise': '#FF7360',
    'Cinnamon': '#C15A39',
    'Caramel': '#C47149',
    'Acorn': '#B27749',
    'Tortilla': '#9A7B4F',
    'Hide': '#C3996F',
    'Beige': '#CABBA2',
    'Pine': '#827A64',
    'Soil': '#6D675B',
    'Coffee': '#564D48',
    'Cocoa': '#3C3030',
    'Chocolate': '#766259',
    'Cappuccino': '#977B6C',
    'Beach': '#BFA18F',
    'Gingerbread': '#8A6059',
    'Maple': '#7A4D4D',
    'Hazel': '#774840',
    'Coconut': '#6B3C34',
    'Clay': '#603E3D',
    'Sable': '#57372C',
    'Penny': '#432711',
    'Umber': '#301E1A',
    'Brownie': '#22110A',
    'Birch': '#2F1B1B',
    'Feldspar': '#5A4534',
    'Walnut': '#72573A',
    'Grain': '#855B33',
    'Ginger': '#91532A',
    'Starfish': '#90553A',
    'Brown': '#8E5B3F',
    'Slate': '#563012',
    'Auburn': '#7B3C1D',
    'Copper': '#A44B28',
    'Rust': '#8B3220',
    'Tomato': '#BA311C',
    'Vermillion': '#E22D18',
    'Pepper': '#CE000D',
    'Cherry': '#AA0024',
    'Crimson': '#850012',
    'Ruby': '#7A0E1E',
    'Garnet': '#581014',
    'Sanguine': '#2D0102',
    'Blood': '#451717',
    'Rose': '#652127',
    'Cranberry': '#8C272D',
    'Redwood': '#C1272D',
    'Strawberry': '#DF3236',
    'Fruit': '#FC6D68',
    'Carmine': '#B13A3A',
    'Cerise': '#A12928',
    'Brick': '#9A534D',
    'Coral': '#CC6F6F',
    'Blush': '#FEA0A0',
    'Macaron': '#FFE2E6',
    'Sakura': '#FFB7B4',
    'Flamingo': '#FEA1B3',
    'Peony': '#FFE5E5',
    'Dust': '#EBE0DF',
    'Ribbon': '#FF839B',
    'Charm': '#C67A80',
    'Taffy': '#D696B6',
    'Candy': '#EB799A',
    'Bubblegum': '#FB5E79',
    'Watermelon': '#DB518D',
    'Magenta': '#E934AA',
    'Fuschia': '#E7008B',
    'Tulip': '#CB0381',
    'Razzmatazz': '#ED2061',
    'Rubellite': '#AA004C',
    'Raspberry': '#8A024A',
    'Syrah': '#4D0F28',
    'Mauve': '#9C4975',
    'Radish': '#C44674',
    'Gum': '#E77FBF',
    'Quartz': '#E5A9FF',
    'Confetti': '#E8CCFF',
    'Petalite': '#FFD6F6',
    'Pearl': '#FBEDFA',
    'Legendary': '#FFD700',
    'Error: 2F1B1C': '#2F1B1C',
    'Error: 211919': '#211919',
    'Error: 28292B': '#28292B',
    'Error: 8C272F': '#8C272F',
    'Error: 7A87A1': '#7A87A1',
    'Error: 567C3F': '#567C3F',
    'Error: 013485': '#013485',
    'Error: 0F0A09': '#0F0A09',
    'Error: AB5D29': '#AB5D29',
    'Error: 134805': '#134805',
}

COLOR_LIST = [
    'White', 'Snowflake', 'Whisp', 'Whale', 'Mist', 'Storm', 'Silver', 'Gravel', 'Felt', 
    'Bluesteel', 'Stone', 'Tin', 'Spirit', 'Gloom', 'Coal', 'Gabbro', 'Asphalt', 'Ash', 'Basalt', 
    'Scoria', 'Boulder', 'Black', 'Pitch', 'Night', 'Depth', 'Blackberry', 'Berry', 'Loulou', 
    'Lilac', 'Amarklor', 'Grape', 'Petal', 'Satin', 'Haunted', 'Ghost', 'Lavender', 'Amethyst', 
    'Dart', 'Pansy', 'Bubble', 'Plum', 'Purple', 'Royal', 'Eggplant', 'Midnight', 'Urchin', 
    'Jelly', 'Smog', 'Sapphire', 'Angler', 'Bluebell', 'Aster', 'Smoke', 'Uranus', 'Rain', 
    'Periwinkle', 'Stream', 'Aegean', 'Harpy', 'Blue', 'Denim', 'Morpho', 'Raindrop', 'Marine', 
    'Ocean', 'Drip', 'Cool', 'Sky', 'Cloud', 'Aluminum', 'Iron', 'Dream', 'Abyss', 'Trench', 
    'Twilight', 'Mountain', 'Azure', 'Shell', 'Cerulean', 'Icecap', 'Winter', 'Glacier', 'Glow', 
    'Cyan', 'Bermuda', 'Lagoon', 'Plankton', 'Turquoise', 'History', 'Spruce', 'Water', 'Glass', 
    'Pistachio', 'Dolphin', 'Mint', 'Seafoam', 'Caterpillar', 'Jade', 'Spearmint', 'Essence', 
    'Rainforest', 'Seaweed', 'Algae', 'Forest', 'Hydra', 'Emerald', 'Shamrock', 'Pear', 'Jungle', 
    'Swamp', 'Root', 'Moonrock', 'Snake', 'Camo', 'Prismarine', 'Scale', 'Ivy', 'Mantis', 'Micah', 
    'Pea', 'Synthesizer', 'Malachite', 'Fern', 'Stem', 'Green', 'Grass', 'Clover', 'Cactus', 
    'Leaf', 'Toxin', 'Uranium', 'Corrosion', 'Peridot', 'Cabbage', 'Chartreuse', 'Prehistoric', 
    'Alligator', 'Olive', 'Murk', 'Bark', 'Amber', 'Sponge', 'Haze', 'Swallowtail', 'Lemon', 
    'Wasp', 'Yolk', 'Banana', 'Honey', 'Squash', 'Sanddollar', 'Mellow', 'Lychee', 'Creme', 
    'Pelt', 'Ivory', 'Peanut', 'Gold', 'Marigold', 'Apricot', 'Poppy', 'Yam', 'Orange', 'Peach', 
    'Silt', 'Sahara', 'Pecan', 'Saffron', 'Chestnut', 'Bronze', 'Sandstone', 'Carrot', 'Fire', 
    'Pumpkin', 'Sunrise', 'Cinnamon', 'Caramel', 'Acorn', 'Tortilla', 'Hide', 'Beige', 'Pine', 
    'Soil', 'Coffee', 'Cocoa', 'Chocolate', 'Cappuccino', 'Beach', 'Gingerbread', 'Maple', 
    'Hazel', 'Coconut', 'Clay', 'Sable', 'Penny', 'Umber', 'Brownie', 'Birch', 'Feldspar', 
    'Walnut', 'Grain', 'Ginger', 'Starfish', 'Brown', 'Slate', 'Auburn', 'Copper', 'Rust', 
    'Tomato', 'Vermillion', 'Pepper', 'Cherry', 'Crimson', 'Ruby', 'Garnet', 'Sanguine', 'Blood', 
    'Rose', 'Cranberry', 'Redwood', 'Strawberry', 'Fruit', 'Carmine', 'Cerise', 'Brick', 'Coral', 
    'Blush', 'Macaron', 'Sakura', 'Flamingo', 'Peony', 'Dust', 'Ribbon', 'Charm', 'Taffy', 
    'Candy', 'Bubblegum', 'Watermelon', 'Magenta', 'Fuschia', 'Tulip', 'Razzmatazz', 'Rubellite', 
    'Raspberry', 'Syrah', 'Mauve', 'Radish', 'Gum', 'Quartz', 'Confetti', 'Petalite', 'Pearl', 
    'Legendary', 'Error: 2F1B1C', 'Error: 211919', 'Error: 28292B', 'Error: 8C272F', 
    'Error: 7A87A1', 'Error: 567C3F', 'Error: 013485', 'Error: 0F0A09', 'Error: AB5D29', 
    'Error: 134805', 
]

MATERIAL_LIST = [
    'Asphalt', 'Basalt', 'Big Scales', 'Circuitry', 'Clean Metal', 'Clovers', 'Cobblestone', 
    'Concrete', 'Cracked Lava', 'Cracked Rock', 'Cursed', 'Diamonds', 'Fish Scales', 'Foil', 
    'Force Field', 'Fur Tufts', 'Gator Leather', 'Gemstone', 'Glacier', 'Glass', 'Granite', 
    'Grass', 'Hearts', 'Honeycomb', 'Ice', 'Limestone', 'Marble', 'Metal', 'Mud', 'Neon', 
    'Pasture', 'Patches', 'Pebble', 'Plagued', 'Pumpkin', 'Quilt', 'Rounded Scales', 'Salt', 
    'Sand', 'Sandstone', 'Scales', 'Scute', 'Serpentine', 'Sharp Scales', 'Slate', 
    'Smooth Plastic', 'Snow', 'Snowflakes', 'Star Paper', 'Static', 'Terrascale', 'Thick Fur', 
    'Thin Fur', 'Tough Leather', 'Velvet', 'Wall Paper', 'Wavy Fur', 'Weeds', 'Wood', 
    'Wood Planks', 'Worn Leather', 'Wrapping Paper', 
]

ELEMENT_LIST = [
    'Abyss',
    'Air',
    'Angel',
    'Antimatter',
    'Ashfall',
    'Aspect',
    'Aurora Borealis',
    'Auspicious Clouds',
    'Battle',
    'Binary',
    'Biohazard',
    'Bluefire',
    'Bone',
    'Bubble',
    'Campfire Tales',
    'Carrot',
    'Cat Toys',
    'Celestial',
    'Chitin',
    'Chocolate',
    'Chocolate Strawberry',
    'Christmas',
    'Classic',
    'Clover',
    'Coded Void',
    'Confetti',
    'Corrosive',
    'Cotton',
    'Dandelion',
    'Dark',
    'Death',
    'Debug',
    'Deep Sea',
    'Deepwood',
    'Demon',
    'Diamond',
    'Divine Essence',
    'Dragonseer',
    'Dream',
    'Eclipse',
    'Egged',
    'Equinox',
    'Eternal',
    'Explorer',
    'Fear',
    'Film Star',
    'Fire',
    'Fireworks',
    'Floral',
    'Fossil',
    'Frostbite',
    'Gamma Ray',
    'Ghost',
    'Gilded Moon',
    'Gold',
    'Golden Coin',
    'Grass',
    'Holly Berry',
    'Honey',
    'Ice',
    'Icicle',
    'Inferno',
    'Jelly Bean',
    'Laser',
    'Lava',
    'Life',
    'Light',
    'Lightning',
    'Love',
    'Lucky Gold',
    'Lunaris',
    'Magister',
    'Malware',
    'Maple',
    'Melody',
    'Messier',
    'Metal',
    'Mining Drill',
    'Moon',
    'Moonward',
    'Moss',
    'Nightmare',
    'Nightshade',
    'Obsession',
    'Obsidian',
    'Ocean',
    'Opal',
    'Opulent',
    'Orbit',
    'Ouroborus',
    'Paint',
    'Pan Dulce',
    'Peppermint',
    'Pixie',
    'Plasma',
    'Poison Field',
    'Prickly Rose',
    'Pulsar',
    'Pumpkin Spice',
    'Rainbow',
    'Relic',
    'Ribbon',
    'Runic Waters',
    'Sakura',
    'Scythe',
    'Seashell',
    'Shooting Star',
    'Snowflake',
    'Solar Winds',
    'Soul Flame',
    'Starlight',
    'Storm',
    'Stygian',
    'Subzero',
    'Sugar',
    'Sun',
    'Sunswept Sea',
    'Superheated',
    'Targeting System',
    'Tempest',
    'Thorned Apple',
    'Time',
    'Toxic',
    'Treasurefire',
    'Tungsten',
    'Vampire',
    'Verdant',
    'Virus',
    'Vivid Bloom',
    'War Cry',
    'Warrior',
    'Water',
    'Witch Brew',
    'Wraith',
    'Zephyr',
]

SPECIES_LIST = [
    'Aeroseys',
    'Aethereus',
    'Agricos',
    'Alatura',
    'Allpehourn',
    'Alrenoth',
    'Amaris',
    'Amoonita',
    'Amphyll',
    'Ancient Aranga',
    'Ancient Skriffei',
    'Ancient Tosknir',
    'Andronaut',
    'Araneaix',
    'Aranga',
    'Archogine',
    'Arielisces',
    'Astraeisis',
    'Atarix',
    'Atravanta',
    'Aurutentia',
    'Avarakuma',
    'Avefir',
    'Ayatrice',
    'Balgunyur',
    'Betevial',
    'Bisonture',
    'Bizaltidath',
    'Bylendarach',
    'Caelydris',
    'Calimaki',
    'Canyarches',
    'Carnealgon',
    'Casirius',
    'Catruca',
    'Caudembris',
    'Caunaris',
    'Chameleaf',
    'Chippychiip',
    'Chronocus',
    'Chrysaloom',
    'Cirquemaar',
    'Cocovira',
    'Cogitergosyn',
    'Constello',
    'Coralina',
    'Corrupted Chronocus',
    'Cosmalisk',
    'Cryptillow',
    'Cutiepatoo',
    'Cybernid',
    'Cynphion-Noire',
    'Desygual',
    'Dexyn',
    'Diraixos',
    'Djaevelhest',
    'Dratheros',
    'Dunvolth',
    'Dysuva',
    'Eisendrache',
    'Enkylous',
    'Eryndiorn',
    'Eteralix',
    'Fabledrak',
    'Falugeis',
    'Fayrah',
    'Featherfang',
    'Fernifex',
    'Ferorex',
    'Firifeller',
    'Flame',
    'Fleurianthus',
    'Flornymphis',
    'Fueguin',
    'Fulong',
    'Garutagoyle',
    'Gaulyra',
    'Geliklen',
    'Geoteryx',
    'Glacegar',
    'Glaquacus',
    'Goelica',
    'Goliatomb',
    'Gordigourd',
    'Guilmoros',
    'Gundrakken',
    'Gyngefared',
    'Gyrocopter',
    'Harvitius',
    'Hexalios',
    'Hielochiim',
    'Hoarusn',
    'Hongliang',
    'Howler',
    'Ignicaris',
    'Impiavolo',
    'Iridesia',
    'Karukiri',
    'Khalknirik',
    'Khepera',
    'Khorgeryn',
    'Kikien',
    'Kostragula',
    'Krekiz',
    'Ladonix',
    'Lepilon',
    'Livalient',
    'Lucklif',
    'Lum Luenh',
    'Lumenigh',
    'Lunaesol',
    'Lyria',
    'Magmip',
    'Makoura',
    'Mallopii',
    'Malupentys',
    'Mechanoxide',
    'Mielebee',
    'Mistrasune',
    'Moixaura',
    'Mosuraki',
    'Mother Dragon',
    'Motorouk',
    'Mountain Dragon',
    'Nadaler',
    'Nakahii',
    'Neroxide',
    'Nightmare Paranox',
    'Noctorius',
    "Nor'gan",
    'Numine',
    'Nyxavoid',
    'Onagajin',
    'Oroalas',
    'Ortarouk',
    'Ovicirus',
    'Pagulau',
    'Paladianos',
    'Palus',
    'Pananisea',
    'Paranox',
    'Paukiki',
    'Penguitus',
    'Phocaphan',
    'Phyllantis',
    'Polairistel',
    'Putrefacceum',
    'Quahtona',
    'Quasaldrus',
    'Quetzaloctli',
    'Radidon',
    'Raikami',
    'Rhyndac',
    'Riyu',
    'Robodon',
    'Roborus V',
    'Roborus X',
    'Rocirus',
    'Rozora',
    'Saurium',
    'Scrawei',
    'Seikarin',
    'Sentalius',
    'Shard',
    'Silvestratus',
    'Skelltor',
    'Skriffei',
    'Skyrix',
    'Smokgien',
    'Snoballista',
    'Solarizon',
    'Soukeyi',
    'Source Dragon of Energy',
    'Source Dragon of Motion',
    'Stellaris',
    'Stratalix',
    'Stymelisk',
    'Suiikipon',
    'Sunfloris',
    'Syliru',
    'Sylva',
    'Taihoa',
    'Taligris',
    'Taraka',
    'Tarotta',
    'Tempiritus',
    'Tenebis',
    'Terruak',
    'Thorkonyx',
    'Tianma',
    'Tigrilia',
    'Tlalocun',
    'Torneidus',
    'Tosknir',
    'Trametos',
    'Trilinaris',
    'Tronat',
    'Tsukuizan',
    'Tuskaryn',
    'Uheailes',
    'Valkiero',
    'Varana',
    'Veidreki',
    'Venid',
    'Venu',
    'Verdrakor',
    'Verscervus',
    'Viridik',
    'Volkumos',
    'Voltagen',
    'Voltstorm',
    'Vulcoramor',
    'Vulpiruth',
    'Vyreas',
    'Woodluma',
    'Wuonghou',
    'Xellatruce',
    'Xerthos',
    'Yaruakura',
    'Yggdraten',
    'Yueshi',
    'Yulereinn',
    'Zeipera',
    'Zinthros',
]

SPECIES_RARITY = {
    'Cogitergosyn': 'Legendary',
    'Putrefacceum': 'Relic',
    'Veidreki': 'Relic',
    'Voltstorm': 'Relic',
    'Alatura': 'Legendary',
    'Allpehourn': 'Legendary',
    'Amaris': 'Legendary',
    'Ancient Aranga': 'Legendary',
    'Ancient Skriffei': 'Legendary',
    'Ancient Tosknir': 'Legendary',
    'Aranga': 'Legendary',
    'Aurutentia': 'Legendary',
    'Avarakuma': 'Legendary',
    'Betevial': 'Legendary',
    'Bylendarach': 'Legendary',
    'Catruca': 'Legendary',
    'Chippychiip': 'Legendary',
    'Constello': 'Legendary',
    'Corrupted Chronocus': 'Legendary',
    'Cosmalisk': 'Legendary',
    'Cryptillow': 'Legendary',
    'Cynphion-Noire': 'Legendary',
    'Djaevelhest': 'Legendary',
    'Dratheros': 'Legendary',
    'Eryndiorn': 'Legendary',
    'Eteralix': 'Legendary',
    'Fabledrak': 'Legendary',
    'Flornymphis': 'Legendary',
    'Fulong': 'Legendary',
    'Gaulyra': 'Legendary',
    'Goelica': 'Legendary',
    'Guilmoros': 'Legendary',
    'Gundrakken': 'Legendary',
    'Gyrocopter': 'Legendary',
    'Ignicaris': 'Legendary',
    'Khorgeryn': 'Legendary',
    'Kikien': 'Legendary',
    'Kostragula': 'Legendary',
    'Ladonix': 'Legendary',
    'Livalient': 'Legendary',
    'Lumenigh': 'Legendary',
    'Lyria': 'Legendary',
    'Mallopii': 'Legendary',
    'Malupentys': 'Legendary',
    'Moixaura': 'Legendary',
    'Motorouk': 'Legendary',
    'Oroalas': 'Legendary',
    'Ortarouk': 'Legendary',
    'Paladianos': 'Legendary',
    'Penguitus': 'Legendary',
    'Polairistel': 'Legendary',
    'Quetzaloctli': 'Legendary',
    'Raikami': 'Legendary',
    'Riyu': 'Legendary',
    'Roborus V': 'Legendary',
    'Seikarin': 'Legendary',
    'Sentalius': 'Legendary',
    'Silvestratus': 'Legendary',
    'Source Dragon of Energy': 'Legendary',
    'Source Dragon of Motion': 'Legendary',
    'Stellaris': 'Legendary',
    'Stratalix': 'Legendary',
    'Taligris': 'Legendary',
    'Terruak': 'Legendary',
    'Tianma': 'Legendary',
    'Tlalocun': 'Legendary',
    'Tosknir': 'Legendary',
    'Tronat': 'Legendary',
    'Uheailes': 'Legendary',
    'Verdrakor': 'Legendary',
    'Voltagen': 'Legendary',
    'Vulcoramor': 'Legendary',
    'Vyreas': 'Legendary',
    'Xellatruce': 'Legendary',
    'Yggdraten': 'Legendary',
    'Aeroseys': 'Epic',
    'Aethereus': 'Epic',
    'Amoonita': 'Epic',
    'Andronaut': 'Epic',
    'Araneaix': 'Epic',
    'Arielisces': 'Epic',
    'Astraeisis': 'Epic',
    'Atravanta': 'Epic',
    'Balgunyur': 'Epic',
    'Caelydris': 'Epic',
    'Calimaki': 'Epic',
    'Carnealgon': 'Epic',
    'Casirius': 'Epic',
    'Caudembris': 'Epic',
    'Caunaris': 'Epic',
    'Chameleaf': 'Epic',
    'Chrysaloom': 'Epic',
    'Cirquemaar': 'Epic',
    'Cutiepatoo': 'Epic',
    'Desygual': 'Epic',
    'Diraixos': 'Epic',
    'Eisendrache': 'Epic',
    'Falugeis': 'Epic',
    'Fernifex': 'Epic',
    'Firifeller': 'Epic',
    'Fleurianthus': 'Epic',
    'Fueguin': 'Epic',
    'Geoteryx': 'Epic',
    'Glaquacus': 'Epic',
    'Goliatomb': 'Epic',
    'Gordigourd': 'Epic',
    'Gyngefared': 'Epic',
    'Harvitius': 'Epic',
    'Hoarusn': 'Epic',
    'Hongliang': 'Epic',
    'Impiavolo': 'Epic',
    'Iridesia': 'Epic',
    'Karukiri': 'Epic',
    'Khalknirik': 'Epic',
    'Lucklif': 'Epic',
    'Lum Luenh': 'Epic',
    'Lunaesol': 'Epic',
    'Makoura': 'Epic',
    'Mechanoxide': 'Epic',
    'Mielebee': 'Epic',
    'Mistrasune': 'Epic',
    'Mosuraki': 'Epic',
    'Mountain Dragon': 'Epic',
    'Nakahii': 'Epic',
    'Nightmare Paranox': 'Epic',
    'Noctorius': 'Epic',
    "Nor'gan": 'Epic',
    'Nyxavoid': 'Epic',
    'Ovicirus': 'Epic',
    'Pagulau': 'Epic',
    'Pananisea': 'Epic',
    'Phocaphan': 'Epic',
    'Phyllantis': 'Epic',
    'Quahtona': 'Epic',
    'Quasaldrus': 'Epic',
    'Robodon': 'Epic',
    'Roborus X': 'Epic',
    'Rozora': 'Epic',
    'Smokgien': 'Epic',
    'Snoballista': 'Epic',
    'Stymelisk': 'Epic',
    'Sunfloris': 'Epic',
    'Syliru': 'Epic',
    'Tempiritus': 'Epic',
    'Tenebis': 'Epic',
    'Thorkonyx': 'Epic',
    'Torneidus': 'Epic',
    'Trametos': 'Epic',
    'Trilinaris': 'Epic',
    'Tsukuizan': 'Epic',
    'Valkiero': 'Epic',
    'Varana': 'Epic',
    'Verscervus': 'Epic',
    'Viridik': 'Epic',
    'Volkumos': 'Epic',
    'Vulpiruth': 'Epic',
    'Woodluma': 'Epic',
    'Wuonghou': 'Epic',
    'Yueshi': 'Epic',
    'Alrenoth': 'Rare',
    'Coralina': 'Rare',
    'Dunvolth': 'Rare',
    'Dysuva': 'Rare',
    'Fayrah': 'Rare',
    'Featherfang': 'Rare',
    'Ferorex': 'Rare',
    'Glacegar': 'Rare',
    'Hexalios': 'Rare',
    'Hielochiim': 'Rare',
    'Krekiz': 'Rare',
    'Lepilon': 'Rare',
    'Mother Dragon': 'Rare',
    'Nadaler': 'Rare',
    'Onagajin': 'Rare',
    'Paranox': 'Rare',
    'Radidon': 'Rare',
    'Solarizon': 'Rare',
    'Soukeyi': 'Rare',
    'Xerthos': 'Rare',
    'Yulereinn': 'Rare',
    'Zinthros': 'Rare',
    'Avefir': 'Uncommon',
    'Ayatrice': 'Uncommon',
    'Bisonture': 'Uncommon',
    'Bizaltidath': 'Uncommon',
    'Chronocus': 'Uncommon',
    'Cybernid': 'Uncommon',
    'Magmip': 'Uncommon',
    'Paukiki': 'Uncommon',
    'Scrawei': 'Uncommon',
    'Sylva': 'Uncommon',
    'Taraka': 'Uncommon',
    'Tarotta': 'Uncommon',
    'Tigrilia': 'Uncommon',
    'Tuskaryn': 'Uncommon',
    'Venid': 'Uncommon',
    'Yaruakura': 'Uncommon',
    'Zeipera': 'Uncommon',
    'Agricos': 'Common',
    'Amphyll': 'Common',
    'Atarix': 'Common',
    'Cocovira': 'Common',
    'Dexyn': 'Common',
    'Enkylous': 'Common',
    'Geliklen': 'Common',
    'Howler': 'Common',
    'Khepera': 'Common',
    'Neroxide': 'Common',
    'Numine': 'Common',
    'Palus': 'Common',
    'Rhyndac': 'Common',
    'Rocirus': 'Common',
    'Saurium': 'Common',
    'Skelltor': 'Common',
    'Skriffei': 'Common',
    'Skyrix': 'Common',
    'Suiikipon': 'Common',
    'Taihoa': 'Common',
    'Venu': 'Common',
    'Canyarches': 'Legendary',
    'Garutagoyle': 'Legendary',
    'Archogine': 'Legendary',
    'Flame': 'Epic',
    'Shard': 'Epic',
}

PUPIL_LIST = [
    'Round', 'Slit', 'Empty', 'Square', 'Sparkle', 'Star', 'Confused', 'Legendary', 
]

COSMETIC_TRAIT_LIST = [
    '[Error:Cosmetic]',
    'Ace of Cards',
    'Albinism',
    'Astrologic Aura',
    'Aura',
    'Bat Swarm',
    'Bioluminescent Aura',
    'Black Hole',
    'Blizzard',
    'Blooming Aura',
    'Blossoming Aura',
    'Blossoming Head Aura',
    'Blossoming Tail Aura',
    'Bloxfest 2026 Shimmer',
    'Celestial Blaze',
    'Chaos Aura',
    'Chilly',
    'Christmas Lights',
    'Clover',
    'Cosmic Traveller',
    'Cozy Campfire',
    'Crystallized',
    'Digital Make',
    'Easter Bunny',
    'Easter Egg Aura',
    'Easter Egg Head Aura',
    'Easter Egg Tail Aura',
    'Electric',
    'Electric Head',
    'Electric Tail',
    'Enchanted Meadows',
    'Envelopes',
    'Fluttering Aura',
    'Frosted',
    'Ghost Aura',
    'Gold Coins',
    'Golden Shimmer',
    'Guiding Star',
    'Head Aura',
    'Headless',
    'Heartbreak Aura',
    'Hologrammic',
    'Homestead',
    'Honey Aura',
    'Honeybees',
    'Icicle',
    'Inflamed',
    'Inflamed Head',
    'Inflamed Tail',
    'Jewel Rush',
    'Landslide',
    'Lantern Lights',
    'Loving Aura',
    'Loving Head Aura',
    'Loving Tail Aura',
    'Lucky Aura',
    'Lucky Head Aura',
    'Lucky Tail Aura',
    'Malfunction',
    'Melanism',
    'Moonfall',
    'None',
    'Northern Lights',
    'Noxious',
    'Pastel Chalk',
    'Platinum',
    'Poison',
    'Pollen Aura',
    'Primordial Storm',
    'Ribbon',
    'Ring of Fire',
    'Robotics',
    'Seashell',
    'Shadow',
    'Snowman',
    'Solar Rays',
    'Storm Circuit',
    'Storm Surge',
    'Suncatcher',
    'Super Computer',
    'Supercharged',
    'Tail Aura',
    'Virus',
    'Wild Eye Aura',
]


FLYING_ONLY_POSITIVE  = {"Strong Wing Membrane"}
NONFLYING_ONLY_POSITIVE = {"Swifter Leap"}
FLYING_ONLY_NEGATIVE  = {"Thin Wing Membrane"}


def species_can_fly(species):
    return SPECIES_CAN_FLY.get(species, True)


def available_positive_traits(species):
    if species_can_fly(species):
        return [t for t in POSITIVE_TRAIT_LIST if t not in NONFLYING_ONLY_POSITIVE]
    else:
        return [t for t in POSITIVE_TRAIT_LIST if t not in FLYING_ONLY_POSITIVE]


def available_negative_traits(species):
    if species_can_fly(species):
        return list(NEGATIVE_TRAIT_LIST)
    else:
        return [t for t in NEGATIVE_TRAIT_LIST if t not in FLYING_ONLY_NEGATIVE]

MUTATION_CAP = 5
GENDER_LIST = ["Male", "Female"]
SDA_EXCLUDED = {
    'Flame',
    'Mountain Dragon',
    'Riyu',
    'Shard',
    'Source Dragon of Energy',
    'Source Dragon of Motion',
}
AGE_LIST = ["Baby", "Juvenile", "Adult", "Elder"]
MONTH_NAMES = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]
BIRTHDAY_MIN_YEAR = 1969

POSITIVE_TRAIT_LIST = [
    "None", "Aerodynamic Body", "Beautiful", "High IQ", "Large Lungs", "Sharp Teeth",
    "Slow Metabolism", "Strong Immune System", "Strong Joints", "Strong Wing Membrane",
    "Swifter Leap", "Thermal Resistance", "Tough Skin",
]
NEGATIVE_TRAIT_LIST = [
    "None", "Allergies", "Brittle Joints", "Fast Metabolism", "Hemophilia", "Low IQ",
    "Thin Skin", "Thin Wing Membrane", "Ugly", "Weak Lungs",
]
MAX_POSITIVE_TRAITS = 5
MAX_NEGATIVE_TRAITS = 2
TRAIT_TIER_MIN, TRAIT_TIER_MAX = 1, 10

ELEMENT_COLOR_OVERRIDES = {
    "Fire": "#FF5C2E", "Grass": "#4CAF50", "Water": "#3D8EDB", "Lightning": "#F2D11D",
    "Ice": "#7FD8F2", "Dark": "#1A1A22", "Light": "#FFF3C2", "Toxic": "#9FFF00",
    "Demon": "#7A0E1E", "Angel": "#FFE9A8", "Sun": "#FFB300", "Moon": "#C9D6E8",
    "Lava": "#FF4500", "Air": "#D9F2EA", "Ocean": "#2F83FF", "Abyss": "#0D1E25",
    "Bone": "#E8DFC8", "Ghost": "#C9C2E8", "Christmas": "#C8102E", "Gold": "#F2AD0C",
    "Diamond": "#BEEFFF", "Rainbow": "#FF6FCB", "Storm": "#6E7B8B", "Frostbite": "#AEE9FF",
    "Antimatter": "#2B0D88", "Corrosive": "#9FFF00", "Death": "#3B3736", "Life": "#3ABB3B",
    "Equinox": "#B884FF", "Wraith": "#5C415D", "Celestial": "#9499F7", "Metal": "#9C9C9C",
    "Plasma": "#E934AA", "Eclipse": "#22110A", "Solar Winds": "#FF8500", "Battle": "#8B3220",
    "Warrior": "#A44B28", "Love": "#FB5E79", "Honey": "#FDD68B", "Carrot": "#FF8500",
    "Moss": "#3ABB3B", "Sakura": "#FFB7B4", "Bluefire": "#2F83FF", "Relic": "#B2560D",
    "Tempest": "#6E7B8B",
}


def element_hash_color(name):
    """Deterministic fallback color for any element without a hand-picked one."""
    h = int(hashlib.md5(name.encode("utf-8")).hexdigest(), 16)
    hue = (h % 360) / 360.0
    sat = 0.55 + ((h // 360) % 30) / 100.0
    light = 0.42 + ((h // 360 // 30) % 22) / 100.0
    r, g, b = colorsys.hls_to_rgb(hue, light, sat)
    return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"


def get_element_color(name):
    return ELEMENT_COLOR_OVERRIDES.get(name) or element_hash_color(name)


def get_color_hex(name, element=None):
    """Resolve a Color dropdown value to a hex. 'Legendary' dynamically
    matches the dragon's element instead of having one fixed color."""
    if name == "Legendary" and element:
        return get_element_color(element)
    return COLOR_HEX_MAP.get(name, "#777777")


def readable_text_color(hex_color):
    """Pick black or white text so it stays legible on any pill/swatch color."""
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "#1A1A1B" if luminance > 0.55 else "#FFFFFF"


if getattr(sys, "frozen", False):
    SCRIPT_DIR = os.path.dirname(sys.executable)
else:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(SCRIPT_DIR, "dragons_data.json")
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
ICON_DIR = os.path.join(SCRIPT_DIR, "assets", "icons")
LEGENDARY_SHIFT_DIR = os.path.join(SCRIPT_DIR, "assets", "legendary_shifts")
MISC_DIR = os.path.join(SCRIPT_DIR, "assets", "misc")
DRAGON_ICONS_DIR = os.path.join(SCRIPT_DIR, "assets", "dragonicons")
DRAGON_IMAGES_DIR = os.path.join(SCRIPT_DIR, "assets", "dragon_images")
COSMETIC_TRAIT_ICON_DIR = os.path.join(SCRIPT_DIR, "assets", "misc", "cosmetictrait")
FONTS_DIR = os.path.join(SCRIPT_DIR, "assets", "fonts")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(ICON_DIR, exist_ok=True)
os.makedirs(LEGENDARY_SHIFT_DIR, exist_ok=True)
os.makedirs(MISC_DIR, exist_ok=True)
os.makedirs(DRAGON_ICONS_DIR, exist_ok=True)
os.makedirs(DRAGON_IMAGES_DIR, exist_ok=True)
os.makedirs(COSMETIC_TRAIT_ICON_DIR, exist_ok=True)
os.makedirs(FONTS_DIR, exist_ok=True)

APP_FONT_FAMILY = "Fredoka"
APP_VERSION = "1.4.0"
GITHUB_REPO = "I-Verian/The-Lairkeeper"
APP_FONT_WEIGHT = "bold"


def load_custom_fonts():
    """Privately registers any .ttf/.otf files in assets/fonts/ for this
    process only (Windows) — so a custom font like Ultima Black works even
    on a machine that doesn't have it actually installed, as long as the
    font file is dropped in that folder. Writes what happened to both the
    console AND a font_debug.log next to the script/exe, since a missing or
    misnamed font fails completely silently otherwise — and if you're
    running the packaged --windowed .exe, there's no console to see prints
    in at all, so the log file is the only way to actually check."""
    lines = []

    def log(msg):
        lines.append(msg)
        print(msg)

    if sys.platform != "win32":
        log(f"[fonts] Not on Windows — skipping private font loading. "
            f"'{APP_FONT_FAMILY}' must be installed normally for it to show up.")
    else:
        font_files = [f for f in os.listdir(FONTS_DIR) if f.lower().endswith((".ttf", ".otf"))]
        if not font_files:
            log(f"[fonts] No .ttf/.otf files found in: {FONTS_DIR}")
            log(f"        Drop an '{APP_FONT_FAMILY}' font file in there for it to be used.")
        else:
            FR_PRIVATE = 0x10
            for fname in font_files:
                try:
                    n_added = ctypes.windll.gdi32.AddFontResourceExW(
                        os.path.join(FONTS_DIR, fname), FR_PRIVATE, 0)
                    if n_added:
                        log(f"[fonts] Registered: {fname} ({n_added} face(s) added)")
                    else:
                        log(f"[fonts] FAILED to register {fname} — Windows returned 0 faces added "
                            f"(file may be corrupt or not a valid font)")
                except Exception as e:
                    log(f"[fonts] Failed to register {fname}: {e}")
            try:
                HWND_BROADCAST, WM_FONTCHANGE = 0xFFFF, 0x001D
                ctypes.windll.user32.SendMessageW(HWND_BROADCAST, WM_FONTCHANGE, 0, 0)
            except Exception:
                pass

    try:
        resolved = tkfont.Font(family=APP_FONT_FAMILY, size=20, weight=APP_FONT_WEIGHT).actual()
        if resolved.get("family", "").lower() == APP_FONT_FAMILY.lower():
            log(f"[fonts] SUCCESS — Tk resolved ('{APP_FONT_FAMILY}', 20, '{APP_FONT_WEIGHT}') "
                f"to itself: {resolved}")
        else:
            log(f"[fonts] NOT APPLIED — asked for '{APP_FONT_FAMILY}' but Tk is actually using "
                f"'{resolved.get('family')}' instead: {resolved}")
            log(f"        This usually means either (a) the font file's INTERNAL name doesn't "
                f"match '{APP_FONT_FAMILY}' exactly (filenames don't count — open the font in "
                f"Windows' Font Viewer to check the real name), or (b) the file didn't register.")
    except Exception as e:
        log(f"[fonts] Could not verify font resolution: {e}")

    try:
        with open(os.path.join(SCRIPT_DIR, "font_debug.log"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    except Exception:
        pass


def fit_text_size(text, family, max_size, min_size, max_width, weight=APP_FONT_WEIGHT):
    """Shrinks the font size (down to min_size) until `text` measures within
    max_width in this family/weight — keeps long dragon names from spilling
    past their available space instead of just clipping or overlapping."""
    size = max_size
    while size > min_size:
        try:
            measured = tkfont.Font(family=family, size=size, weight=weight).measure(text)
        except Exception:
            return size
        if measured <= max_width:
            return size
        size -= 1
    return min_size


DEFAULT_DRAGONS = {}

LEGACY_DEMO_DRAGON_IDS = {"ferorex", "zinthros", "amoonita"}


def species_icon_path(species):
    base_underscore = species.replace(" ", "_")
    base_nospace = species.replace(" ", "")
    base_lower = species.lower().replace(" ", "_")
    base_lower_nospace = species.lower().replace(" ", "")
    candidates = [
        f"{base_underscore}_Icon.png",
        f"{base_underscore}_icon.png",
        f"{base_underscore}.png",
        f"{base_nospace}_Icon.png",
        f"{base_nospace}_icon.png",
        f"{base_nospace}.png",
        f"{species}_Icon.png",
        f"{species}_icon.png",
        f"{species}.png",
        f"{base_lower}_icon.png",
        f"{base_lower}.png",
        f"{base_lower_nospace}_icon.png",
        f"{base_lower_nospace}.png",
    ]
    try:
        existing = {fname.lower(): fname for fname in os.listdir(DRAGON_ICONS_DIR)}
    except Exception:
        existing = {}
    for candidate in candidates:
        match = existing.get(candidate.lower())
        if match:
            return os.path.join(DRAGON_ICONS_DIR, match)
    return os.path.join(DRAGON_ICONS_DIR, candidates[0])


def migrate_dragon(d):
    """Upgrade an entry saved by an older version of this script
    (Patterns/Finish field names, no Generation, etc.) in place."""
    if "Colors" not in d and "Patterns" in d:
        d["Colors"] = d.pop("Patterns")
    if "Materials" not in d or isinstance(d.get("Materials"), list):
        if "Finish" in d:
            d["Materials"] = d.pop("Finish")
        else:
            d["Materials"] = {"P": "-", "S": "-", "T": "-"}
    d.pop("Finish", None)
    d.pop("Title", None)
    d.pop("Hunger", None)
    d.pop("MaxHunger", None)
    d.pop("Health", None)
    d.pop("MaxHealth", None)
    d.pop("Image", None)
    d.setdefault("Generation", "-")
    d.setdefault("MaxMutations", MUTATION_CAP)
    d.setdefault("CosmeticTrait", "None")
    d.setdefault("Pupil", "-")
    d.setdefault("Element", "-")
    d.setdefault("Gender", "")
    d.setdefault("Soulbound", False)
    d.setdefault("Element2", None)
    d.setdefault("Note", "")
    d.setdefault("Birthday", None)
    d.setdefault("OriginalOwner", None)
    d.setdefault("Level", "-")
    d.setdefault("Age", "-")
    d.setdefault("PositiveTraits", [])
    d.setdefault("NegativeTraits", [])

    return d


TABS_KEY = "__tabs__"
import shutil


def _account_dir(account_name):
    return os.path.join(DATA_DIR, account_name)


def _dragon_path(account_name, dragon_id):
    return os.path.join(_account_dir(account_name), f"{dragon_id}.json")


def _tabs_path(account_name):
    return os.path.join(_account_dir(account_name), "__tabs__.json")


def _settings_path(account_name):
    return os.path.join(_account_dir(account_name), "__settings__.json")


def load_account_settings(account_name):
    p = _settings_path(account_name)
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_account_settings(account_name, settings):
    adir = _account_dir(account_name)
    os.makedirs(adir, exist_ok=True)
    try:
        with open(_settings_path(account_name), "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)
    except Exception as e:
        print(f"Could not save settings for {account_name}:", e)


account_settings = {}


def _write_account(account_name, dragon_dict, tabs_dict):
    """Write all files for one account: one JSON per dragon + one tabs file.
    Also removes orphaned dragon files that no longer exist in dragon_dict."""
    adir = _account_dir(account_name)
    os.makedirs(adir, exist_ok=True)

    try:
        with open(_tabs_path(account_name), "w", encoding="utf-8") as f:
            json.dump(tabs_dict, f, indent=2)
    except Exception as e:
        print(f"Could not save tabs for {account_name}:", e)

    for did, d in dragon_dict.items():
        try:
            with open(_dragon_path(account_name, did), "w", encoding="utf-8") as f:
                json.dump(d, f, indent=2)
        except Exception as e:
            print(f"Could not save dragon {did}:", e)

    try:
        existing_ids = {
            fname[:-5] for fname in os.listdir(adir)
            if fname.endswith(".json") and fname != "__tabs__.json"
        }
        for orphan in existing_ids - set(dragon_dict.keys()):
            try:
                os.remove(_dragon_path(account_name, orphan))
            except Exception:
                pass
    except Exception:
        pass


def _read_account(account_name):
    """Read all dragon files + tabs for one account. Returns (dragon_dict, tabs_dict)."""
    adir = _account_dir(account_name)
    dragon_dict = {}
    tabs_dict = {}

    if not os.path.isdir(adir):
        return dragon_dict, tabs_dict

    tabs_file = _tabs_path(account_name)
    if os.path.exists(tabs_file):
        try:
            with open(tabs_file, "r", encoding="utf-8") as f:
                tabs_dict = json.load(f)
        except Exception as e:
            print(f"Could not read tabs for {account_name}:", e)

    for fname in os.listdir(adir):
        if not fname.endswith(".json") or fname == "__tabs__.json":
            continue
        dragon_id = fname[:-5]
        try:
            with open(os.path.join(adir, fname), "r", encoding="utf-8") as f:
                dragon_dict[dragon_id] = migrate_dragon(json.load(f))
        except Exception as e:
            print(f"Could not read dragon file {fname}:", e)

    return dragon_dict, tabs_dict


def _migrate_from_legacy():
    """If the old monolithic dragons_data.json exists and the new data/
    directory doesn't, convert everything across and rename the old file."""
    if not os.path.exists(DATA_FILE):
        return
    if os.path.exists(DATA_DIR):
        return

    print("[data] Migrating from dragons_data.json to per-dragon files…")
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception as e:
        print("[data] Could not read legacy file:", e)
        return

    if not raw:
        return

    first_value = next(iter(raw.values()))
    if isinstance(first_value, dict) and "Nickname" in first_value:
        raw = {"Player1": raw}

    for acc, roster in raw.items():
        if acc in LEGACY_EXAMPLE_ACCOUNTS:
            continue
        tabs = roster.pop(TABS_KEY, {})
        dragons_in_acc = {k: migrate_dragon(v) for k, v in roster.items()}
        _write_account(acc, dragons_in_acc, tabs)

    try:
        os.rename(DATA_FILE, DATA_FILE + ".migrated")
        print("[data] Migration complete. Old file renamed to dragons_data.json.migrated")
    except Exception:
        pass


def load_all_accounts():
    _migrate_from_legacy()

    data = {}
    if os.path.isdir(DATA_DIR):
        for account_name in os.listdir(DATA_DIR):
            if not os.path.isdir(_account_dir(account_name)):
                continue
            if account_name in LEGACY_EXAMPLE_ACCOUNTS:
                continue
            dragon_dict, tabs_dict = _read_account(account_name)
            data[account_name] = {**dragon_dict, TABS_KEY: tabs_dict}

    return data


def save_all_accounts(data):
    for acc, roster in data.items():
        tabs = roster.get(TABS_KEY, {})
        dragons_in_acc = {k: v for k, v in roster.items() if k != TABS_KEY}
        _write_account(acc, dragons_in_acc, tabs)


all_accounts_data = load_all_accounts()
current_account = None
dragons = {}
current_tabs = {}


def get_account_dragons():
    return {k: v for k, v in all_accounts_data.get(current_account, {}).items()
            if k != TABS_KEY}


def switch_account(account_name):
    global dragons, current_tabs, current_account, account_settings
    current_account = account_name
    slot = all_accounts_data.setdefault(account_name, {})
    if TABS_KEY not in slot:
        slot[TABS_KEY] = {}
    dragons = {k: v for k, v in slot.items() if k != TABS_KEY}
    current_tabs = slot[TABS_KEY]
    account_settings = load_account_settings(account_name)


def persist():
    account_slot = all_accounts_data.setdefault(current_account, {})
    account_slot[TABS_KEY] = current_tabs
    for k, v in dragons.items():
        account_slot[k] = v
    for k in list(account_slot.keys()):
        if k != TABS_KEY and k not in dragons:
            del account_slot[k]
    _write_account(current_account, dragons, current_tabs)


def create_tab(name):
    tab_id = uuid.uuid4().hex[:10]
    current_tabs[tab_id] = {"name": name, "members": []}
    persist()
    return tab_id


def delete_tab(tab_id):
    current_tabs.pop(tab_id, None)
    persist()


def rename_tab(tab_id, new_name):
    if tab_id in current_tabs:
        current_tabs[tab_id]["name"] = new_name
        persist()


def add_dragon_to_tab(tab_id, dragon_id):
    if tab_id in current_tabs and dragon_id not in current_tabs[tab_id]["members"]:
        current_tabs[tab_id]["members"].append(dragon_id)
        persist()


def remove_dragon_from_tab(tab_id, dragon_id):
    if tab_id in current_tabs and dragon_id in current_tabs[tab_id]["members"]:
        current_tabs[tab_id]["members"].remove(dragon_id)
        persist()


def move_dragon_to_account(dragon_id, dest_account):
    if dragon_id not in dragons or dest_account == current_account:
        return False

    record = dragons.pop(dragon_id)

    for tab in current_tabs.values():
        if dragon_id in tab.get("members", []):
            tab["members"].remove(dragon_id)

    dest_slot = all_accounts_data.setdefault(dest_account, {})
    if TABS_KEY not in dest_slot:
        dest_slot[TABS_KEY] = {}

    new_id = dragon_id
    if new_id in dest_slot:
        new_id = uuid.uuid4().hex[:10]
    dest_slot[new_id] = record

    persist()

    dest_dragons = {k: v for k, v in dest_slot.items() if k != TABS_KEY}
    _write_account(dest_account, dest_dragons, dest_slot.get(TABS_KEY, {}))

    return True


def center(win, w, h):
    x = (win.winfo_screenwidth() - w) // 2
    y = (win.winfo_screenheight() - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")


def set_window_icon(win):
    """Sets the title-bar/taskbar icon from assets/misc/dragonhead.png.
    Called once on the root window — default=True makes it the default
    icon for every Toplevel opened afterward too. No-ops quietly if the
    file isn't there yet."""
    try:
        path = os.path.join(MISC_DIR, "dragonhead.png")
        photo = ImageTk.PhotoImage(Image.open(path))
        win._icon_ref = photo
        win.iconphoto(True, photo)
    except Exception:
        pass


def lighten(hex_color, amount=18):
    """Positive amount lightens, negative amount darkens."""
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    r, g, b = (max(0, min(255, c + amount)) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


def round_rect(canvas, x1, y1, x2, y2, r=18, **kwargs):
    """Draw a rounded rectangle on a Canvas using a smoothed polygon."""
    r = min(r, abs(x2 - x1) / 2, abs(y2 - y1) / 2)
    points = [
        x1 + r, y1,
        x2 - r, y1,
        x2, y1,
        x2, y1 + r,
        x2, y2 - r,
        x2, y2,
        x2 - r, y2,
        x1 + r, y2,
        x1, y2,
        x1, y2 - r,
        x1, y1 + r,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


def outline_text(canvas, x, y, text, font, fill, outline, **kwargs):
    """Cheap text-stroke effect: draw the outline color offset in 8 directions,
    then the real fill on top, for that chunky game-font look."""
    offsets = [(-2, 0), (2, 0), (0, -2), (0, 2),
               (-1, -1), (1, 1), (-1, 1), (1, -1)]
    for dx, dy in offsets:
        canvas.create_text(x + dx, y + dy, text=text, font=font,
                            fill=outline, **kwargs)
    canvas.create_text(x, y, text=text, font=font, fill=fill, **kwargs)


def shadowed_name_text(canvas, x, y, text, font, **kwargs):
    """Dragon-name styling: a drop shadow behind a stroked, filled title."""
    shadow_dx, shadow_dy = 3, 3
    canvas.create_text(x + shadow_dx, y + shadow_dy, text=text, font=font,
                        fill=PALETTE["name_shadow"], **kwargs)
    outline_text(canvas, x, y, text, font, PALETTE["name_fill"], PALETTE["name_outline"], **kwargs)


def draw_star(canvas, cx, cy, r, fill, outline):
    pts = []
    for i in range(10):
        angle = math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append(cx + rad * math.cos(angle))
        pts.append(cy - rad * math.sin(angle))
    canvas.create_polygon(pts, fill=fill, outline=outline, width=2)


def draw_bar(canvas, x, y, w, h, value, max_value, text=None):
    """Glowing rounded stat bar a-la Dragon Adventures."""
    round_rect(canvas, x, y, x + w, y + h, r=h / 2,
                fill=PALETTE["bar_track"], outline=PALETTE["bar_border"], width=2)

    frac = 1.0 if not max_value else max(0.0, min(1.0, value / max_value))
    fill_w = max(h, w * frac)
    if frac > 0:
        round_rect(canvas, x, y, x + fill_w, y + h, r=h / 2,
                    fill=PALETTE["bar_fill"], outline="", width=0)
        round_rect(canvas, x, y, x + fill_w, y + h, r=h / 2,
                    fill="", outline=PALETTE["bar_border"], width=2)

    if text is None:
        text = f"{value:,}/{max_value:,}" if isinstance(value, int) else f"{value}/{max_value}"
    outline_text(canvas, x + w / 2, y + h / 2, text, (APP_FONT_FAMILY, 12, APP_FONT_WEIGHT),
                 "white", "#1A3D10")


def setup_ttk_style(root):
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass
    style.configure("Dragon.TCombobox",
                     fieldbackground=PALETTE["tag_fill"],
                     background=PALETTE["card_fill"],
                     foreground="white",
                     arrowcolor="white",
                     bordercolor=PALETTE["panel_border"],
                     selectbackground=PALETTE["tag_fill"],
                     selectforeground="white")
    style.map("Dragon.TCombobox",
              fieldbackground=[("readonly", PALETTE["tag_fill"])],
              foreground=[("readonly", "white")])

    root.option_add("*TCombobox*Listbox.background", PALETTE["tag_fill"])
    root.option_add("*TCombobox*Listbox.foreground", "white")
    root.option_add("*TCombobox*Listbox.selectBackground", PALETTE["card_fill"])
    root.option_add("*TCombobox*Listbox.selectForeground", "white")
    root.option_add("*TCombobox*Listbox.relief", "flat")
    root.option_add("*TCombobox*Listbox.borderWidth", "0")


def bind_mousewheel(canvas):
    """Scroll `canvas` on mouse wheel, but only while the cursor is over it —
    keeps separate scrollable windows from stealing each other's scrolling."""
    def _scroll(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_enter(_event):
        canvas.bind_all("<MouseWheel>", _scroll)

    def _on_leave(_event):
        canvas.unbind_all("<MouseWheel>")

    canvas.bind("<Enter>", _on_enter)
    canvas.bind("<Leave>", _on_leave)


def rounded_button(canvas, x, y, w, h, text, command, r=16,
                    fill=None, outline=None, text_fill="white",
                    font=(APP_FONT_FAMILY, 13, APP_FONT_WEIGHT)):
    fill = fill or PALETTE["card_fill"]
    outline = outline or PALETTE["card_border"]
    rect_id = round_rect(canvas, x, y, x + w, y + h, r=r,
                          fill=fill, outline=outline, width=3)
    text_id = canvas.create_text(x + w / 2, y + h / 2, text=text,
                                  fill=text_fill, font=font)

    def on_click(_event):
        command()

    def on_enter(_event):
        canvas.itemconfig(rect_id, fill=lighten(fill))

    def on_leave(_event):
        canvas.itemconfig(rect_id, fill=fill)

    for item in (rect_id, text_id):
        canvas.tag_bind(item, "<Button-1>", on_click)
        canvas.tag_bind(item, "<Enter>", on_enter)
        canvas.tag_bind(item, "<Leave>", on_leave)
    return rect_id, text_id


def autocrop_to_content(img):
    """Trims transparent padding around the actual artwork. Two icon PNGs
    fit to the same square can still look like different sizes if one has
    more built-in transparent margin than the other — cropping to content
    first makes the visible artwork consistent regardless of source padding.
    No-ops harmlessly on fully-opaque images (portraits, JPEGs, etc.)."""
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    bbox = img.split()[-1].getbbox()
    return img.crop(bbox) if bbox else img


def fit_contain(img, w, h):
    """Scales the image to fit ENTIRELY within (w, h) — no cropping — and
    centers it on a transparent (w, h) canvas. Use this for symbol/glyph
    icons (gender, element, etc.) where a non-square source must never get
    its edges cut off. (For photo-style portraits, ImageOps.fit's crop-to-
    fill is the better look — that's what make_rounded_photo still uses.)"""
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    fitted = img.copy()
    fitted.thumbnail((w, h), Image.LANCZOS)
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    canvas.paste(fitted, ((w - fitted.width) // 2, (h - fitted.height) // 2), fitted)
    return canvas


def make_rounded_photo(path, w, h, radius=16):
    """Loads an image, crops it to fill the target box at the correct aspect
    ratio (no stretching/squishing), and masks it to rounded corners.
    Returns an ImageTk.PhotoImage (caller MUST keep a reference)."""
    img = Image.open(path).convert("RGBA")
    img = autocrop_to_content(img)
    img = ImageOps.fit(img, (w, h), method=Image.LANCZOS, centering=(0.5, 0.5))
    corner_mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(corner_mask).rounded_rectangle([0, 0, w, h], radius=radius, fill=255)
    combined_alpha = ImageChops.multiply(img.split()[-1], corner_mask)
    img.putalpha(combined_alpha)
    return ImageTk.PhotoImage(img)


def draw_pill(canvas, x, y, w, h, text, fill,
              text_fill=None, text_outline=None, font=(APP_FONT_FAMILY, 11, APP_FONT_WEIGHT)):
    """Small rounded capsule used for coat pattern / coat color badges."""
    text_fill = text_fill or PALETTE["pill_text"]
    text_outline = text_outline or PALETTE["pill_outline"]
    round_rect(canvas, x, y, x + w, y + h, r=h / 2,
                fill=fill, outline=fill, width=2)
    cx, cy = x + w / 2, y + h / 2
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        canvas.create_text(cx + dx, cy + dy, text=text, font=font, fill=text_outline)
    canvas.create_text(cx, cy, text=text, font=font, fill=text_fill)


def draw_legendary_pill(canvas, x, y, w, h, element, text="Legendary"):
    """Fills a coat pill with the element's color-shift PNG from
    assets/legendary_shifts/ instead of a flat color. Returns True on
    success; False means no matching file was found and the caller
    should fall back to a normal flat-color draw_pill() instead."""
    try:
        photo = make_rounded_photo(legendary_shift_path(element), int(w), int(h), radius=int(h / 2))
    except Exception:
        return False

    canvas._refs.append(photo)
    canvas.create_image(x + w / 2, y + h / 2, image=photo)
    round_rect(canvas, x, y, x + w, y + h, r=h / 2, fill="", outline="#1C1430", width=2)

    cx, cy = x + w / 2, y + h / 2
    font = (APP_FONT_FAMILY, 11, APP_FONT_WEIGHT)
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        canvas.create_text(cx + dx, cy + dy, text=text, font=font, fill="#000000")
    canvas.create_text(cx, cy, text=text, font=font, fill="#FFFFFF")
    return True


def draw_orb(canvas, cx, cy, r, color):
    """Small glossy sphere icon, used for Element / Pupil rows."""
    canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                        fill=color, outline=lighten(color, -50), width=2)
    canvas.create_oval(cx - r * 0.5, cy - r * 0.65, cx - r * 0.05, cy - r * 0.15,
                        fill=lighten(color, 90), outline="")


def try_icon(canvas, x, y, path, size=24):
    """Try to draw a PNG icon centered at (x, y), cropped to content then
    scaled to fit entirely within a square (no edge-cropping) so every icon
    renders at a consistent size regardless of its source aspect ratio or
    built-in padding. Returns True on success so the caller can fall back
    to something else (emoji, orb, etc.) if the file isn't there."""
    try:
        img = Image.open(path).convert("RGBA")
        img = autocrop_to_content(img)
        img = fit_contain(img, size, size)
        photo = ImageTk.PhotoImage(img)
        canvas._refs.append(photo)
        canvas.create_image(x, y, image=photo)
        return True
    except Exception:
        return False


def draw_triangle(canvas, x, y, size, fill):
    """Small disclosure-arrow icon for section headers."""
    canvas.create_polygon(x, y - size, x, y + size, x + size * 1.3, y,
                           fill=fill, outline="")


def draw_appearance_row_bg(canvas, x, y, w, h):
    return round_rect(canvas, x, y, x + w, y + h, r=12,
                        fill=PALETTE["row_fill"], outline="", width=0)


ROW_ICON_FILES = {
    "Mutations": "mut.png",
    "Age":       "age.png",
}
ROW_ICON_FALLBACK_EMOJI = {
    "Mutations": "\U0001F9EC",
    "Age":       "\u23F3",
}


def draw_row_icon(canvas, x, y, label, icon_value):
    if label == "Cosmetic Trait":
        if not icon_value or icon_value == "None":
            return
        if not try_icon(canvas, x, y, cosmetic_trait_icon_path(icon_value), size=24):
            fallback = os.path.join(MISC_DIR, "costrait.png")
            if not try_icon(canvas, x, y, fallback, size=24):
                canvas.create_text(x, y, text="\U0001FA84", font=(APP_FONT_FAMILY, 17))
    elif label in ROW_ICON_FILES:
        path = os.path.join(MISC_DIR, ROW_ICON_FILES[label])
        if not try_icon(canvas, x, y, path, size=24):
            canvas.create_text(x, y, text=ROW_ICON_FALLBACK_EMOJI[label], font=(APP_FONT_FAMILY, 17))
    else:
        if not try_icon(canvas, x, y, element_icon_path(icon_value), size=24):
            draw_orb(canvas, x, y, 11, get_element_color(icon_value))


def draw_trait_row(canvas, x, y, w, h, trait_entry, accent_color):
    """One row inside the Genetic Traits section: a tier badge + trait name,
    or an 'Empty Slot' placeholder if that slot isn't filled."""
    round_rect(canvas, x, y, x + w, y + h, r=10, fill=PALETTE["row_fill"], outline="", width=0)
    if trait_entry and trait_entry.get("Trait"):
        tier = trait_entry.get("Tier", 1)
        name = trait_entry.get("Trait", "-")
        badge_cx, badge_cy, badge_r = x + 20, y + h / 2, 14
        canvas.create_oval(badge_cx - badge_r, badge_cy - badge_r, badge_cx + badge_r, badge_cy + badge_r,
                            fill=PALETTE["tag_fill"], outline=accent_color, width=3)
        canvas.create_text(badge_cx, badge_cy, text=str(tier), fill="white", font=(APP_FONT_FAMILY, 11, APP_FONT_WEIGHT))
        canvas.create_text(x + 42, y + h / 2, text=name, fill=PALETTE["value_text"],
                            font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT), anchor="w", width=int(w - 50))
    else:
        canvas.create_text(x + w / 2, y + h / 2, text="Empty Slot", fill=PALETTE["label_text"],
                            font=(APP_FONT_FAMILY, 9, "italic"))


genetic_traits_expanded = {}
note_expanded = {}


def show_details(parent, container, name, refresh_grid=None, active_tab=None):
    d = dragons[name]

    for w in container.winfo_children():
        w.destroy()

    W = 640
    is_traits_expanded = genetic_traits_expanded.get(name, False)
    is_note_expanded = note_expanded.get(name, False)
    has_note = bool(d.get("Note", "").strip())
    is_note_expanded = note_expanded.get(name, False)

    extra_optional_rows = sum(1 for v in (d.get("Birthday"), d.get("OriginalOwner"), d.get("Element2")) if v)

    base_H = 728
    traits_extra = 262 if is_traits_expanded else 0

    note_section_h = 44 + 14
    if is_note_expanded:
        if has_note:
            note_text = d.get("Note", "").strip()
            note_lines = max(1, -(-len(note_text) // 55))
            note_section_h += note_lines * 18 + 20
        else:
            note_section_h += 36 + 6

    H = base_H + extra_optional_rows * 46 + traits_extra + note_section_h
    c = tk.Canvas(container, width=W, height=H,
                   bg=PALETTE["lair_bg"], highlightthickness=0)
    c.pack(padx=20, pady=18)
    c._refs = []

    round_rect(c, 4, 4, W - 4, H - 4, r=28,
                fill=PALETTE["info_card_fill"], outline=PALETTE["panel_border"], width=5)

    img_x, img_y, img_w, img_h = 16, 16, 100, 100
    round_rect(c, img_x, img_y, img_x + img_w, img_y + img_h, r=14,
                fill="#2A2143", outline="", width=0)
    try:
        custom_path = custom_dragon_image_path(name)
        icon_path = custom_path if os.path.exists(custom_path) else species_icon_path(d.get("Species", ""))
        photo = make_rounded_photo(icon_path, img_w, img_h, radius=14)
        c._refs.append(photo)
        c.create_image(img_x + img_w / 2, img_y + img_h / 2, image=photo)
    except Exception:
        c.create_text(img_x + img_w / 2, img_y + img_h / 2,
                      text="No Icon\nFound", fill="#9B8FCC",
                      font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT), justify="center")

    right_edge = W - 24

    gender = d.get("Gender", "")
    level = d.get("Level", "-")
    gl_y = img_y + 18
    level_id = c.create_text(right_edge, gl_y, text=f"Lv. {level}", fill=PALETTE["label_text"],
                              font=(APP_FONT_FAMILY, 18, APP_FONT_WEIGHT), anchor="e")
    if gender:
        icon_size = 26
        bbox = c.bbox(level_id)
        icon_cx = (bbox[0] - 8 - icon_size / 2) if bbox else (right_edge - 70)
        try:
            gimg = Image.open(gender_icon_path(gender)).convert("RGBA")
            gimg = autocrop_to_content(gimg)
            gimg = fit_contain(gimg, icon_size, icon_size)
            gphoto = ImageTk.PhotoImage(gimg)
            c._refs.append(gphoto)
            c.create_image(icon_cx, gl_y, image=gphoto)
        except Exception:
            is_male = gender.lower() == "male"
            symbol = "\u2642" if is_male else "\u2640"
            symbol_color = "#5AA9E6" if is_male else "#E667A8"
            c.create_text(icon_cx, gl_y, text=symbol, fill=symbol_color, font=(APP_FONT_FAMILY, 20, APP_FONT_WEIGHT))

    name_max_width = right_edge - (img_x + img_w) - 10
    name_size = fit_text_size(d["Nickname"], APP_FONT_FAMILY, 24, 12, name_max_width)
    shadowed_name_text(c, right_edge, img_y + 50, d["Nickname"],
                       (APP_FONT_FAMILY, name_size, APP_FONT_WEIGHT), anchor="e")
    c.create_text(right_edge, img_y + 80, text=d["Species"],
                  fill=PALETTE["label_text"], font=(APP_FONT_FAMILY, 16, APP_FONT_WEIGHT), anchor="e")
    c.create_text(right_edge, img_y + 104, text=d.get("Rarity", "-"),
                  fill=RARITY_COLORS.get(d.get("Rarity", ""), RARITY_DEFAULT_COLOR),
                  font=(APP_FONT_FAMILY, 16, APP_FONT_WEIGHT), anchor="e")

    if d.get("Soulbound"):
        sb_size = 32
        sb_x = img_x + img_w - sb_size // 2 - 2
        sb_y = img_y + img_h - sb_size // 2 - 2
        sb_path = os.path.join(MISC_DIR, "soulbound.png")
        try:
            sbimg = Image.open(sb_path).convert("RGBA")
            sbimg = autocrop_to_content(sbimg)
            sbimg = fit_contain(sbimg, sb_size, sb_size)
            sbphoto = ImageTk.PhotoImage(sbimg)
            c._refs.append(sbphoto)
            c.create_image(sb_x, sb_y, image=sbphoto)
        except Exception as e:
            print(f"[soulbound] Failed to load {sb_path!r}: {e}")
            c.create_text(sb_x, sb_y, text="\u26d4", fill="#FFD700",
                          font=(APP_FONT_FAMILY, 18, APP_FONT_WEIGHT))

    def handle_edit():
        def after_save():
            if refresh_grid:
                refresh_grid()
            show_details(parent, container, name, refresh_grid, active_tab)

        open_dragon_form(parent, after_save, dragon_id=name)

    def handle_delete():
        if messagebox.askyesno("Delete dragon", f"Delete {d['Nickname']}? This can't be undone."):
            dragons.pop(name, None)
            persist()
            for w in container.winfo_children():
                w.destroy()
            tk.Label(container, text="Select a dragon from the list",
                     fg=PALETTE["label_text"], bg=PALETTE["lair_bg"],
                     font=(APP_FONT_FAMILY, 12, APP_FONT_WEIGHT)).pack(pady=40)
            if refresh_grid:
                refresh_grid()

    def handle_add_to_collection():
        if not current_tabs:
            messagebox.showinfo("No tabs yet",
                                "Create a tab first using '+ New Tab' in the tab bar.")
            return
        dlg = tk.Toplevel(parent)
        dlg.title("Add to Collection")
        dlg.configure(bg=PALETTE["bg_outer"])
        center(dlg, 300, min(60 + len(current_tabs) * 50, 400))
        tk.Label(dlg, text=f'Add "{d["Nickname"]}" to:',
                 fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
                 font=(APP_FONT_FAMILY, 11, APP_FONT_WEIGHT)).pack(pady=(16, 8))
        for tab_id, tab in current_tabs.items():
            already_in = name in tab.get("members", [])
            label = f'✓ {tab["name"]}' if already_in else tab["name"]
            color = PALETTE["bar_fill"] if already_in else PALETTE["card_fill"]
            def make_click(tid=tab_id, ain=already_in):
                def click():
                    if ain:
                        remove_dragon_from_tab(tid, name)
                    else:
                        add_dragon_to_tab(tid, name)
                    if refresh_grid:
                        refresh_grid()
                    dlg.destroy()
                return click
            tk.Button(dlg, text=label, command=make_click(),
                       bg=color, fg="white", relief="flat",
                       font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT),
                       width=24).pack(pady=4)

    def handle_move_to_account():
        other_accounts = [a for a in all_accounts_data.keys() if a != current_account]
        if not other_accounts:
            messagebox.showinfo("No other accounts",
                                "Create another account first from the Account Select screen.")
            return
        dlg = tk.Toplevel(parent)
        dlg.title("Move to Account")
        dlg.configure(bg=PALETTE["bg_outer"])
        center(dlg, 300, min(60 + len(other_accounts) * 46, 420))
        tk.Label(dlg, text=f'Move "{d["Nickname"]}" to:',
                 fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
                 font=(APP_FONT_FAMILY, 11, APP_FONT_WEIGHT)).pack(pady=(16, 8))

        def make_click(dest=None):
            def click():
                if messagebox.askyesno("Confirm move",
                                        f'Move "{d["Nickname"]}" to "{dest}"?\n'
                                        f"It will be removed from this account.",
                                        parent=dlg):
                    move_dragon_to_account(name, dest)
                    dlg.destroy()
                    for w in container.winfo_children():
                        w.destroy()
                    tk.Label(container, text="Select a dragon from the list",
                             fg=PALETTE["label_text"], bg=PALETTE["lair_bg"],
                             font=(APP_FONT_FAMILY, 12, APP_FONT_WEIGHT)).pack(pady=40)
                    if refresh_grid:
                        refresh_grid()
            return click

        for acc in other_accounts:
            tk.Button(dlg, text=acc, command=make_click(acc),
                       bg=PALETTE["card_fill"], fg="white", relief="flat",
                       font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT),
                       width=24).pack(pady=4)

    def handle_note():
        current_note = d.get("Note", "")
        dlg = tk.Toplevel(parent)
        dlg.title(f"Note — {d['Nickname']}")
        dlg.configure(bg=PALETTE["bg_outer"])
        center(dlg, 460, 320)
        tk.Label(dlg, text="Note (max 1000 characters)", fg=PALETTE["label_text"],
                 bg=PALETTE["bg_outer"], font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT)).pack(
            anchor="w", padx=14, pady=(14, 4))
        txt = tk.Text(dlg, width=50, height=10, bg=PALETTE["tag_fill"], fg="white",
                       insertbackground="white", relief="flat", wrap="word",
                       font=(APP_FONT_FAMILY, 10), highlightthickness=1,
                       highlightbackground=PALETTE["panel_border"])
        txt.pack(fill="both", expand=True, padx=14, pady=(0, 4))
        txt.insert("1.0", current_note)
        counter_var = tk.StringVar(value=f"{len(current_note)}/1000")
        tk.Label(dlg, textvariable=counter_var, fg=PALETTE["label_text"],
                 bg=PALETTE["bg_outer"], font=(APP_FONT_FAMILY, 8, APP_FONT_WEIGHT),
                 anchor="e").pack(fill="x", padx=14)

        def on_key(_e=None):
            content = txt.get("1.0", "end-1c")
            if len(content) > 1000:
                txt.delete(f"1.0+{1000}c", "end")
                content = content[:1000]
            counter_var.set(f"{len(content)}/1000")

        txt.bind("<KeyRelease>", on_key)

        def save_note():
            d["Note"] = txt.get("1.0", "end-1c").strip()
            dragons[name] = d
            persist()
            dlg.destroy()

        btn_row = tk.Frame(dlg, bg=PALETTE["bg_outer"])
        btn_row.pack(pady=10)
        tk.Button(btn_row, text="Save Note", command=save_note,
                   bg=PALETTE["bar_fill"], fg="#16330F", relief="flat",
                   font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT), padx=16, pady=6).pack(side="left", padx=6)
        tk.Button(btn_row, text="Cancel", command=dlg.destroy,
                   bg=PALETTE["tag_fill"], fg="white", relief="flat",
                   font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT), padx=16, pady=6).pack(side="left", padx=6)
        txt.focus_set()

    title_stack_bottom = img_y + 104 + 10
    action_y0, action_h = max(img_y + img_h, title_stack_bottom) + 10, 30
    btn_w, btn_gap = 80, 8
    delete_x0 = W - 20 - btn_w
    edit_x0 = delete_x0 - btn_gap - btn_w
    move_x0 = edit_x0 - btn_gap - btn_w
    coll_x0 = move_x0 - btn_gap - 105
    rounded_button(c, coll_x0, action_y0, 105, action_h, "+ Collection",
                    handle_add_to_collection, r=10,
                    fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"])
    rounded_button(c, move_x0, action_y0, btn_w, action_h, "Move",
                    handle_move_to_account, r=10,
                    fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"])
    rounded_button(c, edit_x0, action_y0, btn_w, action_h, "Edit", handle_edit, r=10,
                    fill=PALETTE["card_fill"], outline=PALETTE["card_border"])
    rounded_button(c, delete_x0, action_y0, btn_w, action_h, "Delete", handle_delete, r=10,
                    fill="#7A2020", outline="#4A1010")

    rx, rw = 20, W - 40
    header_y0 = action_y0 + action_h + 14
    header_y1 = header_y0 + 44

    round_rect(c, rx, header_y0, rx + rw, header_y1, r=14,
                fill=PALETTE["header_band"], outline=PALETTE["header_band_border"], width=2)
    outline_text(c, rx + 24, (header_y0 + header_y1) / 2, "Appearance",
                 (APP_FONT_FAMILY, 16, APP_FONT_WEIGHT), "#FFD24C", "#5C3A12", anchor="w")

    row_h, row_gap = 40, 6
    element = d.get("Element", "Ice")
    row_defs = [
        ("coat", "Primary Coat", "P", None),
        ("coat", "Secondary Coat", "S", None),
        ("coat", "Tertiary Coat", "T", None),
        ("icon", "Mutations", None,
         f"{d.get('Mutations', 0)}/{d.get('MaxMutations', 0)}"),
        ("icon", "Age", None, d.get("Age", "-")),
        ("icon", "Cosmetic Trait", d.get("CosmeticTrait", "None"), d.get("CosmeticTrait", "None")),
        ("icon", "Element", element, element),
        ("icon", "Pupil", element, d.get("Pupil", "-")),
        ("plain", "Generation", None, d.get("Generation", "-")),
    ]

    element2 = d.get("Element2")
    if element2:
        row_defs.insert(row_defs.index(("icon", "Pupil", element, d.get("Pupil", "-"))),
                         ("icon", "Element 2", element2, element2))

    if d.get("Birthday"):
        try:
            bdt = date.fromisoformat(d["Birthday"])
            bday_text = f"{MONTH_NAMES[bdt.month - 1]} {bdt.day}, {bdt.year}"
        except Exception:
            bday_text = d["Birthday"]
        row_defs.append(("plain", "Birthday", None, bday_text))

    if d.get("OriginalOwner"):
        row_defs.append(("plain", "Original Owner", None, d["OriginalOwner"]))

    ry = header_y1 + 8
    for kind, label, icon, value in row_defs:
        draw_appearance_row_bg(c, rx, ry, rw, row_h)
        rcy = ry + row_h / 2

        if kind == "coat":
            c.create_text(rx + 20, rcy, text=label, fill=PALETTE["label_text"],
                          font=(APP_FONT_FAMILY, 14, APP_FONT_WEIGHT), anchor="w")
            slot = icon
            color_name = d.get("Colors", {}).get(slot, "-")
            material = d.get("Materials", {}).get(slot, "-")
            color_hex = get_color_hex(color_name, element)
            text_fill = readable_text_color(color_hex)
            text_outline = "#000000" if text_fill == "#FFFFFF" else "#FFFFFF"
            pill_w, pill_h, pill_gap = 110, 28, 8
            p2x = rx + rw - 18 - pill_w
            p1x = p2x - pill_gap - pill_w
            p1y = rcy - pill_h / 2
            if color_name == "Legendary":
                if not draw_legendary_pill(c, p1x, p1y, pill_w, pill_h, element):
                    draw_pill(c, p1x, p1y, pill_w, pill_h, color_name, color_hex,
                              text_fill=text_fill, text_outline=text_outline)
            else:
                draw_pill(c, p1x, p1y, pill_w, pill_h, color_name, color_hex,
                          text_fill=text_fill, text_outline=text_outline)
            draw_pill(c, p2x, rcy - pill_h / 2, pill_w, pill_h, material, "#FFFFFF",
                      text_fill="#2F7FBF", text_outline="#BFE0F5")
        elif kind == "plain":
            c.create_text(rx + 20, rcy, text=label, fill=PALETTE["label_text"],
                          font=(APP_FONT_FAMILY, 14, APP_FONT_WEIGHT), anchor="w")
            outline_text(c, rx + rw - 18, rcy, str(value), (APP_FONT_FAMILY, 15, APP_FONT_WEIGHT),
                         PALETTE["value_text"], PALETTE["value_outline"], anchor="e")
        else:
            draw_row_icon(c, rx + 18, rcy, label, icon)
            c.create_text(rx + 44, rcy, text=label, fill=PALETTE["label_text"],
                          font=(APP_FONT_FAMILY, 14, APP_FONT_WEIGHT), anchor="w")
            outline_text(c, rx + rw - 18, rcy, str(value), (APP_FONT_FAMILY, 15, APP_FONT_WEIGHT),
                         PALETTE["value_text"], PALETTE["value_outline"], anchor="e")

        ry += row_h + row_gap

    note_header_y0 = ry + 14
    note_header_y1 = note_header_y0 + 44

    def toggle_note():
        note_expanded[name] = not note_expanded.get(name, False)
        show_details(parent, container, name, refresh_grid, active_tab)

    note_hdr_id = round_rect(c, rx, note_header_y0, rx + rw, note_header_y1, r=14,
                               fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"], width=2)
    note_arrow_id = c.create_text(rx + 22, (note_header_y0 + note_header_y1) / 2,
                                   text=("\u25BC" if is_note_expanded else "\u25B6"),
                                   fill=PALETTE["label_text"],
                                   font=(APP_FONT_FAMILY, 13, APP_FONT_WEIGHT))
    outline_text(c, rx + 50, (note_header_y0 + note_header_y1) / 2, "Note",
                 (APP_FONT_FAMILY, 16, APP_FONT_WEIGHT),
                 PALETTE["title_fill"], PALETTE["title_outline"], anchor="w")

    note_btn_label = "Edit Note" if has_note else "Add Note"
    note_btn_x = rx + rw - 94
    note_btn_y0 = note_header_y0 + 8
    note_btn_id = round_rect(c, note_btn_x, note_btn_y0, note_btn_x + 84, note_btn_y0 + 28,
                              r=8, fill=PALETTE["card_fill"], outline=PALETTE["panel_border"], width=1)
    note_btn_lbl_id = c.create_text(note_btn_x + 42, note_btn_y0 + 14, text=note_btn_label,
                                     fill="white", font=(APP_FONT_FAMILY, 9, APP_FONT_WEIGHT))

    for item in (note_hdr_id, note_arrow_id):
        c.tag_bind(item, "<Button-1>", lambda _e: toggle_note())
    for item in (note_btn_id, note_btn_lbl_id):
        c.tag_bind(item, "<Button-1>", lambda _e: handle_note())

    if is_note_expanded:
        note_body_y = note_header_y1 + 6
        if has_note:
            note_text = d["Note"].strip()
            note_lines = max(1, -(-len(note_text) // 55))
            note_body_h = note_lines * 18 + 20
            draw_appearance_row_bg(c, rx, note_body_y, rw, note_body_h)
            c.create_text(rx + 16, note_body_y + 10, text=note_text,
                           fill=PALETTE["value_text"],
                           font=(APP_FONT_FAMILY, 10), anchor="nw",
                           width=rw - 32, justify="left")
            ry = note_body_y + note_body_h + 6
        else:
            draw_appearance_row_bg(c, rx, note_body_y, rw, 36)
            c.create_text(rx + 16, note_body_y + 18, text="No note added yet. Click \"Add Note\" to write one.",
                           fill=PALETTE["label_text"], font=(APP_FONT_FAMILY, 9),
                           anchor="w")
            ry = note_body_y + 36 + 6
    else:
        ry = note_header_y1 + 6

    traits_header_y0 = ry + 14
    traits_header_y1 = traits_header_y0 + 44

    def toggle_traits():
        genetic_traits_expanded[name] = not genetic_traits_expanded.get(name, False)
        show_details(parent, container, name, refresh_grid, active_tab)

    traits_header_id = round_rect(c, rx, traits_header_y0, rx + rw, traits_header_y1, r=14,
                                   fill=PALETTE["header_band"], outline=PALETTE["header_band_border"], width=2)
    arrow_id = c.create_text(rx + 22, (traits_header_y0 + traits_header_y1) / 2,
                              text=("\u25BC" if is_traits_expanded else "\u25B6"),
                              fill="#F2A93B", font=(APP_FONT_FAMILY, 13, APP_FONT_WEIGHT))
    outline_text(c, rx + 50, (traits_header_y0 + traits_header_y1) / 2, "Genetic Traits",
                 (APP_FONT_FAMILY, 16, APP_FONT_WEIGHT), "#FFD24C", "#5C3A12", anchor="w")
    for clickable in (traits_header_id, arrow_id):
        c.tag_bind(clickable, "<Button-1>", lambda _e: toggle_traits())

    if is_traits_expanded:
        col_gap = 12
        col_w = (rw - col_gap) / 2
        pos_x0, neg_x0 = rx, rx + col_w + col_gap
        cols_y0 = traits_header_y1 + 10

        c.create_text(pos_x0 + col_w / 2, cols_y0 + 12, text="Positive",
                      fill="#7CFC6E", font=(APP_FONT_FAMILY, 14, APP_FONT_WEIGHT))
        c.create_text(neg_x0 + col_w / 2, cols_y0 + 12, text="Negative",
                      fill="#FF6B6B", font=(APP_FONT_FAMILY, 14, APP_FONT_WEIGHT))

        trait_row_h, trait_row_gap = 40, 6
        trait_rows_y0 = cols_y0 + 28

        positive_traits = d.get("PositiveTraits", [])
        for i in range(MAX_POSITIVE_TRAITS):
            entry = positive_traits[i] if i < len(positive_traits) else None
            row_y = trait_rows_y0 + i * (trait_row_h + trait_row_gap)
            draw_trait_row(c, pos_x0, row_y, col_w, trait_row_h, entry, "#52C724")

        negative_traits = d.get("NegativeTraits", [])
        for i in range(MAX_NEGATIVE_TRAITS):
            entry = negative_traits[i] if i < len(negative_traits) else None
            row_y = trait_rows_y0 + i * (trait_row_h + trait_row_gap)
            draw_trait_row(c, neg_x0, row_y, col_w, trait_row_h, entry, "#FF4D4D")


def make_dragon_card(parent, name, d, on_click):
    w, h = 150, 190
    c = tk.Canvas(parent, width=w, height=h, bg=PALETTE["lair_bg"], highlightthickness=0)
    rect_id = round_rect(c, 5, 5, w - 5, h - 5, r=18,
                          fill=PALETTE["card_fill"], outline=PALETTE["card_border"], width=3)
    c._refs = []

    try:
        custom_path = custom_dragon_image_path(name)
        icon_path = custom_path if os.path.exists(custom_path) else species_icon_path(d.get("Species", ""))
        photo = make_rounded_photo(icon_path, 100, 100, radius=14)
        c._refs.append(photo)
        c.create_image(w / 2, 70, image=photo)
    except Exception:
        round_rect(c, w / 2 - 45, 25, w / 2 + 45, 115, r=12,
                    fill=RARITY_COLORS.get(d["Rarity"], "#888888"))
        c.create_text(w / 2, 70, text=name, fill="white",
                      font=(APP_FONT_FAMILY, 9, APP_FONT_WEIGHT), width=80, justify="center")

    if d.get("Note", "").strip():
        c.create_oval(w - 22, 10, w - 10, 22, fill=PALETTE["badge_fill"],
                       outline=PALETTE["badge_border"], width=1)
        c.create_text(w - 16, 16, text="\u270f", fill="#3A2A06",
                       font=(APP_FONT_FAMILY, 7, APP_FONT_WEIGHT))

    card_name_size = fit_text_size(d["Nickname"], APP_FONT_FAMILY, 12, 7, w - 16)
    shadowed_name_text(c, w / 2, 142, d["Nickname"], (APP_FONT_FAMILY, card_name_size, APP_FONT_WEIGHT))
    c.create_text(w / 2, 162, text=d.get("Species", "-"),
                  fill=PALETTE["label_text"], font=(APP_FONT_FAMILY, 9, APP_FONT_WEIGHT))

    def handler(_event):
        on_click(name)

    def on_enter(_event):
        c.itemconfig(rect_id, fill=lighten(PALETTE["card_fill"]))

    def on_leave(_event):
        c.itemconfig(rect_id, fill=PALETTE["card_fill"])

    c.bind("<Button-1>", handler)
    c.bind("<Enter>", on_enter)
    c.bind("<Leave>", on_leave)
    return c


def open_sda_tracker(parent_win):
    owned_species = set()
    best_mutations = {}
    for d in dragons.values():
        sp = d.get("Species", "")
        if sp:
            owned_species.add(sp)
            mut = int(d.get("Mutations", 0))
            best_mutations[sp] = max(best_mutations.get(sp, 0), mut)

    def badge_color(sp):
        mut = best_mutations.get(sp, 0)
        if mut >= 5:
            return "#52C724"
        if mut >= 1:
            return "#FFB300"
        return "#8B1A1A"

    total = sum(1 for s in SPECIES_LIST if s not in SDA_EXCLUDED)
    owned_count = sum(1 for s in SPECIES_LIST if s in owned_species)
    sda_count = sum(1 for s in SPECIES_LIST
                    if best_mutations.get(s, 0) >= 5 and s not in SDA_EXCLUDED)

    owned_color = "#52C724"
    sda_header_color = "#FFB300"

    win = tk.Toplevel(parent_win)
    win.title("Supreme Dragon Adventurer Tracker")
    win.configure(bg=PALETTE["bg_outer"])
    center(win, 980, 760)
    win.minsize(600, 400)

    header_frame = tk.Frame(win, bg=PALETTE["panel_fill"])
    header_frame.pack(fill="x")

    header_canvas = tk.Canvas(header_frame, bg=PALETTE["panel_fill"], highlightthickness=0, height=100)
    header_canvas.pack(fill="x")

    def redraw_header(event=None):
        w = header_canvas.winfo_width() or 980
        header_canvas.delete("all")
        outline_text(header_canvas, w // 2, 26, "Supreme Dragon Adventurer Tracker",
                     (APP_FONT_FAMILY, 18, APP_FONT_WEIGHT), PALETTE["title_fill"], PALETTE["title_outline"])
        header_canvas.create_text(w // 4, 66,
                                   text=f"Owned:  {owned_count} / {total}",
                                   fill=owned_color, font=(APP_FONT_FAMILY, 14, APP_FONT_WEIGHT))
        header_canvas.create_text(w * 3 // 4, 66,
                                   text=f"SDA-Ready (5/5):  {sda_count} / {total}",
                                   fill=sda_header_color, font=(APP_FONT_FAMILY, 14, APP_FONT_WEIGHT))

    header_canvas.bind("<Configure>", lambda e: redraw_header())

    body_outer = tk.Frame(win, bg=PALETTE["bg_outer"])
    body_outer.pack(fill="both", expand=True)

    scroll_canvas = tk.Canvas(body_outer, bg=PALETTE["bg_outer"], highlightthickness=0)
    scroll_canvas.pack(side="left", fill="both", expand=True)
    vscroll = tk.Scrollbar(body_outer, command=scroll_canvas.yview)
    vscroll.pack(side="right", fill="y")
    scroll_canvas.configure(yscrollcommand=vscroll.set)
    bind_mousewheel(scroll_canvas)

    grid_frame = tk.Frame(scroll_canvas, bg=PALETTE["bg_outer"])
    win_id = scroll_canvas.create_window((0, 0), window=grid_frame, anchor="nw")

    icon_cache = {}

    def build_grid(available_width):
        for w in grid_frame.winfo_children():
            w.destroy()

        PAD = 8
        MIN_CELL_W = 200
        cols = max(2, available_width // (MIN_CELL_W + PAD))
        cell_w = (available_width - PAD * (cols + 1)) // cols
        icon_s = max(44, min(80, cell_w // 3))
        cell_h = icon_s + 24
        name_font_size = max(9, min(13, cell_w // 18))
        badge_font_size = max(7, name_font_size - 2)

        for idx, species in enumerate(SPECIES_LIST):
            row_i = idx // cols
            col_i = idx % cols

            is_owned = species in owned_species
            is_excluded = species in SDA_EXCLUDED
            sp_mut = best_mutations.get(species, 0) if not is_excluded else None

            icon_species = "Riyu" if species == "Mountain Dragon" else species

            cell = tk.Canvas(grid_frame, width=cell_w, height=cell_h,
                              bg=PALETTE["panel_fill"], highlightthickness=0)
            cell.grid(row=row_i, column=col_i, padx=PAD // 2, pady=PAD // 2)
            round_rect(cell, 2, 2, cell_w - 2, cell_h - 2, r=10,
                        fill=PALETTE["row_fill"], outline=PALETTE["panel_border"], width=1)

            icon_cx = icon_s // 2 + 8
            icon_cy = cell_h // 2

            cache_key = (icon_species, icon_s)
            if cache_key not in icon_cache:
                try:
                    icon_cache[cache_key] = make_rounded_photo(
                        species_icon_path(icon_species), icon_s, icon_s, radius=8)
                except Exception:
                    icon_cache[cache_key] = None

            photo = icon_cache[cache_key]
            if photo:
                cell._ref = photo
                cell.create_image(icon_cx, icon_cy, image=photo)
            else:
                cell.create_rectangle(8, (cell_h - icon_s) // 2, 8 + icon_s,
                                       (cell_h + icon_s) // 2,
                                       fill=PALETTE["tag_fill"], outline="")

            text_x = icon_s + 16
            text_w = cell_w - text_x - 8
            name_color = "#3EBF2F" if is_owned else "#8B1A1A"

            show_badge = sp_mut is not None
            fitted_size = fit_text_size(species, APP_FONT_FAMILY,
                                        name_font_size + 3, 8, text_w)
            text_y = icon_cy - (10 if show_badge else 0)
            cell.create_text(text_x + text_w // 2, text_y, text=species, fill=name_color,
                              font=(APP_FONT_FAMILY, fitted_size, APP_FONT_WEIGHT),
                              width=text_w, justify="center", anchor="center")

            if show_badge:
                bc = badge_color(species)
                bw, bh = 38, 17
                bx = text_x + (text_w - bw) // 2
                by = icon_cy + 10
                round_rect(cell, bx, by, bx + bw, by + bh, r=5,
                            fill=PALETTE["tag_fill"], outline=bc, width=1)
                cell.create_text(bx + bw // 2, by + bh // 2,
                                  text=f"{sp_mut}/5",
                                  fill=bc, font=(APP_FONT_FAMILY, badge_font_size, APP_FONT_WEIGHT))

        grid_frame.update_idletasks()
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

    last_width = {"w": 0}

    def on_canvas_resize(event):
        w = event.width
        scroll_canvas.itemconfig(win_id, width=w)
        if abs(w - last_width["w"]) > 4:
            last_width["w"] = w
            build_grid(w)

    scroll_canvas.bind("<Configure>", on_canvas_resize)

    win.update_idletasks()
    build_grid(scroll_canvas.winfo_width() or 960)


def open_lair(root, account):
    switch_account(account)
    root.withdraw()

    win = tk.Toplevel()
    win.title(f"The Lair — {account}")
    win.configure(bg=PALETTE["lair_bg"])
    center(win, 1100, 850)

    def back_to_accounts():
        win.destroy()
        root.deiconify()

    win.protocol("WM_DELETE_WINDOW", back_to_accounts)

    active_tab = {"id": None}

    left = tk.Frame(win, bg=PALETTE["lair_bg"], width=380)
    left.pack(side="left", fill="y")
    left.pack_propagate(False)

    tk.Label(left, text=f"Logged in as {account}", fg=PALETTE["label_text"],
             bg=PALETTE["lair_bg"], font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT)).pack(pady=(12, 2))

    back_canvas = tk.Canvas(left, width=352, height=34, bg=PALETTE["lair_bg"], highlightthickness=0)
    back_canvas.pack(padx=14, pady=(2, 0))
    rounded_button(back_canvas, 2, 2, 350, 32, "\u2190 Switch Account", back_to_accounts, r=12,
                    fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"])

    tab_area = tk.Frame(left, bg=PALETTE["lair_bg"])
    tab_area.pack(fill="x", padx=14, pady=(10, 0))

    tab_scroll_canvas = tk.Canvas(tab_area, bg=PALETTE["lair_bg"], highlightthickness=0, height=36)
    tab_scroll_canvas.pack(side="top", fill="x")
    tab_inner = tk.Frame(tab_scroll_canvas, bg=PALETTE["lair_bg"])
    tab_scroll_canvas.create_window((0, 0), window=tab_inner, anchor="nw")

    search_var = tk.StringVar()
    search_box = tk.Frame(left, bg=PALETTE["lair_bg"])
    search_box.pack(fill="x", padx=14, pady=(8, 6))
    search_canvas = tk.Canvas(search_box, height=40, bg=PALETTE["lair_bg"], highlightthickness=0)
    search_canvas.pack(fill="x")
    round_rect(search_canvas, 2, 2, 352, 38, r=14,
                fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"], width=2)
    search = tk.Entry(search_canvas, textvariable=search_var,
                       bg=PALETTE["tag_fill"], fg="white",
                       insertbackground="white", relief="flat",
                       font=(APP_FONT_FAMILY, 11))
    search_canvas.create_window(177, 20, window=search, width=320)

    sort_wrap = tk.Frame(left, bg=PALETTE["lair_bg"])
    sort_wrap.pack(fill="x", padx=14, pady=(0, 10))
    tk.Label(sort_wrap, text="Sort by", fg=PALETTE["label_text"], bg=PALETTE["lair_bg"],
             font=(APP_FONT_FAMILY, 9, APP_FONT_WEIGHT)).pack(anchor="w")
    sort_var = tk.StringVar(value="Nickname")
    sort_combo = ttk.Combobox(sort_wrap, textvariable=sort_var,
                               values=["Nickname", "Species", "Level", "Gender"],
                               state="readonly", style="Dragon.TCombobox", font=(APP_FONT_FAMILY, 10))
    sort_combo.pack(fill="x")

    add_canvas = tk.Canvas(left, width=352, height=44, bg=PALETTE["lair_bg"], highlightthickness=0)
    add_canvas.pack(padx=14, pady=(0, 10))

    add_dragon_window = {"win": None}

    def open_add_dragon():
        existing = add_dragon_window["win"]
        if existing is not None and existing.winfo_exists():
            existing.lift()
            existing.focus_force()
            return
        add_dragon_window["win"] = open_dragon_form(win, render)

    rounded_button(add_canvas, 2, 2, 350, 42, "+ Add Dragon",
                    open_add_dragon, r=14,
                    fill=PALETTE["badge_fill"], outline=PALETTE["badge_border"],
                    text_fill="#3A2A06")

    sub_on = account_settings.get("Subscription", False)
    sub_state = {"on": sub_on}
    sub_canvas = tk.Canvas(left, width=352, height=36, bg=PALETTE["lair_bg"], highlightthickness=0)
    sub_canvas.pack(padx=14, pady=(0, 4))

    def draw_sub_btn():
        sub_canvas.delete("all")
        on = sub_state["on"]
        lbl = "\u2714 Subscription (ON)" if on else "Subscription (OFF)"
        fill = PALETTE["bar_fill"] if on else PALETTE["tag_fill"]
        tf = "#16330F" if on else "white"
        rounded_button(sub_canvas, 2, 2, 350, 34, lbl,
                        toggle_sub, r=12, fill=fill, outline=PALETTE["panel_border"], text_fill=tf)

    def toggle_sub():
        sub_state["on"] = not sub_state["on"]
        account_settings["Subscription"] = sub_state["on"]
        save_account_settings(current_account, account_settings)
        draw_sub_btn()

    draw_sub_btn()

    sda_canvas = tk.Canvas(left, width=352, height=36, bg=PALETTE["lair_bg"], highlightthickness=0)
    sda_canvas.pack(padx=14, pady=(0, 4))
    rounded_button(sda_canvas, 2, 2, 350, 34, "\u2605 SDA Tracker",
                    lambda: open_sda_tracker(win), r=12,
                    fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"])

    select_mode = {"on": False}
    selected_ids = set()

    sel_canvas = tk.Canvas(left, width=352, height=36, bg=PALETTE["lair_bg"], highlightthickness=0)
    sel_canvas.pack(padx=14, pady=(0, 4))
    sel_btn_ids = rounded_button(sel_canvas, 2, 2, 350, 34, "\u2610  Select Mode",
                                  lambda: toggle_select_mode(), r=12,
                                  fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"])

    del_canvas = tk.Canvas(left, width=352, height=36, bg=PALETTE["lair_bg"], highlightthickness=0)
    move_canvas = tk.Canvas(left, width=352, height=36, bg=PALETTE["lair_bg"], highlightthickness=0)

    def refresh_del_button():
        del_canvas.delete("all")
        n = len(selected_ids)
        rounded_button(del_canvas, 2, 2, 350, 34,
                        f"Delete Selected ({n})",
                        lambda: batch_delete(), r=12,
                        fill="#7A2020" if n else PALETTE["row_fill"],
                        outline="#4A1010" if n else PALETTE["panel_border"])

        move_canvas.delete("all")
        rounded_button(move_canvas, 2, 2, 350, 34,
                        f"Move Selected ({n})",
                        lambda: batch_move(), r=12,
                        fill=PALETTE["tag_fill"] if n else PALETTE["row_fill"],
                        outline=PALETTE["panel_border"])

    def toggle_select_mode():
        select_mode["on"] = not select_mode["on"]
        selected_ids.clear()
        if select_mode["on"]:
            sel_canvas.itemconfig(sel_btn_ids[0], fill=PALETTE["badge_fill"])
            sel_canvas.itemconfig(sel_btn_ids[1], fill="#3A2A06")
            sel_canvas.delete("all")
            rounded_button(sel_canvas, 2, 2, 350, 34, "\u2611  Select Mode  (on)",
                            lambda: toggle_select_mode(), r=12,
                            fill=PALETTE["badge_fill"], outline=PALETTE["badge_border"],
                            text_fill="#3A2A06")
            move_canvas.pack(padx=14, pady=(0, 4))
            del_canvas.pack(padx=14, pady=(0, 4))
            refresh_del_button()
        else:
            sel_canvas.delete("all")
            rounded_button(sel_canvas, 2, 2, 350, 34, "\u2610  Select Mode",
                            lambda: toggle_select_mode(), r=12,
                            fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"])
            del_canvas.pack_forget()
            move_canvas.pack_forget()
        render(search_var.get())

    def batch_delete():
        if not selected_ids:
            return
        n = len(selected_ids)
        names = ", ".join(dragons[i]["Nickname"] for i in selected_ids if i in dragons)
        if not messagebox.askyesno("Delete dragons",
                                    f"Permanently delete {n} dragon(s)?\n{names}"):
            return
        for did in list(selected_ids):
            dragons.pop(did, None)
            for tab in current_tabs.values():
                if did in tab.get("members", []):
                    tab["members"].remove(did)
        selected_ids.clear()
        persist()
        for w in right.winfo_children():
            w.destroy()
        toggle_select_mode()

    def batch_move():
        if not selected_ids:
            return
        other_accounts = [a for a in all_accounts_data.keys() if a != current_account]
        if not other_accounts:
            messagebox.showinfo("No other accounts",
                                "Create another account first from the Account Select screen.")
            return
        dlg = tk.Toplevel(win)
        dlg.title("Move Selected To")
        dlg.configure(bg=PALETTE["bg_outer"])
        center(dlg, 300, min(60 + len(other_accounts) * 46, 420))
        n = len(selected_ids)
        tk.Label(dlg, text=f"Move {n} selected dragon(s) to:",
                 fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
                 font=(APP_FONT_FAMILY, 11, APP_FONT_WEIGHT)).pack(pady=(16, 8))

        def make_click(dest=None):
            def click():
                if not messagebox.askyesno("Confirm move",
                                            f'Move {n} dragon(s) to "{dest}"?',
                                            parent=dlg):
                    return
                for did in list(selected_ids):
                    move_dragon_to_account(did, dest)
                dlg.destroy()
                for w in right.winfo_children():
                    w.destroy()
                toggle_select_mode()
            return click

        for acc in other_accounts:
            tk.Button(dlg, text=acc, command=make_click(acc),
                       bg=PALETTE["card_fill"], fg="white", relief="flat",
                       font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT),
                       width=24).pack(pady=4)

    MAX_GRID_HEIGHT = 560

    canvas_holder = tk.Frame(left, bg=PALETTE["lair_bg"])
    canvas_holder.pack(fill="x")

    grid_canvas = tk.Canvas(canvas_holder, bg=PALETTE["lair_bg"], highlightthickness=0, height=1)
    grid_canvas.pack(side="left", fill="x", expand=True)

    scrollbar = tk.Scrollbar(canvas_holder, command=grid_canvas.yview)
    scrollbar.pack(side="right", fill="y")
    grid_canvas.configure(yscrollcommand=scrollbar.set)

    list_frame = tk.Frame(grid_canvas, bg=PALETTE["lair_bg"])
    list_window_id = grid_canvas.create_window((0, 0), window=list_frame, anchor="nw")
    grid_canvas.bind("<Configure>", lambda e: grid_canvas.itemconfig(list_window_id, width=e.width))

    right_outer = tk.Frame(win, bg=PALETTE["lair_bg"])
    right_outer.pack(side="right", fill="both", expand=True)

    right_canvas = tk.Canvas(right_outer, bg=PALETTE["lair_bg"], highlightthickness=0)
    right_canvas.pack(side="left", fill="both", expand=True)
    right_scroll = tk.Scrollbar(right_outer, command=right_canvas.yview)
    right_scroll.pack(side="right", fill="y")
    right_canvas.configure(yscrollcommand=right_scroll.set)
    bind_mousewheel(right_canvas)

    right = tk.Frame(right_canvas, bg=PALETTE["lair_bg"])
    right_window_id = right_canvas.create_window((0, 0), window=right, anchor="nw")
    right_canvas.bind("<Configure>", lambda e: right_canvas.itemconfig(right_window_id, width=e.width))
    right.bind("<Configure>", lambda e: right_canvas.configure(scrollregion=right_canvas.bbox("all")))

    def rebuild_tab_bar():
        for w in tab_inner.winfo_children():
            w.destroy()

        def make_tab_btn(tab_id, label, is_all=False):
            is_active = active_tab["id"] == tab_id
            fill = PALETTE["badge_fill"] if is_active else PALETTE["tag_fill"]
            text_color = "#3A2A06" if is_active else "white"
            btn_w = max(80, len(label) * 9 + 20)
            c = tk.Canvas(tab_inner, width=btn_w, height=30, bg=PALETTE["lair_bg"], highlightthickness=0)
            c.pack(side="left", padx=(0, 4))
            round_rect(c, 1, 1, btn_w - 1, 29, r=10, fill=fill, outline=PALETTE["panel_border"], width=2)
            c.create_text(btn_w // 2 - (0 if is_all else 6), 15, text=label,
                          fill=text_color, font=(APP_FONT_FAMILY, 9, APP_FONT_WEIGHT))
            c.bind("<Button-1>", lambda _e: select_tab(tab_id))

            if not is_all:
                del_x = btn_w - 10
                del_id = c.create_text(del_x, 15, text="✕", fill="#FF8888",
                                        font=(APP_FONT_FAMILY, 8, APP_FONT_WEIGHT))
                c.tag_bind(del_id, "<Button-1>", lambda _e, t=tab_id: confirm_delete_tab(t))

                edit_x = btn_w - 22
                edit_id = c.create_text(edit_x, 15, text="✎", fill="#CCC",
                                         font=(APP_FONT_FAMILY, 8, APP_FONT_WEIGHT))
                c.tag_bind(edit_id, "<Button-1>", lambda _e, t=tab_id, n=label: open_rename_tab(t, n))

        make_tab_btn(None, "All Dragons", is_all=True)
        for tab_id, tab in current_tabs.items():
            make_tab_btn(tab_id, tab["name"])

        new_c = tk.Canvas(tab_inner, width=80, height=30, bg=PALETTE["lair_bg"], highlightthickness=0)
        new_c.pack(side="left", padx=(0, 4))
        round_rect(new_c, 1, 1, 79, 29, r=10, fill=PALETTE["card_fill"],
                    outline=PALETTE["panel_border"], width=2)
        new_c.create_text(40, 15, text="+ New Tab", fill=PALETTE["label_text"],
                           font=(APP_FONT_FAMILY, 8, APP_FONT_WEIGHT))
        new_c.bind("<Button-1>", lambda _e: open_new_tab_dialog())

        tab_inner.update_idletasks()
        tab_scroll_canvas.configure(scrollregion=tab_scroll_canvas.bbox("all"))

    def select_tab(tab_id):
        active_tab["id"] = tab_id
        rebuild_tab_bar()
        render(search_var.get())

    def confirm_delete_tab(tab_id):
        name = current_tabs.get(tab_id, {}).get("name", "this tab")
        if messagebox.askyesno("Delete tab", f'Delete "{name}"? Dragons won\'t be removed.'):
            if active_tab["id"] == tab_id:
                active_tab["id"] = None
            delete_tab(tab_id)
            rebuild_tab_bar()
            render(search_var.get())

    def open_rename_tab(tab_id, current_name):
        dlg = tk.Toplevel(win)
        dlg.title("Rename Tab")
        dlg.configure(bg=PALETTE["bg_outer"])
        center(dlg, 320, 160)
        tk.Label(dlg, text="New name:", fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
                 font=(APP_FONT_FAMILY, 11, APP_FONT_WEIGHT)).pack(pady=(18, 4))
        var = tk.StringVar(value=current_name)
        e = tk.Entry(dlg, textvariable=var, bg=PALETTE["tag_fill"], fg="white",
                      insertbackground="white", relief="flat", font=(APP_FONT_FAMILY, 11))
        e.pack(fill="x", padx=20)
        def save():
            n = var.get().strip()
            if n:
                rename_tab(tab_id, n)
                rebuild_tab_bar()
                dlg.destroy()
        tk.Button(dlg, text="Save", command=save, bg=PALETTE["bar_fill"], fg="#16330F",
                   relief="flat", font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT)).pack(pady=14)
        e.bind("<Return>", lambda _e: save())
        e.focus_set()

    def open_new_tab_dialog():
        dlg = tk.Toplevel(win)
        dlg.title("New Tab")
        dlg.configure(bg=PALETTE["bg_outer"])
        center(dlg, 320, 160)
        tk.Label(dlg, text="Tab name:", fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
                 font=(APP_FONT_FAMILY, 11, APP_FONT_WEIGHT)).pack(pady=(18, 4))
        var = tk.StringVar()
        e = tk.Entry(dlg, textvariable=var, bg=PALETTE["tag_fill"], fg="white",
                      insertbackground="white", relief="flat", font=(APP_FONT_FAMILY, 11))
        e.pack(fill="x", padx=20)
        def create():
            n = var.get().strip()
            if n:
                new_id = create_tab(n)
                rebuild_tab_bar()
                select_tab(new_id)
                dlg.destroy()
        tk.Button(dlg, text="Create", command=create, bg=PALETTE["bar_fill"], fg="#16330F",
                   relief="flat", font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT)).pack(pady=14)
        e.bind("<Return>", lambda _e: create())
        e.focus_set()

    def matches(d, ft):
        if not ft:
            return True
        haystack = [d.get("Nickname", ""), d.get("Species", ""),
                    d.get("CosmeticTrait", ""), d.get("Element", "")]
        haystack.extend(d.get("Colors", {}).values())
        return any(ft in str(h).lower() for h in haystack)

    def sort_key(item):
        _id, dd = item
        mode = sort_var.get()
        if mode == "Level":
            try:
                return (0, float(dd.get("Level", 0)))
            except (TypeError, ValueError):
                return (1, str(dd.get("Level", "")).lower())
        if mode == "Species":
            return (0, dd.get("Species", "").lower())
        if mode == "Gender":
            return (0, dd.get("Gender", "").lower())
        return (0, dd.get("Nickname", "").lower())

    def render(filter_text=""):
        for w in list_frame.winfo_children():
            w.destroy()

        tab_id = active_tab["id"]
        tab_members = set(current_tabs[tab_id]["members"]) if tab_id else None

        ft = filter_text.lower()
        all_items = [(i, d) for i, d in dragons.items() if matches(d, ft)]
        if tab_members is not None:
            all_items = [(i, d) for i, d in all_items if i in tab_members]
        all_items.sort(key=sort_key)

        row = col = 0
        for dragon_id, d in all_items:
            if select_mode["on"]:
                card = make_dragon_card(list_frame, dragon_id, d, lambda _n: None)
                card.grid(row=row, column=col, padx=8, pady=8)
                is_sel = dragon_id in selected_ids
                card.delete("sel_overlay")
                box_c = PALETTE["badge_fill"] if is_sel else PALETTE["tag_fill"]
                box_outline = PALETTE["badge_border"] if is_sel else PALETTE["panel_border"]
                bx, by, bsz = 6, 6, 18
                round_rect(card, bx, by, bx + bsz, by + bsz, r=4,
                            fill=box_c, outline=box_outline, width=2)
                if is_sel:
                    card.create_text(bx + bsz // 2, by + bsz // 2, text="\u2714",
                                      fill="white", font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT))

                def make_toggle(did=dragon_id, c=card):
                    def toggle(_event=None):
                        if did in selected_ids:
                            selected_ids.discard(did)
                        else:
                            selected_ids.add(did)
                        refresh_del_button()
                        render(search_var.get())
                    return toggle

                card.bind("<Button-1>", make_toggle())
            else:
                card = make_dragon_card(list_frame, dragon_id, d,
                                         lambda n=dragon_id: show_details(win, right, n, render, active_tab))
                card.grid(row=row, column=col, padx=8, pady=8)

                if tab_id is not None:
                    rem = tk.Label(card, text="✕", fg="#FF8888", bg=PALETTE["lair_bg"],
                                    font=(APP_FONT_FAMILY, 8, APP_FONT_WEIGHT), cursor="hand2")
                    rem.place(x=card.winfo_reqwidth() - 14, y=2)
                    rem.bind("<Button-1>", lambda _e, did=dragon_id, tid=tab_id: (
                        remove_dragon_from_tab(tid, did), render(search_var.get())))

            col += 1
            if col > 1:
                col = 0
                row += 1

        if not all_items:
            tab_name = current_tabs.get(tab_id, {}).get("name", "") if tab_id else ""
            if ft:
                msg = "No dragons match your search"
            elif tab_id:
                msg = f'No dragons in "{tab_name}" yet\nOpen a dragon\'s card and tap + to add'
            else:
                msg = "No dragons yet —\ntap + Add Dragon to add one"
            tk.Label(list_frame, text=msg, fg=PALETTE["label_text"], bg=PALETTE["lair_bg"],
                     font=(APP_FONT_FAMILY, 11, APP_FONT_WEIGHT), justify="center",
                     wraplength=320).pack(pady=50)

        list_frame.update_idletasks()
        content_h = max(1, list_frame.winfo_reqheight())
        grid_canvas.configure(height=min(content_h, MAX_GRID_HEIGHT))
        grid_canvas.configure(scrollregion=grid_canvas.bbox("all"))

    search_var.trace_add("write", lambda *_: render(search_var.get()))
    sort_var.trace_add("write", lambda *_: render(search_var.get()))
    rebuild_tab_bar()
    render()

    bind_mousewheel(grid_canvas)


def element_icon_path(element):
    return os.path.join(ICON_DIR, f"{element.lower().replace(' ', '_')}.png")


def legendary_shift_path(element):
    return os.path.join(LEGENDARY_SHIFT_DIR, f"{element.lower().replace(' ', '_')}.png")


def gender_icon_path(gender):
    return os.path.join(MISC_DIR, f"{gender.lower()}.png")


def custom_dragon_image_path(dragon_id):
    return os.path.join(DRAGON_IMAGES_DIR, f"{dragon_id}.png")


def import_dragon_custom_image(source_path, dragon_id):
    """Copies and resizes a user-chosen image into assets/dragon_images/
    at a consistent 200x200 max, preserving transparency. Returns the
    destination path, or None on failure."""
    try:
        img = Image.open(source_path).convert("RGBA")
        img = autocrop_to_content(img)
        img.thumbnail((200, 200), Image.LANCZOS)
        dest = custom_dragon_image_path(dragon_id)
        img.save(dest, "PNG", optimize=True)
        return dest
    except Exception as e:
        print(f"[custom icon] Failed to import {source_path}: {e}")
        return None


def cosmetic_trait_icon_path(trait):
    base = trait.lower().replace(" ", "_")
    base_nospace = trait.lower().replace(" ", "")
    candidates = [
        f"{base}_icon.png",
        f"{base}.png",
        f"{base_nospace}_icon.png",
        f"{base_nospace}.png",
    ]
    try:
        existing = {f.lower(): f for f in os.listdir(COSMETIC_TRAIT_ICON_DIR)}
    except Exception:
        existing = {}
    for candidate in candidates:
        match = existing.get(candidate.lower())
        if match:
            return os.path.join(COSMETIC_TRAIT_ICON_DIR, match)
    return os.path.join(COSMETIC_TRAIT_ICON_DIR, candidates[0])


def make_element_picker(parent, initial=None):
    """Searchable, scrollable grid of click-to-select element icons. Looks for
    a matching PNG in assets/icons/ (e.g. assets/icons/ice.png) and falls back
    to a colored orb if no icon file has been dropped in yet."""
    wrap_outer = tk.Frame(parent, bg=PALETTE["bg_outer"])
    selected = {"value": initial or (ELEMENT_LIST[0] if ELEMENT_LIST else None)}
    cells = {}

    search_holder, filter_var = styled_entry(wrap_outer, width=400, height=30)
    search_holder.pack(pady=(0, 6))

    grid_holder = tk.Frame(wrap_outer, bg=PALETTE["bg_outer"])
    grid_holder.pack()

    GRID_W, GRID_H, COLS = 360, 220, 4
    CELL_W, CELL_H = 80, 78

    grid_canvas = tk.Canvas(grid_holder, width=GRID_W, height=GRID_H, bg=PALETTE["bg_outer"], highlightthickness=0)
    grid_canvas.pack(side="left")
    grid_scroll = tk.Scrollbar(grid_holder, command=grid_canvas.yview)
    grid_scroll.pack(side="left", fill="y")
    grid_canvas.configure(yscrollcommand=grid_scroll.set)
    bind_mousewheel(grid_canvas)

    inner = tk.Frame(grid_canvas, bg=PALETTE["bg_outer"])
    grid_canvas.create_window((0, 0), window=inner, anchor="nw")

    selected_label = tk.Label(wrap_outer, text=f"Selected: {selected['value']}",
                               fg=PALETTE["title_fill"], bg=PALETTE["bg_outer"],
                               font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT))
    selected_label.pack(pady=(6, 0))

    def refresh_highlight():
        for el, (_cell, border_id) in cells.items():
            is_sel = (el == selected["value"])
            _cell.itemconfig(border_id, outline=PALETTE["title_fill"] if is_sel else PALETTE["bg_outer"])

    def render_grid(filter_text=""):
        for w in inner.winfo_children():
            w.destroy()
        cells.clear()

        ft = filter_text.lower()
        col = row = 0
        for el in ELEMENT_LIST:
            if ft and ft not in el.lower():
                continue

            cell = tk.Canvas(inner, width=CELL_W, height=CELL_H,
                              bg=PALETTE["bg_outer"], highlightthickness=0)
            cell.grid(row=row, column=col, padx=2, pady=2)
            cell._refs = []

            border_id = round_rect(cell, 1, 1, CELL_W - 1, CELL_H - 1, r=10,
                                    fill="", outline=PALETTE["bg_outer"], width=3)

            try:
                img = Image.open(element_icon_path(el)).convert("RGBA")
                img = autocrop_to_content(img)
                img = fit_contain(img, 40, 40)
                photo = ImageTk.PhotoImage(img)
                cell._refs.append(photo)
                cell.create_image(CELL_W / 2, 26, image=photo)
            except Exception:
                draw_orb(cell, CELL_W / 2, 26, 16, get_element_color(el))

            cell.create_text(CELL_W / 2, 58, text=el, fill=PALETTE["label_text"],
                              font=(APP_FONT_FAMILY, 7, APP_FONT_WEIGHT), width=CELL_W - 6, justify="center")

            def select(_event=None, el=el):
                selected["value"] = el
                selected_label.config(text=f"Selected: {el}")
                refresh_highlight()

            cell.bind("<Button-1>", select)
            cells[el] = (cell, border_id)

            col += 1
            if col >= COLS:
                col = 0
                row += 1

        inner.update_idletasks()
        grid_canvas.configure(scrollregion=grid_canvas.bbox("all"))
        refresh_highlight()

    filter_var.trace_add("write", lambda *_: render_grid(filter_var.get()))
    render_grid()

    return wrap_outer, selected


def styled_entry(parent, width=420, height=34, default=""):
    holder = tk.Canvas(parent, width=width, height=height, bg=PALETTE["bg_outer"], highlightthickness=0)
    round_rect(holder, 2, 2, width - 2, height - 2, r=12,
                fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"], width=2)
    var = tk.StringVar(value=default)
    entry = tk.Entry(holder, textvariable=var, bg=PALETTE["tag_fill"], fg="white",
                      insertbackground="white", relief="flat", font=(APP_FONT_FAMILY, 11))
    holder.create_window(width / 2, height / 2, window=entry, width=width - 24)
    return holder, var


def labeled_field(parent, label_text):
    wrap = tk.Frame(parent, bg=PALETTE["bg_outer"])
    wrap.pack(fill="x", padx=20, pady=(10, 2))
    tk.Label(wrap, text=label_text, fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 11, APP_FONT_WEIGHT)).pack(anchor="w")
    return wrap


def labeled_entry(parent, label_text, default=""):
    wrap = labeled_field(parent, label_text)
    holder, var = styled_entry(wrap, width=420, height=34, default=default)
    holder.pack()
    return var


def labeled_spinbox(parent, label_text, from_, to, default=1):
    wrap = labeled_field(parent, label_text)
    var = tk.IntVar(value=max(from_, min(to, default)))
    spin = tk.Spinbox(wrap, from_=from_, to=to, textvariable=var,
                       bg=PALETTE["tag_fill"], fg="white",
                       insertbackground="white", relief="flat",
                       buttonbackground=PALETTE["card_fill"],
                       font=(APP_FONT_FAMILY, 11), justify="center")
    spin.pack(fill="x", pady=(2, 0), ipady=4)
    return var


def labeled_birthday_picker(parent, label_text, default_enabled=False, default_value=None):
    """An optional Day/Month/Year birthday picker with an enable checkbox.
    `default_value`, if given, is an ISO date string ('YYYY-MM-DD').
    Returns (enabled_var, day_var, month_var, year_var, get_iso_or_none)."""
    wrap = labeled_field(parent, label_text)

    current_year = date.today().year
    year_choices = [str(y) for y in range(current_year, BIRTHDAY_MIN_YEAR - 1, -1)]

    def_day, def_month, def_year = 1, 1, current_year
    if default_value:
        try:
            dt = date.fromisoformat(default_value)
            def_day, def_month, def_year = dt.day, dt.month, dt.year
        except Exception:
            pass

    enabled_var = tk.BooleanVar(value=default_enabled)
    tk.Checkbutton(wrap, text="Set a birthday", variable=enabled_var,
                    bg=PALETTE["bg_outer"], fg="white", selectcolor=PALETTE["tag_fill"],
                    activebackground=PALETTE["bg_outer"], activeforeground="white",
                    font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT),
                    command=lambda: set_enabled_state()).pack(anchor="w", pady=(2, 4))

    row = tk.Frame(wrap, bg=PALETTE["bg_outer"])
    row.pack(fill="x")

    day_var = tk.StringVar(value=str(def_day))
    month_var = tk.StringVar(value=MONTH_NAMES[def_month - 1])
    year_var = tk.StringVar(value=str(def_year))

    day_col = tk.Frame(row, bg=PALETTE["bg_outer"])
    day_col.pack(side="left", padx=(0, 5))
    tk.Label(day_col, text="Day", fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 9)).pack(anchor="w")
    day_combo = ttk.Combobox(day_col, textvariable=day_var, width=5, state="readonly",
                              style="Dragon.TCombobox", font=(APP_FONT_FAMILY, 10))
    day_combo.pack()

    month_col = tk.Frame(row, bg=PALETTE["bg_outer"])
    month_col.pack(side="left", padx=5)
    tk.Label(month_col, text="Month", fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 9)).pack(anchor="w")
    month_combo = ttk.Combobox(month_col, textvariable=month_var, values=MONTH_NAMES,
                                width=11, state="readonly", style="Dragon.TCombobox",
                                font=(APP_FONT_FAMILY, 10))
    month_combo.pack()

    year_col = tk.Frame(row, bg=PALETTE["bg_outer"])
    year_col.pack(side="left", padx=(5, 0))
    tk.Label(year_col, text="Year", fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 9)).pack(anchor="w")
    year_combo = ttk.Combobox(year_col, textvariable=year_var, values=year_choices,
                               width=7, state="readonly", style="Dragon.TCombobox",
                               font=(APP_FONT_FAMILY, 10))
    year_combo.pack()

    def refresh_day_options(*_args):
        try:
            m = MONTH_NAMES.index(month_var.get()) + 1
            y = int(year_var.get())
        except (ValueError, IndexError):
            m, y = 1, current_year
        days_in_month = calendar.monthrange(y, m)[1]
        day_combo["values"] = [str(d) for d in range(1, days_in_month + 1)]
        if int(day_var.get() or 1) > days_in_month:
            day_var.set(str(days_in_month))

    month_var.trace_add("write", refresh_day_options)
    year_var.trace_add("write", refresh_day_options)
    refresh_day_options()

    def set_enabled_state():
        state = "readonly" if enabled_var.get() else "disabled"
        for combo in (day_combo, month_combo, year_combo):
            combo.configure(state=state)

    set_enabled_state()

    def get_iso_or_none():
        if not enabled_var.get():
            return None
        try:
            m = MONTH_NAMES.index(month_var.get()) + 1
            return date(int(year_var.get()), m, int(day_var.get())).isoformat()
        except Exception:
            return None

    return enabled_var, day_var, month_var, year_var, get_iso_or_none


def labeled_trait_row(parent, label_text, trait_list, trait_default=None, tier_default=1):
    wrap = labeled_field(parent, label_text)
    row = tk.Frame(wrap, bg=PALETTE["bg_outer"])
    row.pack(fill="x", pady=(2, 0))

    trait_col = tk.Frame(row, bg=PALETTE["bg_outer"])
    trait_col.pack(side="left", fill="x", expand=True, padx=(0, 5))
    tk.Label(trait_col, text="Trait", fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 9)).pack(anchor="w")
    trait_var = tk.StringVar(value=trait_default if trait_default in trait_list else trait_list[0])
    trait_combo = ttk.Combobox(trait_col, textvariable=trait_var, values=trait_list, state="readonly",
                                style="Dragon.TCombobox", font=(APP_FONT_FAMILY, 10))
    trait_combo.pack(fill="x")

    tier_col = tk.Frame(row, bg=PALETTE["bg_outer"])
    tier_col.pack(side="left", padx=(5, 0))
    tk.Label(tier_col, text="Tier", fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 9)).pack(anchor="w")
    tier_var = tk.IntVar(value=max(TRAIT_TIER_MIN, min(TRAIT_TIER_MAX, tier_default or TRAIT_TIER_MIN)))
    tk.Spinbox(tier_col, from_=TRAIT_TIER_MIN, to=TRAIT_TIER_MAX, textvariable=tier_var, width=4,
               bg=PALETTE["tag_fill"], fg="white", insertbackground="white", relief="flat",
               buttonbackground=PALETTE["card_fill"], font=(APP_FONT_FAMILY, 10), justify="center").pack()

    return trait_var, tier_var, trait_combo


def make_search_select(parent, values_or_getter, initial=None, height=5, width=420):
    """A live-search list picker: type in the box, the list below filters
    instantly, click a row to select. More reliable than a type-to-filter
    ttk.Combobox, whose popup list doesn't refresh while it's open.
    `values_or_getter` can be a plain list or a zero-arg callable returning
    the current valid list (for fields whose options change dynamically).
    Returns (wrap_frame, var, refresh_fn) — call refresh_fn() if the valid
    options change for reasons other than typing in this box."""
    def get_base():
        return values_or_getter() if callable(values_or_getter) else values_or_getter

    base_now = get_base()
    start_value = initial if initial in base_now else (base_now[0] if base_now else "")
    var = tk.StringVar(value=start_value)

    wrap = tk.Frame(parent, bg=PALETTE["bg_outer"])

    search_holder, search_var = styled_entry(wrap, width=width, height=32, default="")
    search_holder.pack()

    list_holder = tk.Frame(wrap, bg=PALETTE["bg_outer"])
    list_holder.pack(fill="x", pady=(4, 0))
    listbox = tk.Listbox(list_holder, height=height, bg=PALETTE["tag_fill"], fg="white",
                          selectbackground=PALETTE["card_fill"], selectforeground="white",
                          relief="flat", font=(APP_FONT_FAMILY, 10), highlightthickness=1,
                          highlightbackground=PALETTE["panel_border"], exportselection=False,
                          activestyle="none")
    listbox.pack(side="left", fill="both", expand=True)
    scroll = tk.Scrollbar(list_holder, command=listbox.yview)
    scroll.pack(side="right", fill="y")
    listbox.configure(yscrollcommand=scroll.set)

    selected_label = tk.Label(wrap, text=f"Selected: {var.get()}", fg=PALETTE["title_fill"],
                               bg=PALETTE["bg_outer"], font=(APP_FONT_FAMILY, 9, APP_FONT_WEIGHT), anchor="w")
    selected_label.pack(fill="x", pady=(4, 0))

    def refresh(*_args):
        typed = search_var.get().strip().lower()
        base = get_base()
        filtered = base if not typed else [v for v in base if typed in v.lower()]
        listbox.delete(0, "end")
        for v in filtered:
            listbox.insert("end", v)
        if var.get() in filtered:
            listbox.selection_set(filtered.index(var.get()))

    def on_pick(_event=None):
        sel = listbox.curselection()
        if sel:
            var.set(listbox.get(sel[0]))
            selected_label.config(text=f"Selected: {var.get()}")

    search_var.trace_add("write", refresh)
    listbox.bind("<<ListboxSelect>>", on_pick)
    refresh()

    return wrap, var, refresh


def labeled_search_select(parent, label_text, values_or_getter, default=None, height=5):
    wrap = labeled_field(parent, label_text)
    field, var, refresh = make_search_select(wrap, values_or_getter, initial=default, height=height, width=420)
    field.pack()
    return var, refresh


def labeled_double_search(parent, label_text, left_label, left_values, right_label, right_values,
                           left_default=None, right_default=None, height=4):
    wrap = labeled_field(parent, label_text)
    row = tk.Frame(wrap, bg=PALETTE["bg_outer"])
    row.pack(fill="x", pady=(2, 0))

    left_col = tk.Frame(row, bg=PALETTE["bg_outer"])
    left_col.pack(side="left", fill="both", expand=True, padx=(0, 5))
    tk.Label(left_col, text=left_label, fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 9)).pack(anchor="w")
    lfield, lvar, lrefresh = make_search_select(left_col, left_values, initial=left_default,
                                                 height=height, width=190)
    lfield.pack(fill="x")

    right_col = tk.Frame(row, bg=PALETTE["bg_outer"])
    right_col.pack(side="left", fill="both", expand=True, padx=(5, 0))
    tk.Label(right_col, text=right_label, fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 9)).pack(anchor="w")
    rfield, rvar, rrefresh = make_search_select(right_col, right_values, initial=right_default,
                                                 height=height, width=190)
    rfield.pack(fill="x")

    return lvar, rvar, lrefresh, rrefresh


def labeled_combo(parent, label_text, values, default=None):
    wrap = labeled_field(parent, label_text)
    var = tk.StringVar(value=default if default is not None else (values[0] if values else ""))
    combo = ttk.Combobox(wrap, textvariable=var, values=values, state="readonly",
                          style="Dragon.TCombobox", font=(APP_FONT_FAMILY, 11))
    combo.pack(fill="x", pady=(2, 0))
    return var, combo


def open_dragon_form(parent_win, refresh_callback, dragon_id=None):
    editing = dragon_id is not None
    d = dragons.get(dragon_id, {}) if editing else {}

    form = tk.Toplevel(parent_win)
    form.title("Edit Dragon" if editing else "Add New Dragon")
    form.configure(bg=PALETTE["bg_outer"])
    center(form, 480, 700)

    outer_canvas = tk.Canvas(form, bg=PALETTE["bg_outer"], highlightthickness=0)
    outer_canvas.pack(side="left", fill="both", expand=True)
    vscroll = tk.Scrollbar(form, command=outer_canvas.yview)
    vscroll.pack(side="right", fill="y")
    outer_canvas.configure(yscrollcommand=vscroll.set)

    body = tk.Frame(outer_canvas, bg=PALETTE["bg_outer"])
    outer_canvas.create_window((0, 0), window=body, anchor="nw", width=460)
    body.bind("<Configure>", lambda _e: outer_canvas.configure(scrollregion=outer_canvas.bbox("all")))
    bind_mousewheel(outer_canvas)

    tk.Label(body, text="Edit Dragon" if editing else "Add New Dragon",
             fg=PALETTE["title_fill"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 18, APP_FONT_WEIGHT)).pack(pady=(16, 4))

    img_row = tk.Frame(body, bg=PALETTE["bg_outer"])
    img_row.pack(pady=10)
    preview_canvas = tk.Canvas(img_row, width=100, height=100, bg=PALETTE["bg_outer"], highlightthickness=0)
    preview_canvas.pack(side="left", padx=(0, 12))

    has_custom_icon = {"val": os.path.exists(custom_dragon_image_path(dragon_id or ""))}

    def update_preview():
        preview_canvas.delete("all")
        round_rect(preview_canvas, 2, 2, 98, 98, r=14, fill="#2A2143",
                    outline=PALETTE["panel_border"], width=2)
        try:
            if has_custom_icon["val"] and dragon_id:
                icon_path = custom_dragon_image_path(dragon_id)
            else:
                icon_path = species_icon_path(species_var.get())
            photo = make_rounded_photo(icon_path, 90, 90, radius=12)
            preview_canvas._ref = photo
            preview_canvas.create_image(50, 50, image=photo)
        except Exception:
            preview_canvas.create_text(50, 50, text="No\nIcon", fill="#9B8FCC",
                                        font=(APP_FONT_FAMILY, 9, APP_FONT_WEIGHT), justify="center")

    icon_btn_col = tk.Frame(img_row, bg=PALETTE["bg_outer"])
    icon_btn_col.pack(side="left")

    def browse_custom_icon():
        from tkinter import filedialog as _tkfd
        path = _tkfd.askopenfilename(
            title="Choose a custom dragon icon",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")])
        if not path:
            return
        temp_id = dragon_id or uuid.uuid4().hex[:10]
        result = import_dragon_custom_image(path, temp_id)
        if result:
            has_custom_icon["val"] = True
            update_preview()
            custom_label.config(text="Custom icon set")

    def clear_custom_icon():
        p = custom_dragon_image_path(dragon_id or "")
        if os.path.exists(p):
            try:
                os.remove(p)
            except Exception:
                pass
        has_custom_icon["val"] = False
        update_preview()
        custom_label.config(text="Using species default")

    tk.Button(icon_btn_col, text="Upload Icon…", command=browse_custom_icon,
               bg=PALETTE["tag_fill"], fg="white", relief="flat",
               font=(APP_FONT_FAMILY, 9, APP_FONT_WEIGHT), pady=4).pack(fill="x", pady=(0, 4))
    tk.Button(icon_btn_col, text="Clear Custom", command=clear_custom_icon,
               bg=PALETTE["row_fill"], fg="white", relief="flat",
               font=(APP_FONT_FAMILY, 9, APP_FONT_WEIGHT), pady=4).pack(fill="x")
    custom_label = tk.Label(icon_btn_col,
                             text="Custom icon set" if has_custom_icon["val"] else "Using species default",
                             fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
                             font=(APP_FONT_FAMILY, 8), wraplength=120, justify="left")
    custom_label.pack(anchor="w", pady=(6, 0))

    nickname_var = labeled_entry(body, "Nickname", default=d.get("Nickname", ""))

    species_var, _species_refresh = labeled_search_select(body, "Species", SPECIES_LIST,
                                                            default=d.get("Species"), height=5)

    rarity_var = tk.StringVar(value=d.get("Rarity", "Common"))

    def sync_rarity_to_species(*_args):
        known_rarity = SPECIES_RARITY.get(species_var.get())
        if known_rarity:
            rarity_var.set(known_rarity)

    species_var.trace_add("write", sync_rarity_to_species)
    species_var.trace_add("write", lambda *_: update_preview())
    sync_rarity_to_species()
    update_preview()

    gender_var, _gender_combo = labeled_combo(body, "Gender", GENDER_LIST, default=d.get("Gender", GENDER_LIST[0]))

    soulbound_wrap = labeled_field(body, "Soulbound")
    soulbound_var = tk.BooleanVar(value=bool(d.get("Soulbound", False)))
    tk.Checkbutton(soulbound_wrap, text="This dragon is soulbound", variable=soulbound_var,
                    bg=PALETTE["bg_outer"], fg="white", selectcolor=PALETTE["tag_fill"],
                    activebackground=PALETTE["bg_outer"], activeforeground="white",
                    font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT)).pack(anchor="w", pady=(2, 0))

    bday_enabled, bday_day, bday_month, bday_year, get_birthday_iso = labeled_birthday_picker(
        body, "Birthday (optional)",
        default_enabled=bool(d.get("Birthday")), default_value=d.get("Birthday"))

    owner_enabled_wrap = labeled_field(body, "Original Owner (optional)")
    owner_enabled_var = tk.BooleanVar(value=bool(d.get("OriginalOwner")))
    owner_text_var = tk.StringVar(value=d.get("OriginalOwner", ""))

    tk.Checkbutton(owner_enabled_wrap, text="Track original owner", variable=owner_enabled_var,
                    bg=PALETTE["bg_outer"], fg="white", selectcolor=PALETTE["tag_fill"],
                    activebackground=PALETTE["bg_outer"], activeforeground="white",
                    font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT),
                    command=lambda: set_owner_state()).pack(anchor="w", pady=(2, 4))

    owner_holder = tk.Canvas(owner_enabled_wrap, width=420, height=34,
                              bg=PALETTE["bg_outer"], highlightthickness=0)
    owner_holder.pack()
    round_rect(owner_holder, 2, 2, 418, 32, r=12,
                fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"], width=2)
    owner_entry_widget = tk.Entry(owner_holder, textvariable=owner_text_var,
                                   bg=PALETTE["tag_fill"], fg="white",
                                   insertbackground="white", relief="flat",
                                   font=(APP_FONT_FAMILY, 11))
    owner_holder.create_window(210, 17, window=owner_entry_widget, width=396)

    def set_owner_state():
        owner_entry_widget.configure(state="normal" if owner_enabled_var.get() else "disabled")

    set_owner_state()

    _level_raw = d.get("Level", 1)
    level_default = int(_level_raw) if str(_level_raw).isdigit() else 1
    level_var = labeled_spinbox(body, "Level (1-50)", 1, 50, default=level_default)
    generation_var = labeled_entry(body, "Generation", default=str(d.get("Generation", "1")))
    age_default = d.get("Age") if d.get("Age") in AGE_LIST else AGE_LIST[0]
    age_var, _age_combo = labeled_combo(body, "Age", AGE_LIST, default=age_default)

    d_colors = d.get("Colors", {})
    d_materials = d.get("Materials", {})

    color_vars = []

    def color_values_for(slot_index):
        def getter():
            legendary_slot = next((i for i, v in enumerate(color_vars) if v.get() == "Legendary"), None)
            non_legendary = [c for c in COLOR_LIST if c != "Legendary"]
            return COLOR_LIST if (legendary_slot is None or legendary_slot == slot_index) else non_legendary
        return getter

    p_color, p_material, p_color_refresh, p_material_refresh = labeled_double_search(
        body, "Primary Coat", "Color", color_values_for(0), "Material", MATERIAL_LIST,
        left_default=d_colors.get("P"), right_default=d_materials.get("P"))
    s_color, s_material, s_color_refresh, s_material_refresh = labeled_double_search(
        body, "Secondary Coat", "Color", color_values_for(1), "Material", MATERIAL_LIST,
        left_default=d_colors.get("S"), right_default=d_materials.get("S"))
    t_color, t_material, t_color_refresh, t_material_refresh = labeled_double_search(
        body, "Tertiary Coat", "Color", color_values_for(2), "Material", MATERIAL_LIST,
        left_default=d_colors.get("T"), right_default=d_materials.get("T"))

    color_vars.extend([p_color, s_color, t_color])
    color_refreshes = [p_color_refresh, s_color_refresh, t_color_refresh]

    def enforce_single_legendary(*_args):
        for refresh in color_refreshes:
            refresh()

    for var in color_vars:
        var.trace_add("write", enforce_single_legendary)
    enforce_single_legendary()

    mutations_var, _mutations_combo = labeled_combo(body, "Mutations", [str(i) for i in range(MUTATION_CAP + 1)],
                                                      default=str(d.get("Mutations", MUTATION_CAP)))
    cosmetic_var, _cosmetic_refresh = labeled_search_select(body, "Cosmetic Trait", COSMETIC_TRAIT_LIST,
                                                              default=d.get("CosmeticTrait", "None"), height=5)
    pupil_var, _pupil_combo = labeled_combo(body, "Pupil", PUPIL_LIST, default=d.get("Pupil"))

    elem_wrap = labeled_field(body, "Element")
    element_row, element_selected = make_element_picker(elem_wrap, initial=d.get("Element", ELEMENT_LIST[0]))
    element_row.pack(anchor="w")

    element2_var = None
    if account_settings.get("Subscription", False):
        e2_choices = ["None"] + list(ELEMENT_LIST)
        element2_var, _e2_refresh = labeled_search_select(
            body, "Element 2 (Subscription — optional)",
            e2_choices, default=d.get("Element2") or "None", height=4)

    tk.Label(body, text="Genetic Traits", fg=PALETTE["title_fill"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 16, APP_FONT_WEIGHT)).pack(pady=(20, 0))

    d_positive = d.get("PositiveTraits", [])
    d_negative = d.get("NegativeTraits", [])

    positive_trait_vars = []
    positive_trait_combos = []
    for i in range(MAX_POSITIVE_TRAITS):
        existing = d_positive[i] if i < len(d_positive) else {}
        tvar, nvar, tcombo = labeled_trait_row(body, f"Positive Trait {i + 1}", POSITIVE_TRAIT_LIST,
                                                trait_default=existing.get("Trait", "None"),
                                                tier_default=existing.get("Tier", 1))
        positive_trait_vars.append((tvar, nvar))
        positive_trait_combos.append((tvar, tcombo))

    negative_trait_vars = []
    negative_trait_combos = []
    for i in range(MAX_NEGATIVE_TRAITS):
        existing = d_negative[i] if i < len(d_negative) else {}
        tvar, nvar, tcombo = labeled_trait_row(body, f"Negative Trait {i + 1}", NEGATIVE_TRAIT_LIST,
                                                trait_default=existing.get("Trait", "None"),
                                                tier_default=existing.get("Tier", 1))
        negative_trait_vars.append((tvar, nvar))
        negative_trait_combos.append((tvar, tcombo))

    def sync_trait_options(*_args):
        sp = species_var.get()
        pos_base = available_positive_traits(sp)
        neg_base = available_negative_traits(sp)

        chosen_pos = {var.get() for var, _ in positive_trait_combos if var.get() != "None"}
        for var, combo in positive_trait_combos:
            mine = var.get()
            if mine != "None" and mine not in pos_base:
                var.set("None")
                mine = "None"
            avail = [t for t in pos_base if t == "None" or t == mine or t not in chosen_pos]
            combo["values"] = avail

        for var, combo in negative_trait_combos:
            mine = var.get()
            if mine != "None" and mine not in neg_base:
                var.set("None")
            combo["values"] = neg_base

    species_var.trace_add("write", sync_trait_options)
    for tvar, _ in positive_trait_combos:
        tvar.trace_add("write", sync_trait_options)
    sync_trait_options()

    def save_dragon():
        nickname = nickname_var.get().strip() or species_var.get()
        if len(nickname) > 20:
            messagebox.showwarning("Nickname too long",
                                    f"Nickname must be 20 characters or less (currently {len(nickname)}).")
            return

        if bday_enabled.get() and not get_birthday_iso():
            messagebox.showwarning("Invalid birthday",
                                    "Birthday is enabled but the selected date isn't valid. "
                                    "Pick a Day, Month, and Year, or turn the birthday off.")
            return

        owner_value = owner_text_var.get().strip()
        if owner_enabled_var.get() and not owner_value:
            messagebox.showwarning("Missing owner",
                                    "Original Owner is enabled but no username was entered. "
                                    "Type a username, or turn this off.")
            return

        new_id = dragon_id if editing else uuid.uuid4().hex[:10]
        gen_text = generation_var.get().strip()
        if gen_text.lstrip("-").isdigit():
            generation = max(1, int(gen_text))
        else:
            generation = gen_text or "-"
        try:
            level = max(1, min(50, int(level_var.get())))
        except (TypeError, ValueError, tk.TclError):
            level = 1
        age = age_var.get()

        def collect_traits(trait_vars):
            collected = []
            for trait_var, tier_var in trait_vars:
                trait_name = trait_var.get()
                if trait_name and trait_name != "None":
                    try:
                        tier = max(TRAIT_TIER_MIN, min(TRAIT_TIER_MAX, int(tier_var.get())))
                    except (TypeError, ValueError, tk.TclError):
                        tier = TRAIT_TIER_MIN
                    collected.append({"Trait": trait_name, "Tier": tier})
            return collected

        dragons[new_id] = {
            "Nickname": nickname,
            "Species": species_var.get(),
            "Rarity": rarity_var.get(),
            "Gender": gender_var.get(),
            "Soulbound": soulbound_var.get(),
            "Birthday": get_birthday_iso() if bday_enabled.get() else None,
            "OriginalOwner": owner_value if owner_enabled_var.get() else None,
            "Level": level,
            "Colors": {"P": p_color.get(), "S": s_color.get(), "T": t_color.get()},
            "Materials": {"P": p_material.get(), "S": s_material.get(), "T": t_material.get()},
            "Mutations": int(mutations_var.get()),
            "MaxMutations": MUTATION_CAP,
            "CosmeticTrait": cosmetic_var.get(),
            "Element": element_selected["value"],
            "Element2": (element2_var.get() if element2_var and element2_var.get() != "None" else None),
            "Pupil": pupil_var.get(),
            "Generation": generation,
            "Age": age,
            "PositiveTraits": collect_traits(positive_trait_vars),
            "NegativeTraits": collect_traits(negative_trait_vars),
        }
        persist()
        if refresh_callback:
            refresh_callback()
        form.destroy()

    button_row = tk.Canvas(body, width=420, height=50, bg=PALETTE["bg_outer"], highlightthickness=0)
    button_row.pack(pady=24)
    rounded_button(button_row, 0, 0, 200, 50, "Cancel", form.destroy, r=16,
                    fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"])
    rounded_button(button_row, 220, 0, 200, 50, "Save Changes" if editing else "Save Dragon",
                    save_dragon, r=16,
                    fill=PALETTE["bar_fill"], outline=PALETTE["bar_border"], text_fill="#16330F")

    return form


def open_add_account_dialog(root, refresh_callback):
    dialog = tk.Toplevel(root)
    dialog.title("Add Account")
    dialog.configure(bg=PALETTE["bg_outer"])
    center(dialog, 360, 230)

    tk.Label(dialog, text="New Account Name", fg=PALETTE["title_fill"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 16, APP_FONT_WEIGHT)).pack(pady=(22, 4))

    name_var = labeled_entry(dialog, "Username")

    def create_account():
        name = name_var.get().strip()
        if not name:
            messagebox.showwarning("Missing name", "Please enter an account name.")
            return
        if " " in name:
            messagebox.showwarning("Invalid name", "Account names cannot contain spaces.")
            return
        if len(name) > 20:
            messagebox.showwarning("Name too long",
                                    f"Account names must be 20 characters or less (currently {len(name)}).")
            return
        if name in all_accounts_data:
            messagebox.showwarning("Already exists", f'An account named "{name}" already exists.')
            return
        all_accounts_data[name] = {}
        save_all_accounts(all_accounts_data)
        refresh_callback()
        dialog.destroy()

    btn_row = tk.Canvas(dialog, width=300, height=50, bg=PALETTE["bg_outer"], highlightthickness=0)
    btn_row.pack(pady=20)
    rounded_button(btn_row, 0, 0, 140, 50, "Cancel", dialog.destroy, r=14,
                    fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"])
    rounded_button(btn_row, 160, 0, 140, 50, "Create", create_account, r=14,
                    fill=PALETTE["bar_fill"], outline=PALETTE["bar_border"], text_fill="#16330F")


def _version_tuple(v):
    try:
        return tuple(int(x) for x in v.lstrip("v").split("."))
    except Exception:
        return (0,)


def fetch_latest_release():
    """Hits the GitHub API and returns (tag, exe_download_url) or (None, None)."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    req = urllib.request.Request(url, headers={"User-Agent": f"Lairkeeper/{APP_VERSION}"})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
        tag = data.get("tag_name", "").replace("Lairkeeper ", "").lstrip("v")
        assets = data.get("assets", [])
        dl_url = next(
            (a["browser_download_url"] for a in assets
             if a["name"].lower() == "lairkeeper.exe"),
            None,
        )
        return tag, dl_url
    except Exception:
        return None, None


def check_for_updates_async(parent_win, on_result):
    """Runs the version check on a background thread so the UI doesn't freeze.
    `on_result(tag, dl_url, is_newer)` is called on the main thread via .after()."""
    def _worker():
        tag, dl_url = fetch_latest_release()
        newer = tag is not None and _version_tuple(tag) > _version_tuple(APP_VERSION)
        parent_win.after(0, lambda: on_result(tag, dl_url, newer))
    threading.Thread(target=_worker, daemon=True).start()


def perform_update(parent_win, dl_url):
    """Downloads the new exe to a temp file beside the current one, writes a
    tiny updater.bat that swaps the files after the app exits, then quits."""
    if not getattr(sys, "frozen", False):
        messagebox.showinfo(
            "Script mode",
            "Auto-update only works when running the compiled Lairkeeper.exe.\n"
            "To update the script version, download the latest code.py from GitHub.",
            parent=parent_win)
        return

    exe_path = sys.executable
    exe_dir = os.path.dirname(exe_path)
    tmp_exe = os.path.join(exe_dir, "Lairkeeper_update.exe")
    updater_bat = os.path.join(exe_dir, "_lk_updater.bat")

    dlg = tk.Toplevel(parent_win)
    dlg.title("Updating Lairkeeper")
    dlg.configure(bg=PALETTE["bg_outer"])
    center(dlg, 360, 120)
    dlg.resizable(False, False)
    status_var = tk.StringVar(value="Connecting…")
    tk.Label(dlg, textvariable=status_var, fg="white", bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 11, APP_FONT_WEIGHT)).pack(pady=(24, 8))
    prog_canvas = tk.Canvas(dlg, width=300, height=14, bg=PALETTE["tag_fill"],
                             highlightthickness=1, highlightbackground=PALETTE["panel_border"])
    prog_canvas.pack()
    prog_bar = prog_canvas.create_rectangle(0, 0, 0, 14, fill=PALETTE["bar_fill"], outline="")
    dlg.update()

    def _download():
        try:
            req = urllib.request.Request(dl_url, headers={"User-Agent": f"Lairkeeper/{APP_VERSION}"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                total = int(resp.headers.get("Content-Length", 0))
                downloaded = 0
                chunk = 65536
                with open(tmp_exe, "wb") as f:
                    while True:
                        block = resp.read(chunk)
                        if not block:
                            break
                        f.write(block)
                        downloaded += len(block)
                        if total:
                            pct = downloaded / total
                            parent_win.after(0, lambda p=pct: (
                                prog_canvas.coords(prog_bar, 0, 0, 300 * p, 14),
                                status_var.set(f"Downloading… {int(p*100)}%"),
                                dlg.update_idletasks(),
                            ))
            parent_win.after(0, _swap)
        except Exception as e:
            parent_win.after(0, lambda: (
                dlg.destroy(),
                messagebox.showerror("Update failed", f"Download error:\n{e}", parent=parent_win),
            ))

    def _swap():
        status_var.set("Installing…")
        dlg.update()
        bat = (
            "@echo off\n"
            "timeout /t 2 /nobreak >nul\n"
            f'move /Y "{tmp_exe}" "{exe_path}"\n'
            f'start "" "{exe_path}"\n'
            'del "%~f0"\n'
        )
        with open(updater_bat, "w") as f:
            f.write(bat)
        subprocess.Popen(
            ["cmd", "/c", updater_bat],
            creationflags=subprocess.CREATE_NEW_CONSOLE,
            close_fds=True,
        )
        parent_win.after(600, parent_win.destroy)

    threading.Thread(target=_download, daemon=True).start()


def open_update_dialog(parent_win, tag, dl_url):
    dlg = tk.Toplevel(parent_win)
    dlg.title("Update Available")
    dlg.configure(bg=PALETTE["bg_outer"])
    center(dlg, 380, 180)
    dlg.resizable(False, False)
    tk.Label(dlg, text=f"A new version is available!",
             fg=PALETTE["title_fill"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 14, APP_FONT_WEIGHT)).pack(pady=(20, 4))
    tk.Label(dlg, text=f"Current: Lairkeeper v{APP_VERSION}     →     New: Lairkeeper v{tag}",
             fg="white", bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 10)).pack(pady=(0, 16))
    btn_row = tk.Frame(dlg, bg=PALETTE["bg_outer"])
    btn_row.pack()
    tk.Button(btn_row, text="Update Now", command=lambda: (dlg.destroy(), perform_update(parent_win, dl_url)),
               bg=PALETTE["bar_fill"], fg="#16330F", relief="flat",
               font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT), padx=18, pady=6).pack(side="left", padx=8)
    tk.Button(btn_row, text="Not Now", command=dlg.destroy,
               bg=PALETTE["tag_fill"], fg="white", relief="flat",
               font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT), padx=18, pady=6).pack(side="left", padx=8)


def start():
    root = tk.Tk()
    root.title("Accounts")
    set_window_icon(root)
    load_custom_fonts()
    setup_ttk_style(root)
    center(root, 440, 600)

    bg_canvas = tk.Canvas(root, width=440, height=600, bg=PALETTE["bg_outer"], highlightthickness=0)
    bg_canvas.place(x=0, y=0, width=440, height=600)
    round_rect(bg_canvas, 15, 15, 425, 585, r=26,
                fill=PALETTE["panel_fill"], outline=PALETTE["panel_border"], width=5)
    outline_text(bg_canvas, 220, 55, "Select Account", (APP_FONT_FAMILY, 22, APP_FONT_WEIGHT),
                 PALETTE["title_fill"], PALETTE["title_outline"])

    MAX_LIST_HEIGHT = 375

    list_holder = tk.Frame(root, bg=PALETTE["panel_fill"])
    list_holder.place(x=30, y=95, width=380, height=375)

    list_canvas = tk.Canvas(list_holder, bg=PALETTE["panel_fill"], highlightthickness=0, height=1)
    list_canvas.pack(side="left", fill="x", expand=True, anchor="n")
    list_scroll = tk.Scrollbar(list_holder, command=list_canvas.yview)
    list_scroll.pack(side="right", fill="y")
    list_canvas.configure(yscrollcommand=list_scroll.set)
    bind_mousewheel(list_canvas)

    rows_frame = tk.Frame(list_canvas, bg=PALETTE["panel_fill"])
    rows_window_id = list_canvas.create_window((0, 0), window=rows_frame, anchor="nw")
    list_canvas.bind("<Configure>", lambda e: list_canvas.itemconfig(rows_window_id, width=e.width))

    def render_accounts():
        for w in rows_frame.winfo_children():
            w.destroy()

        if not all_accounts_data:
            tk.Label(rows_frame, text="No accounts yet —\ntap + Add Account below",
                     fg=PALETTE["label_text"], bg=PALETTE["panel_fill"],
                     font=(APP_FONT_FAMILY, 12, APP_FONT_WEIGHT), justify="center").pack(pady=60)

        for acc in list(all_accounts_data.keys()):
            row = tk.Canvas(rows_frame, width=350, height=56, bg=PALETTE["panel_fill"], highlightthickness=0)
            row.pack(pady=6)
            round_rect(row, 2, 2, 348, 54, r=14,
                        fill=PALETTE["card_fill"], outline=PALETTE["card_border"], width=2)
            rounded_button(row, 6, 6, 270, 44, acc,
                            lambda r=root, u=acc: open_lair(r, u), r=10,
                            fill=PALETTE["card_fill"], outline="")

            def make_delete(u=acc):
                def _delete():
                    if messagebox.askyesno("Delete account",
                                            f'Delete "{u}" and all its dragons? This can\'t be undone.'):
                        all_accounts_data.pop(u, None)
                        try:
                            shutil.rmtree(_account_dir(u), ignore_errors=True)
                        except Exception:
                            pass
                        render_accounts()
                return _delete

            rounded_button(row, 282, 6, 62, 44, "\u2715", make_delete(), r=10,
                            fill="#7A2020", outline="#4A1010")

        rows_frame.update_idletasks()
        content_h = max(1, rows_frame.winfo_reqheight())
        list_canvas.configure(height=min(content_h, MAX_LIST_HEIGHT))
        list_canvas.configure(scrollregion=list_canvas.bbox("all"))

    render_accounts()

    add_canvas = tk.Canvas(root, width=380, height=50, bg=PALETTE["bg_outer"], highlightthickness=0)
    add_canvas.place(x=30, y=485)
    rounded_button(add_canvas, 0, 0, 380, 50, "+ Add Account",
                    lambda: open_add_account_dialog(root, render_accounts), r=14,
                    fill=PALETTE["badge_fill"], outline=PALETTE["badge_border"], text_fill="#3A2A06")

    footer = tk.Frame(root, bg=PALETTE["bg_outer"])
    footer.place(x=30, y=544, width=380)
    version_label = tk.Label(footer, text=f"Lairkeeper v{APP_VERSION}", fg=PALETTE["label_text"],
                              bg=PALETTE["bg_outer"], font=(APP_FONT_FAMILY, 9))
    version_label.pack(side="left")

    update_btn_var = tk.StringVar(value="Check for Updates")
    update_btn = tk.Button(footer, textvariable=update_btn_var,
                            command=lambda: _check_updates_clicked(),
                            bg=PALETTE["tag_fill"], fg="white", relief="flat",
                            font=(APP_FONT_FAMILY, 9), padx=10, pady=3,
                            cursor="hand2")
    update_btn.pack(side="right")

    def _check_updates_clicked():
        update_btn.configure(state="disabled")
        update_btn_var.set("Checking…")

        def on_result(tag, dl_url, is_newer):
            update_btn.configure(state="normal")
            if tag is None:
                update_btn_var.set("No connection")
                root.after(3000, lambda: update_btn_var.set("Check for Updates"))
            elif is_newer:
                update_btn_var.set(f"Lairkeeper v{tag} available!")
                open_update_dialog(root, tag, dl_url)
            else:
                update_btn_var.set("Up to date ✓")
                root.after(3000, lambda: update_btn_var.set("Check for Updates"))

        check_for_updates_async(root, on_result)

    root.mainloop()


if __name__ == "__main__":
    start()
