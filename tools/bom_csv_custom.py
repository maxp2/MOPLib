#The following text box shows in the KiCAD plugin manager
"""
    @package
    Custom KiCAD BOM exporter.
    Part of the MOPLib project. 
    More documentation is available there.
"""

# Import the KiCad python helper module and the csv formatter
import kicad_netlist_reader
import csv
import sys
import copy

# Generate an instance of a generic netlist, and load the netlist tree from
# the command line option. If the file doesn't exist, execution will stop
net = kicad_netlist_reader.netlist(sys.argv[1])

class BOM_component_t:
    
    def __init__(self):
        True
    def friendly_field_names(self):
        fields = [
        'Part ID'                 ,
        'Capacitance'             ,
        'Coupling'                ,
        'Dielectric'              ,
        'ESL'                     ,
        'ESR'                     ,
        'Footprint'               ,
        'Inductance'              ,
        'Impedance'               ,
        'Impedance Frequency'     ,
        'Manufacturer'            ,
        'Manufacturer Part Number',
        'Max Current'             ,
        'Is Installed'            ,
        'Multiplier'              ,
        'Note'                    ,
        'Power'                   ,
        'Design Quantity'         ,
        'Usage Quantity'          ,
        'Reference Designator'    ,
        'Resistance'              ,
        'Saturation Current'      ,
        'SRF'                     ,
        'Symbol Description'      ,
        'Symbol Library Name'     ,
        'Temperature Coefficient' ,
        'Tolerance'               ,
        'Value'                   ,
        'Voltage'                 ]
        return fields
    
    def to_dict(self):
        ret = {
        'Part ID'                   : self.part_ID                 ,
        'capacitance'               : self.capacitance             ,
        'coupling'                  : self.coupling                ,
        'dielectric'                : self.dielectric              ,
        'ESL'                       : self.ESL                     ,
        'ESR'                       : self.ESR                     ,
        'footprint'                 : self.footprint               ,
        'inductance'                : self.inductance              ,
        'impedance'                 : self.impedance               ,
        'impedance_frequency'       : self.impedance_frequency     ,
        'manufacturer'              : self.manufacturer            ,
        'manufacturer_part_number'  : self.manufacturer_part_number,
        'max_current'               : self.max_current             ,
        'Is Installed'              : self.is_installed            ,
        'multiplier'                : self.multiplier              ,
        'note'                      : self.note                    ,
        'power'                     : self.power                   ,
        'design_quantity'           : self.design_quantity         ,
        'usage_quantity'            : self.usage_quantity          ,
        'reference_designator'      : self.reference_designator    ,
        'resistance'                : self.resistance              ,
        'sat_current'               : self.sat_current             ,
        'SRF'                       : self.SRF                     ,
        'symbol_description'        : self.symbol_description      ,
        'symbol_lib_name'           : self.symbol_lib_name         ,
        'tempco'                    : self.tempco                  ,
        'tolerance'                 : self.tolerance               ,
        'value'                     : self.value                   ,
        'voltage'                   : self.voltage                 
        }
        return ret
    
    def to_CSV_row(self, delimiter):
        row =""
        row +=self.part_ID                       + delimiter
        row +=self.capacitance                   + delimiter
        row +=self.coupling                      + delimiter
        row +=self.dielectric                    + delimiter
        row +=self.ESL                           + delimiter
        row +=self.ESR                           + delimiter
        row +=self.footprint                     + delimiter
        row +=self.inductance                    + delimiter
        row +=self.impedance                     + delimiter
        row +=self.impedance_frequency           + delimiter
        row +=self.manufacturer                  + delimiter
        row +=self.manufacturer_part_number      + delimiter
        row +=self.max_current                   + delimiter
        row +=self.is_installed                  + delimiter
        row +=self.multiplier                    + delimiter
        row +=self.note                          + delimiter
        row +=self.power                         + delimiter
        row +=str(self.design_quantity         ) + delimiter
        row +=str(self.usage_quantity          ) + delimiter
        row +=self.reference_designator          + delimiter
        row +=self.resistance                    + delimiter
        row +=self.sat_current                   + delimiter
        row +=self.SRF                           + delimiter
        row +=self.symbol_description            + delimiter
        row +=self.symbol_lib_name               + delimiter
        row +=self.tempco                        + delimiter
        row +=self.tolerance                     + delimiter
        row +=self.value                         + delimiter
        row +=self.voltage                       + "\n"
        
    def from_KiCAD_component(self, component):
        self.part_ID                   = component.getField("Part ID")
        self.capacitance               = component.getField("Capacitance")
        self.coupling                  = component.getField("Coupling"   )
        self.dielectric                = component.getField("Dielectric" )
        self.ESL                       = component.getField("ESL"        )
        self.ESR                       = component.getField("ESR"        )
        self.footprint                 = component.getFootprint()
        self.inductance                = component.getField("Inductance"              )
        self.impedance                 = component.getField("Impedance"               )
        self.impedance_frequency       = component.getField("Impedance Frequency"     )
        self.manufacturer              = component.getField("Manufacturer"            )
        self.manufacturer_part_number  = component.getField("Manufacturer Part Number")
        self.max_current               = component.getField("Max Current"             )
        self.note                      = component.getField("Note"                    )
        self.power                     = component.getField("Power"                   )
        self.design_quantity           = 0
        self.usage_quantity            = 0
        self.reference_designator      = component.getRef()
        self.resistance                = component.getField("Resistance" )
        self.sat_current               = component.getField("Saturation Current")
        self.SRF                       = component.getField("SRF"        )
        self.symbol_description        = component.getDescription()
        self.symbol_lib_name           = component.getLibName()+":"+component.getPartName()
        self.tempco                    = component.getField("Temperature Coefficient"   )
        self.tolerance                 = component.getField("Tolerance")
        self.value                     = component.getValue()
        self.voltage                   = component.getField("Voltage")
        
        
        local_is_installed             = component.getField("Is Installed"            )
        local_is_installed = local_is_installed.strip()
        if ((local_is_installed == "") or (local_is_installed == "true") or (local_is_installed == "TRUE") or (local_is_installed == "True") or (local_is_installed == "yes") or (local_is_installed == "Yes") or (local_is_installed == "1") or (local_is_installed == "Y") or (local_is_installed == "y")):
            self.is_installed = True
        elif ((local_is_installed == "false") or (local_is_installed == "FALSE") or (local_is_installed == "False") or (local_is_installed == "no") or (local_is_installed == "No") or (local_is_installed == "0") or (local_is_installed == "N") or (local_is_installed == "n") or (local_is_installed == "DNP") or (local_is_installed == "DNI") or (local_is_installed == "NP")):
            self.is_installed = False
        else :
            # No error handling for bad input - script crashes
            raise ValueError
        
        local_multiplier               = component.getField("Multiplier"              )
        if (local_multiplier == ""):
            self.multiplier = 1
        else:
            # No error handling for bad input - script crashes
            self.multiplier = int(local_multiplier)
    
    # All except
    # - part_ID
    # - design_quantity
    # - usage_quantity
    # - reference_designator
    # - multiplier
    # The multiplier can represent whether a component is 
    # optional and thus considered a design detail
    def compare_design_data(self, BOM_component2):
        if(self.capacitance              != BOM_component2.capacitance              ): return False
        if(self.coupling                 != BOM_component2.coupling                 ): return False
        if(self.dielectric               != BOM_component2.dielectric               ): return False
        if(self.ESL                      != BOM_component2.ESL                      ): return False
        if(self.ESR                      != BOM_component2.ESR                      ): return False
        if(self.footprint                != BOM_component2.footprint                ): return False
        if(self.inductance               != BOM_component2.inductance               ): return False
        if(self.impedance                != BOM_component2.impedance                ): return False
        if(self.impedance_frequency      != BOM_component2.impedance_frequency      ): return False
        if(self.manufacturer             != BOM_component2.manufacturer             ): return False
        if(self.manufacturer_part_number != BOM_component2.manufacturer_part_number ): return False
        if(self.max_current              != BOM_component2.max_current              ): return False
        #if(self.note                     != BOM_component2.note                     ): return False
        if(self.power                    != BOM_component2.power                    ): return False
        if(self.resistance               != BOM_component2.resistance               ): return False
        if(self.sat_current              != BOM_component2.sat_current              ): return False
        if(self.SRF                      != BOM_component2.SRF                      ): return False
        if(self.symbol_description       != BOM_component2.symbol_description       ): return False
        if(self.symbol_lib_name          != BOM_component2.symbol_lib_name          ): return False
        if(self.tempco                   != BOM_component2.tempco                   ): return False
        if(self.tolerance                != BOM_component2.tolerance                ): return False
        if(self.value                    != BOM_component2.value                    ): return False
        if(self.voltage                  != BOM_component2.voltage                  ): return False
        
        if(self.is_installed == False and BOM_component2.is_installed != False): return False
        if(self.is_installed != False and BOM_component2.is_installed == False): return False
        
        return True
    
    # All except
    # - part_ID
    # - multiplier
    # - design_quantity
    # - usage_quantity
    # - note
    # - reference_designator
    # - symbol_description
    # - symbol_lib_name
    # - footprint
    def compare_part_data(self, BOM_component2):
        if(self.capacitance              != BOM_component2.capacitance              ): return False
        if(self.coupling                 != BOM_component2.coupling                 ): return False
        if(self.dielectric               != BOM_component2.dielectric               ): return False
        if(self.ESL                      != BOM_component2.ESL                      ): return False
        if(self.ESR                      != BOM_component2.ESR                      ): return False
        if(self.inductance               != BOM_component2.inductance               ): return False
        if(self.impedance                != BOM_component2.impedance                ): return False
        if(self.impedance_frequency      != BOM_component2.impedance_frequency      ): return False
        if(self.manufacturer             != BOM_component2.manufacturer             ): return False
        if(self.manufacturer_part_number != BOM_component2.manufacturer_part_number ): return False
        if(self.max_current              != BOM_component2.max_current              ): return False
        #if(self.note                     != BOM_component2.note                     ): return False
        if(self.power                    != BOM_component2.power                    ): return False
        if(self.resistance               != BOM_component2.resistance               ): return False
        if(self.sat_current              != BOM_component2.sat_current              ): return False
        if(self.SRF                      != BOM_component2.SRF                      ): return False
        if(self.tempco                   != BOM_component2.tempco                   ): return False
        if(self.tolerance                != BOM_component2.tolerance                ): return False
        if(self.value                    != BOM_component2.value                    ): return False
        if(self.voltage                  != BOM_component2.voltage                  ): return False
        
        return True

