__author__ = "Martin Larralde <martin.larralde@embl.de>"
__license__ = "MIT"
__version__ = (
    __import__("pkg_resources")
    .resource_string(__name__, "_version.txt")
    .decode("utf-8")
    .strip()
)

from .utils import warnings
from .entity import Entity
from .definition import Definition
from .metadata import Metadata, Subset
from .ontology import Ontology
from .pv import LiteralPropertyValue, PropertyValue, ResourcePropertyValue
from .relationship import Relationship, RelationshipData
from .synonym import Synonym, SynonymData, SynonymType
from .term import Term, TermData
from .xref import Xref

__all__ = [
    # modules
    "warnings",
    # classes
    Ontology.__name__,
    Entity.__name__,
    Term.__name__,
    TermData.__name__,
    Metadata.__name__,
    Subset.__name__,
    Definition.__name__,
    Relationship.__name__,
    RelationshipData.__name__,
    Synonym.__name__,
    SynonymData.__name__,
    SynonymType.__name__,
    PropertyValue.__name__,
    LiteralPropertyValue.__name__,
    ResourcePropertyValue.__name__,
    Xref.__name__,
]
