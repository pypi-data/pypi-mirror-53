from copy import copy, deepcopy
from functools import partial
from typing import Any, Dict, List, Optional, Set, Tuple, Type, TypeVar, Union

from pypika import Query

from tortoise import fields
from tortoise.backends.base.client import BaseDBAsyncClient  # noqa
from tortoise.exceptions import ConfigurationError, OperationalError
from tortoise.fields import (
    Field,
    ManyToManyField,
    ManyToManyRelationManager,
    RelationQueryContainer,
)
from tortoise.filters import get_filters_for_field
from tortoise.queryset import QuerySet
from tortoise.transactions import current_transaction_map

MODEL_TYPE = TypeVar("MODEL_TYPE", bound="Model")
# TODO: Define Filter type object. Possibly tuple?


def get_unique_together(meta) -> Tuple[Tuple[str, ...], ...]:
    unique_together = getattr(meta, "unique_together", None)

    if isinstance(unique_together, (list, tuple)):
        if unique_together and isinstance(unique_together[0], str):
            unique_together = (unique_together,)

    # return without validation, validation will be done further in the code
    return unique_together


def _fk_setter(self, value, _key, relation_field):
    setattr(self, relation_field, value.pk if value else None)
    setattr(self, _key, value)


def _fk_getter(self, _key):
    return getattr(self, _key, None)


def _rfk_getter(self, _key, ftype, frelfield):
    val = getattr(self, _key, None)
    if val is None:
        val = RelationQueryContainer(ftype, frelfield, self)
        setattr(self, _key, val)
    return val


def _m2m_getter(self, _key, field_object):
    val = getattr(self, _key, None)
    if val is None:
        val = ManyToManyRelationManager(field_object.type, self, field_object)
        setattr(self, _key, val)
    return val


