# -*- coding:utf-8 -*-

import uuid


class MessageInfo(object):
    SEND_CALL = 0
    SEND_MESSAGE = 1
    def __init__(self):
        self.send_type = 0
        self.message_id = str(uuid.uuid4())
        self.send_service_name = None

    def __str__(self):
        attrs = vars(self)
        return '\n\r'.join('%s:%s' % item for item in attrs.items())

class BaseMessage(object):
    FAIL = 0
    SUCCESS = 1
    def __init__(self):
        self._base_msg_info = MessageInfo()

    def __str__(self):
        attrs = vars(self)
        return '\n\r'.join('%s:%s' % item for item in attrs.items())

class EmptyMessage(BaseMessage):
    def __init__(self):
        super(EmptyMessage, self).__init__()

class PostResponse(BaseMessage):
    SUCCESS = 0
    FAIL = 1
    def __init__(self):
        super(PostResponse, self).__init__()
        self.status = None


class PolyCityRequest(BaseMessage):
    LIST = 0
    def __init__(self):
        super(PolyCityRequest, self).__init__()
        self.action = None

class PolyCityResponse(BaseMessage):
    SUCCESS = 0
    FAIL = 1
    def __init__(self):
        super(PolyCityResponse, self).__init__()
        self.status = None
        self.cities = []

class PolyProperty(BaseMessage):
    def __init__(self):
        super(PolyProperty, self).__init__()
        self.id = None
        self.name = None
        self.image = None
        self.city = None
        self.description = None
        self.location = None
        self.open_time_from = None
        self.open_time_to = None
        self.property_age = None
        self.surrounding = None

class PolyPropertyRequest(BaseMessage):
    LIST = 0
    DESCRIBE = 1
    def __init__(self):
        super(PolyPropertyRequest, self).__init__()
        self.action = None
        self.city = None
        self.property_id = None

class PolyPropertyResponse(BaseMessage):
    SUCCESS = 0
    FAIL = 1
    def __init__(self):
        super(PolyPropertyResponse, self).__init__()
        self.status = None
        self.properties = None

class PolyStructure(BaseMessage):
    def __init__(self):
        super(PolyStructure, self).__init__()
        self.id = None
        self.name = None
        self.area = None
        self.image = None
        self.room_count = None
        self.hall_count = None
        self.toilet_count = None
        self.lowest_price = None
        self.hall_image = None
        self.kitchen_image = None
        self.bedroom_image = None
        self.toilet_image = None
        self.position_image = None
        self.sketchfab_id = None
        self.yun720_id = None

class StructureFilter(BaseMessage):
    def __init__(self):
        super(StructureFilter, self).__init__()
        self.room_count = None
        self.hall_count = None
        self.toilet_count = None
        self.lower_limit = None
        self.upper_limit = None

class StructureComment(BaseMessage):
    def __init__(self):
        super(StructureComment, self).__init__()
        self.hall_score = None
        self.hall_comment = None
        self.kitchen_score = None
        self.kitchen_comment = None
        self.bedroom_score = None
        self.bedroom_comment = None
        self.toilet_score = None
        self.toilet_comment = None
        self.overview_score = None
        self.overview_comment = None

class PolyCommentRequest(BaseMessage):
    GET = 0
    POST = 1
    EXPORT = 2
    def __init__(self):
        super(PolyCommentRequest, self).__init__()
        self.action = None
        self.openid = None
        self.title = None
        self.phone = None
        self.estimated_time = None
        self.property_id = None
        self.structure_id = None
        self.structure_name = None
        self.comment = None
        self.city = None

class PolyCommentResponse(BaseMessage):
    SUCCESS = 0
    FAIL = 1
    NO_COMMENT = 2
    def __init__(self):
        super(PolyCommentResponse, self).__init__()
        self.status = None
        self.property_id = None
        self.structure_id = None
        self.comment = None

class ExportCommentResponse(BaseMessage):
    SUCCESS = 0
    FAIL = 1
    def __init__(self):
        super(ExportCommentResponse, self).__init__()
        self.status = None
        self.comments = None

class ExportStructureResponse(BaseMessage):
    SUCCESS = 0
    FAIL = 1
    def __init__(self):
        super(ExportStructureResponse, self).__init__()
        self.status = None
        self.structures = None

class PolyStructureRequest(BaseMessage):
    LIST = 0
    FILTER = 1
    DETAIL = 2
    EXPORT = 3
    def __init__(self):
        super(PolyStructureRequest, self).__init__()
        self.action = None
        self.property_id = None
        self.structure_id = None
        self.city = None
        self.filters = None
        self.page = None
        self.count = None

class PolyStructureResponse(BaseMessage):
    SUCCESS = 0
    FAIL = 1
    def __init__(self):
        super(PolyStructureResponse, self).__init__()
        self.status = None
        self.property_info = None
        self.area_filter = []
        self.structure_filter = []
        self.structure_list = []

class PolyStructureDetailResponse(BaseMessage):
    SUCCESS = 0
    FAIL = 1
    EMPTY = 2

    def __init__(self):
        super(PolyStructureDetailResponse, self).__init__()
        self.status = None
        self.structure = None

class UserInformation(BaseMessage):
    def __init__(self):
        super(UserInformation, self).__init__()
        self.openid = None
        self.phone = None
        self.family_structure = None
        self.income_lower = None
        self.income_upper = None
        self.occupation = None
        self.education = None
        self.age = None
        self.purchase_times = None

class UserInformationRequest(BaseMessage):
    UPDATE = 0
    EXPORT = 1
    def __init__(self):
        super(UserInformationRequest, self).__init__()
        self.action = None
        self.city = None
        self.user_information = None

class UserStructureResponse(BaseMessage):
    SUCCESS = 0
    FAIL = 1
    def __init__(self):
        super(UserStructureResponse, self).__init__()
        self.status = None
        self.comment = None
        self.property_info = None
        self.structure = None

class OperateRequest(BaseMessage):
    GET_INDEX = 0
    def __init__(self):
        super(OperateRequest, self).__init__()
        self.action = None

class OperateResponse(BaseMessage):
    SUCCESS = 0
    FAIL = 1
    def __init__(self):
        super(OperateResponse, self).__init__()
        self.status = None
        self.result = None

class WeixinUserInfo(BaseMessage):
    SET = 0
    GET = 1
    SUCCESS = 0
    FAIL = 1
    NO_USER = 2
    def __init__(self):
        super(WeixinUserInfo, self).__init__()
        self.action = None
        self.status = None
        self.openid = None
        self.unionid = None
        self.nickname = None
        self.headimgurl = None
        self.sex = None
        self.lang = None
        self.country = None
        self.province = None
        self.city = None
        self.privilege = None

