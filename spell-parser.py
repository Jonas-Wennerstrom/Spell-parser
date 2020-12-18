##############################
## Two functionsto parse spell descriptions in D&D 5e and 13th Age.
##
## By Jonas Wennerström
##
## https://github.com/Jonas-Wennerstrom
#############################

import re

def parse_dnd_fifth(ability):
    """Given a spell or ability description, prints possible save checks
        DCs, damage, and conditions. Intended to speed up reading.
    """
    conditions = []
    possible_conditions = []
    possible_checks = []
    possible_dc = []
    possible_dmg = []

    print_dict = {"Possible checks: ": possible_checks,
                  "Possible DC: ": possible_dc,
                  "Possible conditions: ": possible_conditions,
                  "Possible damage: ": possible_dmg}

    possible_checks += re.findall(r'\S* \S* check',ability)
    possible_checks += re.findall(r'\S* saving throw',ability)
    possible_dc += re.findall(r'\S* \S* DC',ability)
    possible_dmg += re.findall(r'\dd\d',ability)

    for x in conditions:
        possible_conditions.append(ability.find(x))
    
    for i in print_dict:
        print(i)
        for n in print_dict[i]:
            print('[['+n+']]')
        print('\n')

def parse_thirteenth(base_level,ability):
    """Given a 13th Age ability and its base level, generates a Roll20
        macro with inline-rolls and level selection.
    """
    stats = {"Strength": "@{STR-mod}",
             "Dexterity": "@{DEX-mod}",
             "Constitution": "@{CON-mod}",
             "Intelligence": "@{INT-mod}",
             "Wisdom": "@{WIS-mod}",
             "Charisma": "@{CHA-mod}",
             "Level": " @{level}",
             "level": " @{level}"
             }
    effects = ["Hit","Effect"]
    lvls = ["1", "3", "5", "7", "9"]
    rolls = {i:""for i in lvls[int(base_level/2):]}
    stats_found={}
    raw = ""
    to_parse = {}
    parsed = ["?{At level"]
    lines = ability.split('\n')

    for l in lines:
        if l.find(":") > 0:
            sub, eff = l.split(':',1)
            if sub in effects:
                res = re.findall(r'\d+d\d+',eff)
                raw = eff
                for s in stats:
                    if l.find(s) >= 0:
                        stats_found[s] = stats[s]
                rolls[str(base_level)] = res
            elif sub[0] in rolls:
                res = re.findall(r'\d+d\d+',eff)
                rolls[sub[0]] = res
    for i in range(len(rolls[str(base_level)])):
        raw = raw.replace(
            rolls[str(base_level)][i],
            "{"+str(i)+"}")
    for s in stats_found:
        raw = raw.replace(s, stats_found[s])
    for r in rolls:
        substring = raw
        for i in range(len(rolls[r])):
            substring = substring.replace(
                "{"+str(i)+"}",
                "[["+rolls[r][i]+"]]")
        parsed.append(str(r)+", "+substring)
    parsed = "|".join(parsed)
    parsed = parsed+" }"
    print(lines[0])
    print(parsed)