class MetaInfo:
    __slots__ = (
        "abstract",
        "table",
        "app",
        "fields",
        "db_fields",
        "m2m_fields",
        "fk_fields",
        "backward_fk_fields",
        "fetch_fields",
        "fields_db_projection",
        "_inited",
        "fields_db_projection_reverse",
        "filters",
        "fields_map",
        "default_connection",
        "basequery",
        "basequery_all_fields",
        "_filters",
        "unique_together",
        "pk_attr",
        "generated_db_fields",
        "_model",
        "table_description",
        "pk",
        "db_pk_field",
    )

    def __init__(self, meta) -> None:
        self.abstract = getattr(meta, "abstract", False)  # type: bool
        self.table = getattr(meta, "table", "")  # type: str
        self.app = getattr(meta, "app", None)  # type: Optional[str]
        self.unique_together = get_unique_together(meta)  # type: Union[Tuple, List]
        self.fields = set()  # type: Set[str]
        self.db_fields = set()  # type: Set[str]
        self.m2m_fields = set()  # type: Set[str]
        self.fk_fields = set()  # type: Set[str]
        self.backward_fk_fields = set()  # type: Set[str]
        self.fetch_fields = set()  # type: Set[str]
        self.fields_db_projection = {}  # type: Dict[str,str]
        self.fields_db_projection_reverse = {}  # type: Dict[str,str]
        self._filters = {}  # type: Dict[str, Dict[str, dict]]
        self.filters = {}  # type: Dict[str, dict]
        self.fields_map = {}  # type: Dict[str, fields.Field]
        self._inited = False  # type: bool
        self.default_connection = None  # type: Optional[str]
        self.basequery = Query()  # type: Query
        self.basequery_all_fields = Query()  # type: Query
        self.pk_attr = getattr(meta, "pk_attr", "")  # type: str
        self.generated_db_fields = None  # type: Tuple[str]  # type: ignore
        self._model = None  # type: "Model"  # type: ignore
        self.table_description = getattr(meta, "table_description", "")  # type: str
        self.pk = None  # type: fields.Field  # type: ignore
        self.db_pk_field = ""  # type: str

    def add_field(self, name: str, value: Field):
        if name in self.fields_map:
            raise ConfigurationError("Field {} already present in meta".format(name))
        setattr(self._model, name, value)
        value.model = self._model
        self.fields_map[name] = value

        if value.has_db_field:
            self.fields_db_projection[name] = value.source_field or name

        if isinstance(value, fields.ManyToManyField):
            self.m2m_fields.add(name)
        elif isinstance(value, fields.BackwardFKRelation):
            self.backward_fk_fields.add(name)

        field_filters = get_filters_for_field(
            field_name=name, field=value, source_field=value.source_field or name
        )
        self._filters.update(field_filters)
        self.finalise_fields()

    @property
    def db(self) -> BaseDBAsyncClient:
        try:
            return current_transaction_map[self.default_connection].get()
        except KeyError:
            raise ConfigurationError("No DB associated to model")

    def get_filter(self, key: str) -> dict:
        return self.filters[key]

    def finalise_pk(self) -> None:
        self.pk = self.fields_map[self.pk_attr]
        self.db_pk_field = self.pk.source_field or self.pk_attr

    def finalise_model(self) -> None:
        """
        Finalise the model after it had been fully loaded.
        """
        self.finalise_fields()
        self._generate_filters()

    def finalise_fields(self) -> None:
        self.db_fields = set(self.fields_db_projection.values())
        self.fields = set(self.fields_map.keys())
        self.fields_db_projection_reverse = {
            value: key for key, value in self.fields_db_projection.items()
        }
        self.fetch_fields = self.m2m_fields | self.backward_fk_fields | self.fk_fields

        generated_fields = []
        for field in self.fields_map.values():
            if not field.generated:
                continue
            generated_fields.append(field.source_field or field.model_field_name)
        self.generated_db_fields = tuple(generated_fields)  # type: ignore

        # Create lazy FK fields on model.
        for key in self.fk_fields:
            _key = "_{}".format(key)
            relation_field = self.fields_map[key].source_field
            setattr(
                self._model,
                key,
                property(
                    partial(_fk_getter, _key=_key),
                    partial(_fk_setter, _key=_key, relation_field=relation_field),
                    partial(_fk_setter, value=None, _key=_key, relation_field=relation_field),
                ),
            )

        # Create lazy reverse FK fields on model.
        for key in self.backward_fk_fields:
            _key = "_{}".format(key)
            field_object = self.fields_map[key]  # type: fields.BackwardFKRelation  # type: ignore
            setattr(
                self._model,
                key,
                property(
                    partial(
                        _rfk_getter,
                        _key=_key,
                        ftype=field_object.type,
                        frelfield=field_object.relation_field,
                    )
                ),
            )

        # Create lazy M2M fields on model.
        for key in self.m2m_fields:
            _key = "_{}".format(key)
            setattr(
                self._model,
                key,
                property(partial(_m2m_getter, _key=_key, field_object=self.fields_map[key])),
            )

    def _generate_filters(self) -> None:
        get_overridden_filter_func = self.db.executor_class.get_overridden_filter_func
        for key, filter_info in self._filters.items():
            overridden_operator = get_overridden_filter_func(  # type: ignore
                filter_func=filter_info["operator"]
            )
            if overridden_operator:
                filter_info = copy(filter_info)
                filter_info["operator"] = overridden_operator  # type: ignore
            self.filters[key] = filter_info


