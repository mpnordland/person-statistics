from person_statistics.models import UserListSchema
from person_statistics.processing import *
test_small_json_blob = """
{"results":[{"gender":"male","name":{"title":"Mr","first":"Jacob","last":"Poulsen"},"location":{"street":{"number":3137,"name":"Venusvej"},"city":"Odense Sv","state":"Danmark","country":"Denmark","postcode":49317,"coordinates":{"latitude":"-33.7210","longitude":"-44.8240"},"timezone":{"offset":"+3:00","description":"Baghdad, Riyadh, Moscow, St. Petersburg"}},"email":"jacob.poulsen@example.com","login":{"uuid":"5d85e916-a685-4e8a-af86-1f1883378b40","username":"orangekoala199","password":"ventura","salt":"PAFv3FOP","md5":"789ae2d9f61e80e43fd46b004d9178e0","sha1":"7b9bce3206179b2b6102f6be88cd8bfc5be5bb97","sha256":"c308db872c8492cb4f3ac769f06dda18deca1f097afa4ea83beb1e3341dc21da"},"dob":{"date":"1997-06-01T21:42:55.244Z","age":25},"registered":{"date":"2004-05-12T03:42:50.057Z","age":18},"phone":"52245630","cell":"04137724","id":{"name":"CPR","value":"010697-3802"},"picture":{"large":"https://randomuser.me/api/portraits/men/55.jpg","medium":"https://randomuser.me/api/portraits/med/men/55.jpg","thumbnail":"https://randomuser.me/api/portraits/thumb/men/55.jpg"},"nat":"DK"},{"gender":"male","name":{"title":"Mr","first":"Christian","last":"Thomsen"},"location":{"street":{"number":8226,"name":"Solsikkevej"},"city":"Kongens  Lyngby","state":"Hovedstaden","country":"Denmark","postcode":61838,"coordinates":{"latitude":"-84.2609","longitude":"-8.4030"},"timezone":{"offset":"-5:00","description":"Eastern Time (US & Canada), Bogota, Lima"}},"email":"christian.thomsen@example.com","login":{"uuid":"25bb465e-0454-43f3-9c63-989e0cf0ba3a","username":"brownmouse853","password":"oxford","salt":"GJ4cV9cS","md5":"8ea2414d04171febc55261ff1555b0bd","sha1":"3c09643a1122d0553093ba9b1e36418d36c5b6f4","sha256":"29f8dfc8c94d1672a8a988d485823b396a627dd33ad009a604a347f9f6084a28"},"dob":{"date":"1970-12-31T13:27:08.217Z","age":52},"registered":{"date":"2018-06-25T03:23:52.008Z","age":4},"phone":"63771039","cell":"39184852","id":{"name":"CPR","value":"311270-0605"},"picture":{"large":"https://randomuser.me/api/portraits/men/19.jpg","medium":"https://randomuser.me/api/portraits/med/men/19.jpg","thumbnail":"https://randomuser.me/api/portraits/thumb/men/19.jpg"},"nat":"DK"},{"gender":"female","name":{"title":"Mrs","first":"آدرینا","last":"موسوی"},"location":{"street":{"number":3272,"name":"جمهوری اسلامی"},"city":"رشت","state":"سمنان","country":"Iran","postcode":59374,"coordinates":{"latitude":"60.6490","longitude":"-4.6600"},"timezone":{"offset":"-8:00","description":"Pacific Time (US & Canada)"}},"email":"adryn.mwswy@example.com","login":{"uuid":"e396cb10-6f6e-43d7-9841-908ba0a92536","username":"whitecat109","password":"corleone","salt":"xlnU7sMX","md5":"389049da891c8cab21f9cb3111c7f7d9","sha1":"e12af4a31fda4d14a3f14fd4db18aec6d10c2f8e","sha256":"5fd19eea73e0907a836daeadea37a4e0215773c691d7e4ad1054113882a3ce50"},"dob":{"date":"1979-07-09T15:33:53.459Z","age":43},"registered":{"date":"2019-03-22T06:22:25.589Z","age":3},"phone":"040-98393543","cell":"0941-425-1027","id":{"name":"","value":null},"picture":{"large":"https://randomuser.me/api/portraits/women/36.jpg","medium":"https://randomuser.me/api/portraits/med/women/36.jpg","thumbnail":"https://randomuser.me/api/portraits/thumb/women/36.jpg"},"nat":"IR"}],"info":{"seed":"80f06020794781f3","results":3,"page":1,"version":"1.3"}}
"""

def close_enough(x, y, tolerance=0.001):
    print(abs(x - y))
    return abs(x - y) < tolerance

def test_percentage_female_v_male():
    users = UserListSchema().loads(test_small_json_blob)['results']

    assert close_enough(percentage_female_v_male(users), 0.333)


def test_percentage_first_name_start_a_n():
    users = UserListSchema().loads(test_small_json_blob)['results']

    assert close_enough(percentage_first_name_start_a_m(users), 0.666)



def test_percentage_last_name_start_a_n():
    users = UserListSchema().loads(test_small_json_blob)['results']

    assert close_enough(percentage_last_name_start_a_m(users), 0)


def test_percentage_people_in_states():
    users = UserListSchema().loads(test_small_json_blob)['results']
    result = percentage_people_in_states(users)
    assert len(result) == 3

    for state, p in result:
        assert close_enough(p, 0.333)



def test_percentage_females_in_states():
    users = UserListSchema().loads(test_small_json_blob)['results']
    result = percentage_females_in_states(users)
    assert len(result) == 1

    for state, p in result:
        if state == 'سمنان':
            assert close_enough(p, 1)
        else:
            assert close_enough(p, 0)


def test_percentage_males_in_states():
    users = UserListSchema().loads(test_small_json_blob)['results']
    result = percentage_males_in_states(users)
    assert len(result) == 2

    for state, p in result:
        assert close_enough(p, 1)


    
def test_percentage_people_in_age_ranges():
    users = UserListSchema().loads(test_small_json_blob)['results']
    results = percentage_people_in_age_ranges(users).items()

    for age_range, p in results:
        if age_range == "21-40":
            assert close_enough(p, 0.333)
        elif age_range == "41-60":
            assert close_enough(p, 0.666)
        else:
            assert close_enough(p, 0)