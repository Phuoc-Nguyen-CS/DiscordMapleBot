import pandas as pd

df = pd.read_csv('level_exp.csv')

def simplify_number(num):
    '''
    Turns big numbers to smaller numbers :D

    Args:
        num: A number.
    
    Returns:
        A Number with a corresponding identifier.
    '''
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.2f%s' % (num, ['', 'K', 'M', 'B', 'T'][magnitude])

def expand_number(num):
    '''
    Turns those small numbers into big numbers :D
    Args:
        num: A number with a corresponding identifier.
    Returns:
        A corresponding number to expand the number.
    '''
    temp = num[-1:]
    if temp == 'K':
        return 1000
    elif temp == 'M':
        return 1000000
    elif temp == 'B':
        return 1000000000
    elif temp == 'T':
        return 1000000000000
    else:
        return -1

def calculate_curr_exp_value(total_exp, exp):
    exp = float(exp.replace('%', '')) / 100
    return total_exp - (total_exp * exp)

def calculate_days_to_x_level(level, daily_exp, curr_exp_percentage, goal):
    # Dictionary storing the Days : Level
    days_to_level_dic = {}
    
    # First iteration requires to calculate current player exp relative to their level
    total_exp_to_next_level = df.loc[df['Level'] == level, 'EXP to Next Level'].values[0]
    curr_exp = calculate_curr_exp_value(total_exp_to_next_level, curr_exp_percentage)
    days = curr_exp / daily_exp

    days_to_level_dic[0] = [level + 1, round(float(days), 1)]
    

    total_exp = curr_exp

    # Loop and add to dictionary with format:
    #   Key   -> Integer Value: 
    #   Value -> A List containing [Level, Days]
    key = 0
    for i in range(level + 1, level + (goal - level)):
        
        # Increment the Integer value
        key = key + 1

        temp_exp = df.loc[df['Level'] == i, 'EXP to Next Level'].values[0]
        total_exp = total_exp + temp_exp

        days = total_exp / daily_exp
        days_to_level_dic[key] = [i + 1, round(float(days), 1)]
    
    return days_to_level_dic