class ModelMeta(type):
    __slots__ = ()

    def __new__(mcs, name: str, bases, attrs: dict, *args, **kwargs):
        fields_db_projection = {}  # type: Dict[str,str]
        fields_map = {}  # type: Dict[str, fields.Field]
        filters = {}  # type: Dict[str, Dict[str, dict]]
        fk_fields = set()  # type: Set[str]
        m2m_fields = set()  # type: Set[str]
        meta_class = attrs.get("Meta", type("Meta", (), {}))
        pk_attr = "id"

        # Searching for Field attributes in the class hierarchie
        def __search_for_field_attributes(base, attrs: dict):
            """
            Searching for class attributes of type fields.Field
            in the given class.

            If an attribute of the class is an instance of fields.Field,
            then it will be added to the attrs dict. But only, if the
            key is not already in the dict. So derived classes have a higher
            precedence. Multiple Inheritence is supported from left to right.

            After checking the given class, the function will look into
            the classes according to the mro (method resolution order).

            The mro is 'natural' order, in wich python traverses methods and
            fields. For more information on the magic behind check out:
            `The Python 2.3 Method Resolution Order
            <https://www.python.org/download/releases/2.3/mro/>`_.
            """
            for key, value in base.__dict__.items():
                if isinstance(value, fields.Field) and key not in attrs:
                    attrs[key] = value
                    for parent in base.__mro__[1:]:
                        __search_for_field_attributes(parent, attrs)

        # Start searching for fields in the base classes.
        for base in bases:
            __search_for_field_attributes(base, attrs)

        if name != "Model":
            custom_pk_present = False
            for key, value in attrs.items():
                if isinstance(value, fields.Field):
                    if value.pk:
                        if custom_pk_present:
                            raise ConfigurationError(
                                "Can't create model {} with two primary keys, "
                                "only single pk are supported".format(name)
                            )
                        if value.generated and not isinstance(
                            value, (fields.SmallIntField, fields.IntField, fields.BigIntField)
                        ):
                            raise ConfigurationError(
                                "Generated primary key allowed only for IntField and BigIntField"
                            )
                        custom_pk_present = True
                        pk_attr = key

            if not custom_pk_present:
                if "id" not in attrs:
                    attrs = {"id": fields.IntField(pk=True), **attrs}

                if not isinstance(attrs["id"], fields.Field) or not attrs["id"].pk:
                    raise ConfigurationError(
                        "Can't create model {} without explicit primary key "
                        "if field 'id' already present".format(name)
                    )

            for key, value in attrs.items():
                if isinstance(value, fields.Field):
                    if getattr(meta_class, "abstract", None):
                        value = deepcopy(value)

                    fields_map[key] = value
                    value.model_field_name = key

                    if isinstance(value, fields.ForeignKeyField):
                        fk_fields.add(key)
                    elif isinstance(value, fields.ManyToManyField):
                        m2m_fields.add(key)
                    else:
                        fields_db_projection[key] = value.source_field or key
                        filters.update(
                            get_filters_for_field(
                                field_name=key,
                                field=fields_map[key],
                                source_field=fields_db_projection[key],
                            )
                        )
                        if value.pk:
                            filters.update(
                                get_filters_for_field(
                                    field_name="pk",
                                    field=fields_map[key],
                                    source_field=fields_db_projection[key],
                                )
                            )

        attrs["_meta"] = meta = MetaInfo(meta_class)

        meta.fields_map = fields_map
        meta.fields_db_projection = fields_db_projection
        meta._filters = filters
        meta.fk_fields = fk_fields
        meta.backward_fk_fields = set()
        meta.m2m_fields = m2m_fields
        meta.default_connection = None
        meta.pk_attr = pk_attr
        meta._inited = False
        if not fields_map:
            meta.abstract = True

        new_class = super().__new__(mcs, name, bases, attrs)  # type: "Model"  # type: ignore
        for field in meta.fields_map.values():
            field.model = new_class

        meta._model = new_class
        meta.finalise_fields()
        return new_class


