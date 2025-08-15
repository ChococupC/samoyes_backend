# Sample Data
User = {
    "T_token" : {
        "username" : "C",
        "roles": ["teacher", "manager"],
    },
    "T_token1": {
        "username" : "J",
        "roles": ["student"],
    }
}

res = {
    "status": "",
    "msg" : "",
    "data": {},
}

def get_auth(token: str):
    allow_role = ["teacher", "manager"]

    #Check if user have a token
    if not token:
        res["status"] = "401"
        res["msg"] = 'Not Login'
        return res

    #Check if user token valid
    user_info = User.get(token)
    if not user_info:
        res["status"] = "401"
        res["msg"] = "Outdated Login"
        return res

    #Check if user role allowed
    roles = user_info.get('roles')
    for role in roles:
        if role in allow_role:
            break
        else:
            res["status"] = "401"
            res["msg"] = "No Permission"
            return res

    #Process Data
    res["status"] = "200"
    res["msg"] = "Authorized"
    res["data"] = {
        "username": user_info.get("username", ""),
        "roles": roles
    }

    return res

if __name__ == "__main__":
    print(get_auth("T_token1"))
