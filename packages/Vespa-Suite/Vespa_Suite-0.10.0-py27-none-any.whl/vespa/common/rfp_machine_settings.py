# Python modules
from __future__ import division
import xml.etree.cElementTree as ElementTree


# 3rd party modules


# Our modules
import vespa.common.constants as constants
import vespa.common.util.xml_ as util_xml

from vespa.common.constants import Deflate


#1234567890123456789012345678901234567890123456789012345678901234567890123456789

def settings_from_template(template):
    """
    Given a MachineSettingsTemplate instance, returns a new MachineSettings
    instance containing values copied from the template.
    """
    # Express the template as a dict
    d = template.deflate(Deflate.DICTIONARY)
    
    # Delete a few template-specific attributes
    for attribute in ("id", "name"):
        del d[attribute]

    # Turn that into a machine settings object   
    return MachineSettings(d)


class MachineSettings(object):
    """
    Settings related to the targeted physical MRI machine.
    """
    # The XML_VERSION enables us to change the XML output format in the future 
    XML_VERSION = "1.0.0"

    def __init__(self, attributes=None):
        self.id                     = 0
        # machine_type can be from constants.MachineTypes but the user is also
        # allowed to enter & save freeform text when creating a template, so
        # don't assume that machine_type will always be one of the
        # elements of constants.MachineType.
        self.machine_type           = constants.MachineType.SIEMENS
        
        # These constants are not used in practice. Most (all?) code that needs
        # a new machine settings objects initializes it with the settings from
        # the default template in the database.
        self.field_strength         = 3.0   # 1.5,3,4,7 etc. Tesla
        self.max_b1_field           = 22    # in microTesla
        self.zero_padding           = 0
        self.min_dwell_time         = 1.0   # micro-seconds
        self.dwell_time_increment   = 0.2   # micro-seconds
        self.gradient_raster_time   = 10.0   # e.g. 5 microSeconds for some Siemens machines.
        self.gradient_slew_rate     = 200.0 # In units of (milliTesla/meter)/millisecond
                                            # or equivalently (Tesla/meter)/second
        self.gradient_maximum       = 24.0  # In units of mT/meter

        if attributes is not None:
            self.inflate(attributes)


    def __str__(self):
        return self.__unicode__().encode("utf-8")


    def __unicode__(self):
        lines = [ ]
        
        lines.append("--- Machine Settings %d ---" % self.id)
        if self.machine_type in constants.MachineType.ALL:
            machine_type = self.machine_type["display"]
        else:
            machine_type = self.machine_type
        lines.append("Machine type: %s" % machine_type)
        lines.append("Field Strength: %f" % self.field_strength)
        lines.append("Max B1 Field: %f" % self.max_b1_field)
        lines.append("Zero padding: %d" % self.zero_padding)
        lines.append("Min dwell time: %f" % self.min_dwell_time)
        lines.append("Dwell time increment: %f" % self.dwell_time_increment)
        lines.append("Gradient raster time: %f" % self.gradient_raster_time)
        lines.append("Gradient slew rate: %f" % self.gradient_slew_rate)
        lines.append("Gradient maximum: %f" % self.gradient_maximum)
        
        # __unicode__() must return a Unicode object.
        return u'\n'.join(lines)


    def as_html(self):
        """Returns this object rendered as HTML in an ElementTree.Element. The
        HTML is suitable for display in a wx.html control."""
        # To generate HTML, we cheat a bit and just modify the unicode
        # output.
        lines = unicode(self).split("\n")
        
        # We discard the first line header
        lines = lines[1:]
        
        # Split each line at the colon
        lines = [line.split(":") for line in lines]
        
        table = ElementTree.Element("table", {"border" : "1px"})
        tbody = ElementTree.SubElement(table, "tbody")

        for line in lines:
            description, data = line
            tr = ElementTree.SubElement(tbody, "tr")
            util_xml.TextSubElement(tr, "td", description)
            util_xml.TextSubElement(tr, "td", data, { "align" : "right" })

        return table


    def deflate(self, flavor=Deflate.ETREE):
        if flavor == Deflate.ETREE:
            # mse = machine settings element
            mse = ElementTree.Element("machine_settings",
                                      {"version" : self.XML_VERSION})
                
            machine_type = self.machine_type                      
            if machine_type in constants.MachineType.ALL:
                machine_type = machine_type["db"]

            util_xml.TextSubElement(mse, "machine_type", machine_type)

            for attribute in ("field_strength", 
                              "max_b1_field", 
                              "zero_padding", 
                              "min_dwell_time", 
                              "dwell_time_increment", 
                              "gradient_raster_time",
                              "gradient_slew_rate", 
                              "gradient_maximum",):
                util_xml.TextSubElement(mse, attribute, getattr(self, attribute))

            return mse
        elif flavor == Deflate.DICTIONARY:
            return self.__dict__.copy()


    def inflate(self, source):

        if hasattr(source, "makeelement"):
            # Quacks like an ElementTree.Element
            type_ = source.findtext("machine_type")
            if constants.MachineType.get_type_for_value(type_, "db"):
                type_ = constants.MachineType.get_type_for_value(type_, "db")                
            self.machine_type = type_
            for attribute in ("field_strength", 
                              "max_b1_field", 
                              "zero_padding", 
                              "min_dwell_time", 
                              "dwell_time_increment", 
                              "gradient_raster_time",
                              "gradient_slew_rate", 
                              "gradient_maximum", ):
                setattr(self, attribute, float(source.findtext(attribute)))
                
            # zero padding must be an int
            self.zero_padding = int(self.zero_padding)

        elif hasattr(source, "keys"):
            # Quacks like a dict
            for key in source.keys():
                if hasattr(self, key):
                    setattr(self, key, source[key])

            machine_type = source["machine_type"]
            # Attempt to convert machine_type to a proper constant
            machine_type = constants.MachineType.get_type_for_value(machine_type, 'db')
            if machine_type:
                self.machine_type = machine_type
            else:
                # Conversion failed; apparently the machine_type is free form
                self.machine_type = source["machine_type"]                        