# Import
# grouped = net.groupComponents()
# original KiCAD list
Kcomps = net.getInterestingComponents()
# imported list
icomps = []
for index in range(0, len(Kcomps)):
    comp = BOM_component_t()
    comp.from_KiCAD_component(Kcomps[index])
    icomps.append(comp)

"""
print("import test:")
print(icomps[0].to_dict())

for comp in icomps:
    print("icomps:")
    print(comp.to_dict())
"""

# Find duplicates
# Deduplication algorithm
class duplicate_info_t:
    def __init__(self):
        self.is_duplicate = False
        self.duplicate_of = 0

# Generate duplicate info for components
# TODO (eventually) debate using wrapper object of 
# duplicate_info_t and BOM_component and sub-object 
# references rather than indices
# algorithm is no longer generic for object type
# Linkage is by index
duplicate_info = []
for index in range(0, len(icomps)):
    info = duplicate_info_t()
    duplicate_info.append(info)

for comp1i in range(0,len(icomps)):
    if (duplicate_info[comp1i].is_duplicate == True):
        continue
    for comp2i in range(0,len(icomps)):
        if (comp2i == comp1i):
            continue
        if (duplicate_info[comp2i].is_duplicate == True):
            continue
        if (icomps[comp1i].compare_design_data(icomps[comp2i])):
            duplicate_info[comp2i].is_duplicate = True
            duplicate_info[comp2i].duplicate_of = comp1i

