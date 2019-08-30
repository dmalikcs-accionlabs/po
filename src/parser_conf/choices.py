from django.utils.decorators import classonlymethod


class SupportedFileFormatChoice:
    XLS = 'X'
    CSV = 'C'

    @classonlymethod
    def get_choices(cls):
        return (
            (cls.XLS, 'XLS'),
            (cls.CSV, 'CSV'),
        )


SUPPORTED_FILE_FORMAT_LIST = SupportedFileFormatChoice.get_choices()


class ColumnChoice:
    VENUE = 'venue'
    EVENTDATE = 'eventdate'
    EVENTTIME = 'eventtime'
    EVENT_NAME = 'event_name'
    SECTION_NAME = 'section_name'
    ROW_NAME = 'row_name'
    SEAT_NUM = 'seat_num'
    LAST_SEAT = 'last_seat'
    NUM_SEATS = 'num_seats'
    ACCT_ID = 'acct_id'
    BARCODE = 'barcode'
    MOBILE = 'mobile'

    @classonlymethod
    def get_choices(cls):
        return (
            (cls.VENUE, 'Venu'),
            (cls.EVENTDATE, 'Event Date'),
            (cls.EVENTTIME, 'Event Time'),
            (cls.EVENT_NAME, 'Event Name'),
            (cls.SECTION_NAME, 'Section Name'),
            (cls.ROW_NAME, 'Row name'),
            (cls.SEAT_NUM, 'Seat number'),
            (cls.LAST_SEAT, 'Last seat'),
            (cls.NUM_SEATS, 'Number seats'),
            (cls.ACCT_ID, 'Account ID'),
            (cls.BARCODE, 'Barcode'),
            (cls.MOBILE, 'Mobile'),
        )


COLUMN_CHOICE_LIST = ColumnChoice.get_choices()


class ShareChoice:
    PUBLIC = 'PUB'
    PRIVATE = 'PVT'
    WITHINTEAM = 'WITH_IN_TEAM'

    @classonlymethod
    def get_choices(cls):
        return (
            (cls.PUBLIC, 'Public'),
            (cls.PRIVATE, 'Private'),
            (cls.WITHINTEAM, 'With In Team'),
        )

SHARE_CHOICE_LIST = ShareChoice.get_choices()


class DATEFormatChoice:
    MMDDYY = '%M%d%Y'
    DDMMYYYY ='%d%M%Y'

    @classonlymethod
    def get_choices(cls):
        return (
            (cls.MMDDYY, 'MMDDYY'),
            (cls.DDMMYYYY, 'DDMMYYY')
        )


DATE_FORMAT_CHOICE_LIST = DATEFormatChoice.get_choices()