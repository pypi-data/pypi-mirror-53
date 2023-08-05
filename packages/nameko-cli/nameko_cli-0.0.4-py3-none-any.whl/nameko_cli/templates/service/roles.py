import json

defRole = {
    'role': 'default',
    'name': '默认角色',
    'desc': '',
    'functions': [
        # 在此处添加服务功能名称
    ],
    'router': {}
}


ROLES = list()

ROLES.append(json.dumps(defRole))

