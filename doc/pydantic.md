## Pydantic 

* It's a library used for data validation, parsing or to enforce structure on data. 

### Use cases: 
1) Validate external/untrusted input.
2) Parsing API responses. 
3) Configuration management => Loading settings from environment variables, JSON files or YAML, or other sources.
4) Data serialization and deserialization (Converting data to and from JSON, for example).
5) Less biolerplate code for data validation and parsing -> No need for `def __init__()`
6) Automatic casting (coresion) to write fields types (only safe and umbiguous data are allowed).


### Concepts learned: 
1) BaseModel: The core class in Pydantic, which is used to define data models. It provides validation, parsing, and serialization capabilities. It has "ModelMetaclass" which is responsible for creating the model class and handling the validation logic, and managing it .
2) Field: add custom validation, default values, and metadata to model attributes. It allows you to specify constraints, such as minimum and maximum values, regex patterns, and more. 
3) model_validator(): A decorator that allows you to define custom validation logic for your Pydantic models. It can be used to enforce complex validation rules that cannot be expressed using the built-in field constraints.


> model_validator(mode="before") => This mode allows you to perform validation before the standard field validation occurs, coerces or instantiate from the class. It is useful for scenarios where you need to preprocess or transform the input data before it is validated against the model's fields. -> return / take the pure data as dict.
 
> model_validator(mode="after") => This mode allows you to perform validation after the standard field validation has occurred and coerces. It registers the method as part of the validation process of the data in pydantic. It is useful for scenarios where you need to perform additional checks or transformations on the validated data before it is returned or used in your application. -> return self. 


### Raising Errors
* Pydantic's validator documentation explicitly says that inside field_validator and model_validator, you should raise one of exactly three things for it to be treated as a validation failure: 
  - ValueError (and subclasses)
  - AssertionError (and subclasses) — this also covers plain assert statements
  - Pydantic's own internal PydanticCustomError (a more advanced option for custom error types/codes, less commonly needed)

 * It does not catch and wrap:

    - TypeError
    - KeyError
    - NameError
    - bare Exception
  basically anything else

**Bad way:** Could assume an error in your code not a validation error.
```python3
from pydantic import BaseModel, model_validator, ValidationError


class PlainError(Exception):
    """A normal Exception - NOT a ValueError subclass."""
    pass


class Item(BaseModel):
    name: str

    @model_validator(mode="after")
    def check(self) -> "Item":
        if self.name == "bad":
            raise PlainError("name cannot be 'bad'")
        return self


if __name__ == "__main__":
    try:
        Item(name="bad")
    except ValidationError as e:
        print("Caught as ValidationError:", e)
    except PlainError as e:
        print("Caught as PlainError (NOT wrapped by Pydantic):", e)
```


**Right way:** Catches only validation errors
```python3
from pydantic import BaseModel, model_validator, ValidationError


class GoodError(ValueError):
    """This IS a ValueError subclass."""
    pass


class Item2(BaseModel):
    name: str

    @model_validator(mode="after")
    def check(self) -> "Item2":
        if self.name == "bad":
            raise GoodError("name cannot be 'bad'")
        return self


if __name__ == "__main__":
    try:
        Item2(name="bad")
    except ValidationError as e:
        print("Caught as ValidationError:", e)
    except Exception as e:
        print("Caught as something else:", type(e), e)
```


