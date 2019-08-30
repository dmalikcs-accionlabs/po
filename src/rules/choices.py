from django.utils.decorators import classonlymethod

class ActionChoice:
    STOPPED = 'S'

    @classonlymethod
    def get_choices(cls):
        return (
            (cls.STOPPED, 'Stopped'),
        )


ACTION_LIST = ActionChoice.get_choices()