class Model(metaclass=ModelMeta):
    # I don' like this here, but it makes autocompletion and static analysis much happier
    _meta = MetaInfo(None)

    def __init__(self, *args, **kwargs) -> None:
        # self._meta is a very common attribute lookup, lets cache it.
        meta = self._meta
        self._saved_in_db = meta.pk_attr in kwargs and meta.pk.generated

        # Assign values and do type conversions
        passed_fields = {*kwargs.keys()}
        passed_fields.update(meta.fetch_fields)
        passed_fields |= self._set_field_values(kwargs)

        # Assign defaults for missing fields
        for key in meta.fields.difference(passed_fields):
            field_object = meta.fields_map[key]
            if callable(field_object.default):
                setattr(self, key, field_object.default())
            else:
                setattr(self, key, field_object.default)

    @classmethod
    def _init_from_db(cls, **kwargs) -> MODEL_TYPE:
        self = cls.__new__(cls)
        self._saved_in_db = True

        meta = self._meta

        for key, value in kwargs.items():
            model_field = meta.fields_db_projection_reverse.get(key)
            if model_field:
                setattr(self, model_field, meta.fields_map[model_field].to_python_value(value))

        return self

    def _set_field_values(self, values_map: Dict[str, Any]) -> Set[str]:
        """
        Sets values for fields honoring type transformations and
        return list of fields that were set additionally
        """
        meta = self._meta
        passed_fields = set()

        for key, value in values_map.items():
            if key in meta.fk_fields:
                if value and not value._saved_in_db:
                    raise OperationalError(
                        "You should first call .save() on {} before referring to it".format(value)
                    )
                field_object = meta.fields_map[key]
                relation_field = field_object.source_field  # type: str  # type: ignore
                setattr(self, key, value)
                passed_fields.add(relation_field)
            elif key in meta.fields_db_projection:
                field_object = meta.fields_map[key]
                if value is None and not field_object.null:
                    raise ValueError("{} is non nullable field, but null was passed".format(key))
                setattr(self, key, field_object.to_python_value(value))
            elif key in meta.db_fields:
                field_object = meta.fields_map[meta.fields_db_projection_reverse[key]]
                if value is None and not field_object.null:
                    raise ValueError("{} is non nullable field, but null was passed".format(key))
                setattr(self, key, field_object.to_python_value(value))
            elif key in meta.backward_fk_fields:
                raise ConfigurationError(
                    "You can't set backward relations through init, change related model instead"
                )
            elif key in meta.m2m_fields:
                raise ConfigurationError(
                    "You can't set m2m relations through init, use m2m_manager instead"
                )

        return passed_fields

    def __str__(self) -> str:
        return "<{}>".format(self.__class__.__name__)

    def __repr__(self) -> str:
        if self.pk:
            return "<{}: {}>".format(self.__class__.__name__, self.pk)
        return "<{}>".format(self.__class__.__name__)

    def __hash__(self) -> int:
        if not self.pk:
            raise TypeError("Model instances without id are unhashable")
        return hash(self.pk)

    def __eq__(self, other) -> bool:
        # pylint: disable=C0123
        if type(self) == type(other) and self.pk == other.pk:
            return True
        return False

    def _get_pk_val(self):
        return getattr(self, self._meta.pk_attr)

    def _set_pk_val(self, value):
        setattr(self, self._meta.pk_attr, value)

    pk = property(_get_pk_val, _set_pk_val)
    """
    Alias to the models Primary Key.
    Can be used as a field name when doing filtering e.g. ``.filter(pk=...)`` etc...
    """

    async def save(self, using_db=None, update_fields=None) -> None:
        """
        Creates/Updates the current model object.

        If ``update_fields`` is provided, it should be a tuple/list of fields by name.
        This is the subset of fields that should be updated.
        If the object needs to be created ``update_fields`` will be ignored.
        """
        db = using_db or self._meta.db
        executor = db.executor_class(model=self.__class__, db=db)
        if self._saved_in_db:
            await executor.execute_update(self, update_fields)
        else:
            await executor.execute_insert(self)
            self._saved_in_db = True

    async def delete(self, using_db=None) -> None:
        """
        Deletes the current model object.

        :raises OperationalError: If object has never been persisted.
        """
        db = using_db or self._meta.db
        if not self._saved_in_db:
            raise OperationalError("Can't delete unpersisted record")
        await db.executor_class(model=self.__class__, db=db).execute_delete(self)

    async def fetch_related(self, *args, using_db=None) -> None:
        """
        Fetch related fields.

        .. code-block:: python3

            User.fetch_related("emails", "manager")

        :param args: The related fields that should be fetched.
        """
        db = using_db or self._meta.db
        await db.executor_class(model=self.__class__, db=db).fetch_for_list([self], *args)

    @classmethod
    async def get_or_create(
        cls: Type[MODEL_TYPE], using_db=None, defaults=None, **kwargs
    ) -> Tuple[MODEL_TYPE, bool]:
        """
        Fetches the object if exists (filtering on the provided parameters),
        else creates an instance with any unspecified parameters as default values.
        """
        if not defaults:
            defaults = {}
        instance = await cls.filter(**kwargs).first()
        if instance:
            return instance, False
        return await cls.create(**defaults, **kwargs, using_db=using_db), True

    @classmethod
    async def create(cls: Type[MODEL_TYPE], **kwargs) -> MODEL_TYPE:
        """
        Create a record in the DB and returns the object.

        .. code-block:: python3

            user = await User.create(name="...", email="...")

        Equivalent to:

        .. code-block:: python3

            user = User(name="...", email="...")
            await user.save()
        """
        instance = cls(**kwargs)
        db = kwargs.get("using_db") or cls._meta.db
        await db.executor_class(model=cls, db=db).execute_insert(instance)
        instance._saved_in_db = True
        return instance

    @classmethod
    async def bulk_create(cls: Type[MODEL_TYPE], objects: List[MODEL_TYPE], using_db=None) -> None:
        """
        Bulk insert operation:

        .. note::
            The bulk insert operation will do the minimum to ensure that the object
            created in the DB has all the defaults and generated fields set,
            but may be incomplete reference in Python.

            e.g. ``IntField`` primary keys will not be poplulated.

        This is recommend only for throw away inserts where you want to ensure optimal
        insert performance.

        .. code-block:: python3

            User.bulk_create([
                User(name="...", email="..."),
                User(name="...", email="...")
            ])

        :param objects: List of objects to bulk create
        """
        db = using_db or cls._meta.db
        await db.executor_class(model=cls, db=db).execute_bulk_insert(objects)

    @classmethod
    def first(cls) -> QuerySet:
        """
        Generates a QuerySet that returns the first record.
        """
        return QuerySet(cls).first()

    @classmethod
    def filter(cls, *args, **kwargs) -> QuerySet:
        """
        Generates a QuerySet with the filter applied.
        """
        return QuerySet(cls).filter(*args, **kwargs)

    @classmethod
    def exclude(cls, *args, **kwargs) -> QuerySet:
        """
        Generates a QuerySet with the exclude applied.
        """
        return QuerySet(cls).exclude(*args, **kwargs)

    @classmethod
    def annotate(cls, **kwargs) -> QuerySet:
        return QuerySet(cls).annotate(**kwargs)

    @classmethod
    def all(cls) -> QuerySet:
        """
        Returns the complete QuerySet.
        """
        return QuerySet(cls)

    @classmethod
    def get(cls, *args, **kwargs) -> QuerySet:
        """
        Fetches a single record for a Model type using the provided filter parameters.

        .. code-block:: python3

            user = await User.get(username="foo")

        :raises MultipleObjectsReturned: If provided search returned more than one object.
        :raises DoesNotExist: If object can not be found.
        """
        return QuerySet(cls).get(*args, **kwargs)

    @classmethod
    async def fetch_for_list(cls, instance_list, *args, using_db=None):
        db = using_db or cls._meta.db
        await db.executor_class(model=cls, db=db).fetch_for_list(instance_list, *args)

    @classmethod
    def check(cls) -> None:
        """
        Calls various checks to validate the model.

        :raises ConfigurationError: If the model has not been configured correctly.
        """
        cls._check_unique_together()

    @classmethod
    def _check_unique_together(cls) -> None:
        """Check the value of "unique_together" option."""
        if cls._meta.unique_together is None:
            return

        if not isinstance(cls._meta.unique_together, (tuple, list)):
            raise ConfigurationError(
                "'{}.unique_together' must be a list or tuple.".format(cls.__name__)
            )

        if any(
            not isinstance(unique_fields, (tuple, list))
            for unique_fields in cls._meta.unique_together
        ):
            raise ConfigurationError(
                "All '{}.unique_together' elements must be lists or tuples.".format(cls.__name__)
            )

        for fields_tuple in cls._meta.unique_together:
            for field_name in fields_tuple:
                field = cls._meta.fields_map.get(field_name)

                if not field:
                    raise ConfigurationError(
                        "'{}.unique_together' has no '{}' "
                        "field.".format(cls.__name__, field_name)
                    )

                if isinstance(field, ManyToManyField):
                    raise ConfigurationError(
                        "'{}.unique_together' '{}' field refers "
                        "to ManyToMany field.".format(cls.__name__, field_name)
                    )

    class Meta:
        """
        The ``Meta`` class is used to configure metadate for the Model.

        Usage:

        .. code-block:: python3

            class Foo(Model):
                ...

                class Meta:
                    table="custom_table"
                    unique_together=(("field_a", "field_b"), )
        """
