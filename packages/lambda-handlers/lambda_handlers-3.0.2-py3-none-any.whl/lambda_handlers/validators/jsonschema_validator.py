"""A validator for jsonschema Schemas."""

from typing import Any, Dict, List, Tuple, Union
from collections import defaultdict

from lambda_handlers.errors import LambdaError
from lambda_handlers.validators.validator import Validator

try:
    import jsonschema
except ImportError:
    jsonschema = None

JSONSchemaInstance = Dict[str, Any]


class JSONSchemaValidator(Validator):
    """A Validator that uses jsonschema schemas."""

    def validate(
        self,
        instance,
        schema: JSONSchemaInstance,
    ) -> Tuple[Any, Union[Dict[str, Any], List[Any]]]:
        """Return the data and errors (if any) from validating `instance` against `schema`."""
        if not jsonschema:
            raise LambdaError('Required jsonschema dependency not found.')

        validator = jsonschema.Draft7Validator(schema)
        errors = sorted(validator.iter_errors(instance), key=lambda error: error.path)
        return instance, errors

    def format_errors(self, errors) -> List[Dict[str, Any]]:
        """Re-format the errors from JSONSchema."""
        path_errors: Dict[str, List[str]] = defaultdict(list)
        for error in errors:
            path_errors[error.path.pop()].append(error.message)

        return [{path: messages} for path, messages in path_errors.items()]
