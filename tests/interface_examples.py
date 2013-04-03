""" Test data for testing the protocol manager with interfaces. """


from traits.api import Any, Enum, HasTraits, implements, Interface


#### 'Power plugs' metaphor ###################################################

#### Protocols ################################################################

class UKStandard(Interface):
    pass

class EUStandard(Interface):
    pass

class JapanStandard(Interface):
    pass

class IraqStandard(Interface):
    pass

#### Implementations ##########################################################

class UKPlug(HasTraits):
    implements(UKStandard)

class EUPlug(HasTraits):
    implements(EUStandard)

class JapanPlug(HasTraits):
    implements(JapanStandard)

class IraqPlug(HasTraits):
    implements(IraqStandard)

class TravelPlug(HasTraits):

    mode = Enum(['Europe', 'Asia'])

#### Adapters #################################################################

class Adapter(HasTraits):
    adaptee = Any

class UKStandardToEUStandard(Adapter):
    implements(EUStandard)

class EUStandardToJapanStandard(Adapter):
    implements(JapanStandard)

class JapanStandardToIraqStandard(Adapter):
    implements(IraqStandard)

class EUStandardToIraqStandard(Adapter):
    implements(IraqStandard)

class UKStandardToJapanStandard(Adapter):
    implements(JapanStandard)

class TravelPlugToJapanStandard(Adapter):
    implements(JapanStandard)

class TravelPlugToEUStandard(Adapter):
    implements(EUStandard)


#### 'File, Editor, Printable' metaphor #######################################

class FileType(HasTraits):
    pass

class IEditor(Interface):
    pass

class ITextEditor(Interface):
    pass

class IPrintable(Interface):
    pass

class TextEditor(HasTraits):
    implements(ITextEditor)

class FileTypeToIEditor(Adapter, TextEditor):
    implements(IEditor)

class ITextEditorToIPrintable(Adapter):
    implements(IPrintable)

#### EOF ######################################################################
