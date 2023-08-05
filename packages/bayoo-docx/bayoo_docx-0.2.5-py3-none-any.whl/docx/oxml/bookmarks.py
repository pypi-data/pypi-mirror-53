from . import OxmlElement

from .simpletypes import ST_String 
from .xmlchemy import (
    BaseOxmlElement, RequiredAttribute
)



class CT_BookmarkStart(BaseOxmlElement):
    """
    A ``<w:bookmarkStart>`` element, a container for Footnotes properties 
    """

    id   = RequiredAttribute('w:id'  , ST_String)
    name = RequiredAttribute('w:name', ST_String)

    @classmethod
    def new(cls, idy, name):
        start = OxmlElement('w:bookmarkStart')
        start.id   = idy
        start.name = name

        return start

class CT_BookmarkEnd(BaseOxmlElement):
    """
    A ``<w:bookmarkEnd>`` element, a container for Footnotes properties 
    """
    id = RequiredAttribute('w:id', ST_String)
    
    @classmethod
    def new(cls, idy):
        end = OxmlElement('w:bookmarkEnd')
        end.id = idy
        
        return end