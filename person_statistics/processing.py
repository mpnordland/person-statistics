from collections import Counter, defaultdict

#predicates
def is_female(user):
    return user['gender'] == 'female'

def is_male(user):
    return user['gender'] == 'male'

def name_starts_with_a_m(name):
    return name and name[0].lower() in 'abcdefghijklm'

#constructors
def make_percentage_of_total(predicate, users):
    return sum(map(predicate , users)) / len(users)

# operations
def percentage_female_v_male(users):
    return make_percentage_of_total(is_female, users)

def percentage_first_name_start_a_m(users):
    """
    returns percentage of users who's first name starts with a letter in the range A - M
    Assumes all users have names that start with a character from the English alphabet
    """
    return make_percentage_of_total(lambda u: name_starts_with_a_m(u['first_name']), users)


def percentage_last_name_start_a_m(users):
    """
    returns percentage of users who's last name starts with a letter in the range A - M
    Assumes all users have names that start with a character from the English alphabet
    """
    return make_percentage_of_total(lambda u: name_starts_with_a_m(u['last_name']), users)



def percentage_people_in_states(users):
    """
     Percentage of total users that live in this state
     At most ten of the states with the highest percentage will be returned
    """
    total_counter = Counter([u['state'] for u in  users])
    return [(state[0], state[1] / len(users)) for state in total_counter.most_common(10)]

def percentage_filtered_people_in_states(users, predicate):

    total_counter = Counter([u['state'] for u in  users])
    filtered_counter = Counter([u['state'] for u in filter(predicate, users)])
    return [(state[0], state[1] / total_counter[state[0]]) for state in filtered_counter.most_common(10)]



def percentage_females_in_states(users):
    """
     Percentage of female users in each state compared to the total number of users residing in that state
     At most ten of the states with the highest percentage will be returned
     
    """
    return percentage_filtered_people_in_states(users, is_female)


def percentage_males_in_states(users):
    """
     Percentage of male users in each state compared to the total number of users residing in that state
     At most ten of the states with the highest percentage will be returned
     
    """
    return percentage_filtered_people_in_states(users, is_male)


def percentage_people_in_age_ranges(users):
    counts = {
        range(21): 0, # 20 or under
        range(21, 41): 0, # 21 to 40 
        range(41, 61): 0, # 41 to 60
        range(61, 81): 0, # 61 to 80
        range(81, 101): 0, # 81 to 100
    }
    over_100 = 0
    for user in users:

        for age_range in counts.keys():
            if user['age'] in age_range: # checked cpython code for this, range membership test is O(1)
                counts[age_range] += 1
                break
        else:
            over_100 += 1

    result =  {
        f"{r[0]}-{r[-1]}": c / len(users) for r, c in counts.items()
    }

    result['100+'] = over_100 / len(users)

    return result