class MachineSettingsTemplate(MachineSettings):
    """
    Templates are very similar to MachineSettings (q.v.) but are used
    slightly differently in the application. Each template has a unique name.
    """
    # The XML_VERSION enables us to change the XML output format in the future 
    XML_VERSION = "1.0.0"

    def __init__(self, attributes=None):
        
        MachineSettings.__init__(self, attributes)
        
        self.name = ""
        self.is_default = False

        if attributes is not None:
            self.inflate(attributes)


    def __str__(self):
        return self.__unicode__().encode("utf-8")


    def __unicode__(self):
        # Start with the base class' version
        lines = MachineSettings.__unicode__(self).split("\n")
        
        # Replace the header line & add default info.
        template_lines = ["--- Machine Settings Template %d ---" % self.id]
        template_lines.append("Default: %s" % ("True" if self.is_default else "False"))

        lines = template_lines + lines[1:]
        
        # __unicode__() must return a Unicode object.
        return u'\n'.join(lines)
  
  
    def deflate(self, flavor=Deflate.ETREE):
        # I start by getting my base class to deflate itself, then I append
        # the values specific to this class.
        base = MachineSettings.deflate(self, flavor)
        if flavor == Deflate.ETREE:
            util_xml.TextSubElement(base, "name", self.name)
            # is_default is specific to our GUI/app and so does not get exported

            return base
        elif flavor == Deflate.DICTIONARY:
            base.update(self.__dict__)
            return base

    def inflate(self, source):
        # I start by getting my base class to inflate itself, then I read
        # the values specific to this class.
        base = MachineSettings.inflate(self, source)

        if hasattr(source, "makeelement"):
            # Quacks like an ElementTree.Element
            self.name = source.findtext("name")
        elif hasattr(source, "keys"):
            # Quacks like a dict
            for attribute in ("name", "is_default"):
                if attribute in source:
                    setattr(self, attribute, source[attribute])