# Merge / collect duplicates in a copy (do not directly 
# commit changes)
ddcomps = copy.deepcopy(icomps)
for compi in range(0, len(ddcomps)):
    if(ddcomps[compi].note.strip() != ""):
            ddcomps[compi].note = ddcomps[compi].reference_designator + " : "  + ddcomps[compi].note
    if (duplicate_info[compi].is_duplicate == False):
        ddcomps[compi].design_quantity += max(ddcomps[compi].multiplier,1)
        ddcomps[compi].usage_quantity  += ddcomps[compi].multiplier
    else:
        # Push to original / non-duplicate    
        # ddcomps[compi].quantity*local_multiplier is not 
        # correct - multiplier applies to a single component
        # instance
        if(ddcomps[compi].note.strip() != ""):
            ddcomps[duplicate_info[compi].duplicate_of].note += "\n" + ddcomps[compi].note
        ddcomps[duplicate_info[compi].duplicate_of].design_quantity += max(ddcomps[compi].multiplier,1)
        ddcomps[duplicate_info[compi].duplicate_of].usage_quantity  += ddcomps[compi].multiplier
        ddcomps[duplicate_info[compi].duplicate_of].reference_designator += ", " + ddcomps[compi].reference_designator

"""
for comp2i in range(0, len(ocomps)):
    if(type(ocomps[comp2i]) == str):
        continue
    elif(pcomp['manufacturer']                  == ocomps[comp2i].getField("manufacturer")
        and (pcomp['Manufacturer_Part_Number']  == ocomps[comp2i].getField("manufacturer_Part_Number"))
        and (pcomp['Multiplier']                == ocomps[comp2i].getField("multiplier"))
        and (pcomp['Value']                     == ocomps[comp2i].getValue())
        and (pcomp['Footprint']                 == ocomps[comp2i].getFootprint())
        and (pcomp['Symbol_Description'] == ocomps[comp2i].getDescription())):
        #Multiplier logic not yet implemented
        pcomp["quantity"] += 1
        pcomp["ref"]  += ", " + ocomps[comp2i].getRef()
        ocomps[comp2i] = ""  # Invalidate
pcomps.append(pcomp)
"""

# Open a file to write to, if the file cannot be opened output to stdout
# instead
try:
    f = open(sys.argv[2], 'w')
except IOError:
    e = "Can't open output file for writing: " + sys.argv[2]
    print(__file__, ":", e, sys.stderr)
    f = sys.stdout

# Create a new csv writer object to use as the output formatter
out = csv.writer(f, lineterminator='\n', delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)

# Output a set of rows for a header providing general information
out.writerow(['Source:', net.getSource()])
out.writerow(['Date:', net.getDate()])
out.writerow(['Tool:', net.getTool()])
out.writerow(['Generator:', sys.argv[0]])
out.writerow(['Component Count:', len(net.components)])
out.writerow(['Simplified BOM (merged components):'])
out.writerow(icomps[0].friendly_field_names())

# Print to BOM
for compi in range(0, len(ddcomps)):
    if (duplicate_info[compi].is_duplicate == False):
        out.writerow(list(ddcomps[compi].to_dict().values()))

out.writerow([''])
out.writerow([''])
out.writerow([''])
out.writerow([''])
out.writerow(['Flat BOM / Design Database:'])
out.writerow(icomps[0].friendly_field_names())
for comp in icomps:
    out.writerow(list(comp.to_dict().values()))

