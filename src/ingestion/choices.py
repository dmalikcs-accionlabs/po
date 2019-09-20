from django.utils.decorators import classonlymethod


class InventoryStatusChoice:
    NEW = 'N'
    QUEUE = 'Q'
    UPLOADED = 'U'
    UPLOAD_FAILED = 'F'

    @classonlymethod
    def get_choices(cls):
        return (
            (cls.NEW, "New"),
            (cls.UPLOADED, "Uploaded"),
            (cls.UPLOAD_FAILED, "Upload failed"),
        )


INVENTORYSTATUSCHOICE_LIST = InventoryStatusChoice.get_choices()


class StatusChoice:
    NEW = "N"
    STOPED = 'S'
    COMPLETED_SUCCESS = 'C_S'
    COMPLETED_FAILED = 'C_F'

    @classonlymethod
    def get_choices(cls):
        return (
            (cls.NEW, "NEW"),
            (cls.STOPED, "Stopped"),
            (cls.COMPLETED_FAILED, "Failed"),
            (cls.COMPLETED_SUCCESS, "Completed"),
        )


STATUS_CHOICE_STATUS = StatusChoice.get_choices()


class TaskChoice:
    ACK = 'ack'
    ACK_STOPED = 'ack_stoped'
    VALIDATE_FILE_FORMAT = 'validate_file_format'
    VALIDATE_COLUMN_NAME = 'validate_column_name'
    INGESTION_TASK = 'ingestion_task'
    VALIDATE_COLUMN_DATA = 'validate_column_data'
    TRANSFORMATION_DATA = 'trans_data'
    PREPARE_PAYLOAD_TASK = 'prepare_payload_task'
    SEND_PAYLOAD_TASK = 'send_payload_task'
    HANDLE_RESPONSE_TASK = 'handle_res_task'

    @classonlymethod
    def get_choices(cls):
        return (
            (cls.ACK, 'acknowledge'),
            (cls.ACK_STOPED, 'Acknowledge! can not proceed further'),
            (cls.VALIDATE_FILE_FORMAT, 'Validate file format task'),
            (cls.VALIDATE_COLUMN_NAME, 'Validate column names task'),
            (cls.INGESTION_TASK, 'Ingestion tasks '),
            (cls.VALIDATE_COLUMN_DATA, 'Validate column data task'),
            (cls.TRANSFORMATION_DATA, 'Transformation data task'),
            (cls.PREPARE_PAYLOAD_TASK, 'Prepare payload task'),
            (cls.SEND_PAYLOAD_TASK, 'Send payload task'),
            (cls.HANDLE_RESPONSE_TASK, 'Handle response task'),
        )


TASK_CHOICE_LIST = TaskChoice.get_choices()


class IngestionTypeChoice:
    EMAIL = 'E'
    WEB_FORM = 'W'
    API = 'A'

    @classonlymethod
    def get_choices(cls):
        return (
            (cls.EMAIL, 'Email'),
            (cls.WEB_FORM, 'Web'),
            (cls.API, 'API'),
        )


INGESTION_TYPE_LIST = IngestionTypeChoice.get_choices()
