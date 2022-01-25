import hashlib
from modules.security import dao


class CustomSecurity:
    def registration_new_user(self, login, password):
        pass_hash = hashlib.sha256(password.encode())
        password_hash_to_db = pass_hash.hexdigest()

        new_class = dao.DAO()
        new_user_id = new_class.create_user_in_db(login, password_hash_to_db)
        return new_user_id

    def check_user(self, login, password):
        pass_hash = hashlib.sha256(password.encode())
        password_hash_to_db = pass_hash.hexdigest()

        newclass = dao.DAO()
        user_data = newclass.extract_userdata_from_db(login)

        if password_hash_to_db == user_data["hashed_pass"]:
            return {"status_pass": "OK"}
        else:
            return {"status_pass": "BAD"}
