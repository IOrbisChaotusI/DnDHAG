ability_scores = {"strength": 11, "dexterity": 12, "constitution": 12, "intelligence": 10, "wisdom": 10, "charisma": 10}
challenge_rating = 1/8

attack_name = "Handaxe"
attack_type = "weapon"
primary_ability = "strength"
reach = "5 ft."
num_damage_instances = 1
damage = [
    [1, 6, "damage", "Handaxe", "slashing"]
]
effective_range = "20 ft."
maximum_range = "60 ft."



def proficiency_bonus(challenge_rating):
    if challenge_rating <= 4:
        return 2
    elif challenge_rating <= 8:
        return 3
    elif challenge_rating <= 12:
        return 4
    elif challenge_rating <= 16:
        return 5
    else:
        return 6

def ability_score_modifiers(ability_scores):
    return {k: (v - 10) // 2 for k, v in ability_scores.items()}


def generate_attack_action(attack_name, attack_type, primary_ability, ability_scores, challenge_rating, reach, num_damage_instances, damage, spellcasting_ability=None, effective_range=None, maximum_range=None, add_spell_mod_to_damage=False):
    prof_bonus = proficiency_bonus(challenge_rating)
    ability_modifiers = ability_score_modifiers(ability_scores)
    attack_bonus = ability_modifiers[primary_ability] + prof_bonus
    
    if attack_type == "spell" and spellcasting_ability:
        attack_bonus = ability_modifiers[spellcasting_ability] + prof_bonus

    attack_roll = f'[rollable]+{attack_bonus};{{"diceNotation":"1d20+{attack_bonus}", "rollType":"to hit", "rollAction":"{attack_name}"}}[/rollable]'
    
    damage_str = ""
    for i in range(num_damage_instances):
        dice_num, dice_size, roll_type, roll_action, dmg_type = damage[i]
        dice_expr = f"{dice_num}d{dice_size}"
        if attack_type == "spell" and add_spell_mod_to_damage:
            dice_expr += f"+{ability_modifiers[spellcasting_ability]}"
        elif i == 0:
            dice_expr += f"+{ability_modifiers[primary_ability]}"
        damage_str += f'{dice_expr} [rollable]({dice_expr});{{"diceNotation":"{dice_expr}", "rollType":"{roll_type}", "rollAction":"{roll_action}", "rollDamageType":"{dmg_type}"}}[/rollable] {dmg_type} damage '
        if i < num_damage_instances - 1:
            damage_str += "plus "
    
    range_str = ""
    if reach:
        range_str = f'reach {reach}'
    if effective_range and maximum_range:
        if reach:
            range_str += " or "
        range_str += f'range {effective_range}/{maximum_range}'

    action = f'{attack_name}. {attack_type.capitalize()} Attack: {attack_roll} to hit, {range_str}, one target. Hit: {damage_str}.'
    return action
