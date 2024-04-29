class GetString(object):
    @classmethod
    def get_choice_string(cls,choice):
        dictchoice=dict(cls.CHOICES)
        str=dictchoice[choice]
        return str
    
    @classmethod
    def all(cls):
        return [{"key":name,"key_display_name":cls.get_choice_string(value),"value":value} for name,value in vars(cls).items() if name.isupper() and name != "CHOICES"]

class ObjectStatus(GetString):
    DELETED=0
    ACTIVE=1
    CHOICES=(
        (DELETED,"Deleted"),
        (ACTIVE,"Acive")
    )