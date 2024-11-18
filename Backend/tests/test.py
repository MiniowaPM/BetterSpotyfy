# from sqlalchemy.orm import Session
# from database import *
# from main import *

# users = {
#   "username": [
#     "johndoe123", "janesmith456", "mikebrown789", "emilyjones321", "davidclark654",
#     "alexstone987", "lucyking123", "charliefox456", "sophiablue789", "georgemoon321",
#     "isabellawhite654", "olivergreen789", "chloesilver987", "jackblack321", "gracegold123"
#   ],

#   "first_name": [
#     "John", "Jane", "Mike", "Emily", "David",
#     "Alex", "Lucy", "Charlie", "Sophia", "George",
#     "Isabella", "Oliver", "Chloe", "Jack", "Grace"
#   ],
#     "email": [
#     "johndoe@example.com", "janesmith@example.com", "mikebrown@example.com", "emilyjones@example.com", "davidclark@example.com",
#     "alexstone@example.com", "lucyking@example.com", "charliefox@example.com", "sophiablue@example.com", "georgemoon@example.com",
#     "isabellawhite@example.com", "olivergreen@example.com", "chloesilver@example.com", "jackblack@example.com", "gracegold@example.com"
#   ],
#   "last_name": [
#     "Doe", "Smith", "Brown", "Jones", "Clark",
#     "Stone", "King", "Fox", "Blue", "Moon",
#     "White", "Green", "Silver", "Black", "Gold"
#   ],
#   "gender": [
#     "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", 
#     "2", "2", "2", "2", "2"
#   ],
#   "password": [
#     "P@ssw0rd123", "S3cur3P@ss", "Br0wnM1k3!", "EmilyJ0nes#", "D@v1dC!ark",
#     "St0nePass987!", "KingL1ght123", "F0xCh@rlie456", "BlueSky789@", "MoonSt@r321",
#     "Wh1t3Bella!", "GreenOl1v3r#", "S1lv3rChl0e!", "Bl@ckJ@ck321", "GoldGr@ce!"
#   ],
#   "is_admin": [
#     True, False, False, False, False,
#     False, False, False, False, False,
#     False, False, False, False, False
#   ]
# }

# def add_users_to_db(db: Session):
#     for i in range(len(users["username"])):
#         user = UserBase(
#                 username=users["username"][i],
#                 first_name=users["first_name"][i],
#                 last_name=users["last_name"][i],
#                 email=users["email"][i],
#                 gender=users["gender"][i],
#                 password=users["password"][i],
#                 is_admin=users["is_admin"][i]
#             )
#         db.add(user)
#     db.commit()
        