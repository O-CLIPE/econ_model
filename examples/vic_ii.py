from econ.table_classes import *
from econ import TablesAndDatabase


def main():
    db = TablesAndDatabase(schema='vic_ii', password="../credentials.txt", pass_in_file=True)
    with open('../sql/market_and_entities.sql') as file:
        db.build(file.read())
    victoria_ii_goods()
    Good.auto_generate_id_atts('good_id')
    for good in Good:
        print(good)


def victoria_ii_goods():
    # RGOs
    cattle = Good('Cattle', work=55.6)
    coal = Good('Coal', work=41.7)
    coffee = Good('Coffee', work=66.7)
    cotton = Good('Cotton', work=45.5)
    dye = Good('Dye', work=454.5)
    fish = Good('Fish', work=45.5)
    grain = Good('Grain', work=55.6)
    iron = Good('Iron', work=55.6)
    oil = Good('Oil', work=100)
    opium = Good('Opium', work=142.8)
    fruit = Good('Fruit', work=35.7)
    precious_metal = Good('Precious Metal', work=50)
    rubber = Good('Rubber', work=133.3)
    wool = Good('Wool', work=20)
    silk = Good('Silk', work=400)
    sulphur = Good('Sulphur', work=50)
    tea = Good('Tea', work=54.1)
    timber = Good('Timber', work=12.5)
    tobacco = Good('Tobacco', work=40)
    tropical_wood = Good('Tropical Wood', work=25)
    # Factory Goods
    lumber = Good('Lumber', production_goods=[(timber, 0.91), ], work=9.1)
    fabric = Good('Fabric', production_goods=[(dye, 0.05), (cotton, 0.4)], work=22.2)
    glass = Good('Glass', production_goods=[(coal, 0.8), ], work=55.5)
    paper = Good('Paper', production_goods=[(timber, 2.5), ], work=50)
    steel = Good('Steel', production_goods=[(coal, 0.25), (iron, 1)], work=50)
    furniture = Good('Furniture', production_goods=[(timber, 1.6), (lumber, 1.6)], work=83.3)
    regular_clothes = Good('Regular Clothes', production_goods=[(fabric, 2.6), ], work=66.6)
    liquor = Good('Liquor', production_goods=[(grain, 1), (glass, 0.8)], work=200)
    wine = Good('Wine', production_goods=[(fruit, 1.4), (glass, 1.4)], work=286)
    fertilizer = Good('Fertilizer', production_goods=[(sulphur, 1.2), ], work=200)
    industrial_dye = Good('Dye', production_goods=[(coal, 3.6), ], work=400)
    synthetic_oil = Good('Oil', production_goods=[(coal, 4.8), ], work=400)
    canned_food = Good('Canned Food', production_goods=[(iron, 0.25), (fish, 2), (cattle, 2), (grain, 2)], work=500)
    electric_gear = Good('Electric Gear', production_goods=[(coal, 1), (iron, 1), (rubber, 0.8)], work=200)
    cement = Good('Cement', production_goods=[(coal, 4), ], work=333)
    radio = Good('Radio', production_goods=[(glass, 1.5), (electric_gear, 0.45)], work=154)
    telephone = Good('Telephone', production_goods=[(glass, 2.3), (electric_gear, 0.4)], work=154)
    ammunition = Good('Ammunition', production_goods=[(sulphur, 1), (iron, 2), ], work=500)
    explosives = Good('Explosives', production_goods=[(ammunition, 0.25), (fertilizer, 1)], work=333)
    fuel = Good('Fuel', production_goods=[(oil, 1.25), ], work=500)
    machine_parts = Good('Machine Parts', production_goods=[(coal, 2.5), (steel, 4.5)], work=500)
    small_arms = Good('Small Arms', production_goods=[(fuel, 1.5), (ammunition, 1)], work=500)
    clipper_convoys = Good('Clipper Convoys', production_goods=[(timber, 10), (steel, 3), (fabric, 10)], work=100)
    luxury_furniture = Good('Luxury Furniture', production_goods=[(furniture, 1.8), (tropical_wood, 6.8)], work=909)
    artillery = Good('Artillery', production_goods=[(explosives, 0.8), (steel, 6.2)], work=770)
    luxury_clothes = Good('Luxury Clothes', production_goods=[(regular_clothes, 0.9), (silk, 3.9)], work=1000)
    steamer_convoys = Good('Steamer Convoys', production_goods=[(coal, 10), (steel, 7.3)], work=333)
    automobiles = Good('Automobiles', production_goods=[(rubber, 0.7), (steel, 1.6), (electric_gear, 1),
                                                        (machine_parts, 0.73)], work=700)
    tanks = Good('Tanks', production_goods=[(rubber, 1), (electric_gear, 1), (automobiles, 0.3),
                                            (machine_parts, 0.85)], work=1100)
    aeroplanes = Good('Aeroplanes', production_goods=[(lumber, 3.6), (rubber, 1.1), (electric_gear, 2.2),
                                                      (machine_parts, 1.2)], work=1100)


if __name__ == '__main__':
    main()
    