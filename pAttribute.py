'''
Attribute will track and manage all data with-in an attribute
'''
import pObject as pObject

class PAttribute(pObject.PObject):
    '''
    Base Attribute to manage all data for nodes
    '''
    #All the attribute types usable by this class.
    __attrTypes__ = (bool, basestring, str, int, float, list, tuple)

    @staticmethod
    def isValid(attribute):
        '''
        Check to see if the attribute is a valid type or not.

        :param attribute: Attribute to check
        :type attribute: Attribute | anything else
        '''
        if not isinstance(attribute, PAttribute):
            return False
        
        return True
    
    @staticmethod
    def inValidError(attribute):
        '''
        Error message for the attribute passed in.

        :param attribute: Attribute to run the error message against.
        :type attribute: anything other then Attribute
        '''
        raise TypeError("{0} is not of type attribute.Attribute".format(attribute))
    
    def __init__(self, longName = None, shortName = None, attrType = None, value = None):
        '''
        The constructor method for this attribute.

        :param longName: Name of the attribute.
        :type longName: str

        :param shortName: Short name for the attribute, usually two letters.
        :type shortName: str

        :param attrType: The type of attribute to set this object to.
        :type attrType: str

        :param value: The value to make the attribute.
        :param value: bool | basestring | str | int | float | list | tuple
        '''
        super(PAttribute, self).__init__(longName)
        self._shortName   = shortName
        self._value       = value
        self._storable    = True
        self._connectable = True
        if not attrType:
            self._type = type(self._value).__name__
        else:
            self._type = attrType

    #{ GET
    def getType(self):
        '''Returns the type of attribute. '''
        return self._type
    
    def getShortName(self):
        '''
        Returns the short name for this attribute.
        '''
        return self._shortName

    def getValue(self):
        '''
        Returns the value of the attribute.
        '''
        return self._value

    #{ SET
    def setStorable(self, value):
        '''
        Sets whether or not this attribute 
        is able to be saved.

        :param value: Value to make this storable
        :type value: bool
        '''
        self._storable = self._setBool(value)
        
    def setConnectable(self, value):
        '''
        Sets whether or not this attribute 
        is able to be connected to.

        :param value: Value to make this connectable or not
        :type value: bool
        '''
        self._connectable = self._setBool(value)

    def setValue(self, value):
        '''
        This will set the value of this attribute based on the type of attribute it is.
        If the value passed in does not match the type of the attribute, then there will
        be an error raised.

        :param value: Value to set the attribute to.
        :type value: bool | basestring | str | int | float | list | tuple
        '''
        if not type(value).__name__ not in self.__attrTypes__:
            raise TypeError('{0} needs to be one of the following types: {1}'.format(value, self.__attrTypes__))
        
        #build the command
        if isinstance(value, basestring):
            cmd = "self._set{0}('{1}')".format(type(value).__name__.title(), value)
        else:
            cmd = 'self._set{0}({1})'.format(type(value).__name__.title(), value)
            
        #execute the command
        value = eval(cmd)
        
        self._value = value #set the value

    def _setBool(self, value):
        '''
        Set the value to be bool.

        :param value: Value to set/convert to a bool.
        :type value: bool | int
        '''
        if not isinstance(value, (bool,int)):
            raise TypeError("{0} must be <type 'bool'>".format(value))
        
        if value:
            return True
        
        return False 
    
    def _setStr(self, value):
        '''
        Set the value to be string.

        :param value: Value to set/convert to a bool.
        :type value: str
        '''
        if not isinstance(value, basestring):
            raise TypeError("{0} must be <type 'str'>".format(value))

        return str(value)
    
    def _setFloat(self, value):
        '''
        Set the value to be float.

        :param value: Value to set/convert to a int.
        :type value: int | str | float
        '''
        if not isinstance(value, (float,int,basestring)):
            raise TypeError("{0} must be <type 'float'>".format(value))
        
        return float(value)
    
    def _setInt(self, value):
        '''
        Set the value to be int.

        :param value: Value to set/convert to a int.
        :type value: int | str | float
        '''
        if not isinstance(value, (int,basestring,float)):
            raise TypeError("{0} must be <type 'int'>".format(value))
        
        return int(value)
    
    def _setList(self, value):
        '''
        Set the value to be list.

        :param value: Value to set/convert to a list.
        :type value: tuple | list
        '''
        if not isinstance(value, (list,tuple)):
            raise TypeError("{0} must be <type 'list'>".format(value))

        return list(value)
    
    def _setTuple(self, value):
        '''
        Set the value to be tuple.

        :param value: Value to set/convert to a tuple.
        :type value: tuple | list
        '''
        if not isinstance(value, (tuple,list)):
            raise TypeError("{0} must be <type 'tuple'>".format(value))

        return tuple(value)

    #{ CHECKS
    def isStorable(self):
        '''Returns whether the attribute is storable, meaning can be saved.'''
        return self._storable

    def isConnectable(self):
        '''Returns whether the attribute is connectable.'''
        return self._connectable
    
    #{ MISC
    def create(self, longName, shortName, attrType, value):
        if not attrType in PAttribute.__attrTypes__:
            raise TypeError('{0} must be one of the following types: {1}'.format(attrType, str(*PAttribute.__attrTypes__)))
        
        self.setName(longName)
        self._shortName = shortName
        self._type      = attrType
        self.setValue(value)