def create_test_smart_model_handler(instance, **kwargs):
    from .models import TestSmartModel  # NOQA

    TestSmartModel.objects.create(name='name')


def create_test_fields_model_handler(instance, **kwargs):
    from .models import TestFieldsModel  # NOQA

    TestFieldsModel.objects.create()


def create_test_dispatchers_model_handler(instance, **kwargs):
    from .models import TestDispatchersModel  # NOQA

    TestDispatchersModel.objects.create()


def create_csv_record_handler(instance, **kwargs):
    from .models import CSVRecord  # NOQA

    CSVRecord.objects.create()
