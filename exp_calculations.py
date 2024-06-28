import pandas as pd
import maple_ranks

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

    days_to_level_dic[days] = level
    # print('{:.1f} Days to {:d}'.format(days, level))

    total_exp = curr_exp

    for i in range(level + 1, level + (goal - level)):
        temp_exp = df.loc[df['Level'] == i, 'EXP to Next Level'].values[0]
        total_exp = total_exp + temp_exp

        days = total_exp / daily_exp
        days_to_level_dic[days] = i + 1
        # print('{:.1f} Days to {:d}'.format(days, i+1))
    
    return days_to_level_dic

def main():

    # Get the data
    info = maple_ranks.get_info('Entyprise')

    # Obtain their level, exp
    _, level, exp = info['level'].split()
    curr_exp_percentage = exp.strip('()')

    # Obtain daily exp
    daily_exp = info['exp_1']
    base = expand_number(daily_exp)
    daily_exp = float(daily_exp[:-1]) * base

    test = calculate_days_to_x_level(int(level), daily_exp, curr_exp_percentage, 290)
    print(test)
    # # First iteration requires to calculate current player exp relative to their level
    # total_exp_to_next_level = df.loc[df['Level'] == int(level), 'EXP to Next Level'].values[0]
    # curr_exp = calculate_curr_exp_value(total_exp_to_next_level, curr_exp_percentage)
    # exp = curr_exp

    # # Test Loop for 282 -> 285
    # for i in range(int(level) + 1, int(level) + 3):
    #     # currExp + 283 exp to level + 284 exp to level
    #     temp_exp = df.loc[df['Level'] == i, 'EXP to Next Level'].values[0]
    #     exp = exp + temp_exp

    #     exp_to_goal = exp / daily_exp
    #     print('{:.1f} Days to {:d}'.format(exp_to_goal, i+1))



if __name__ == "__main__":
    main()
