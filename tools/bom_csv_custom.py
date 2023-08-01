#The following text box shows in the KiCAD plugin manager
"""
    @package
    Custom KiCAD BOM exporter.
    - CSV formatted
    - Dual flat BOM and deduplicated BOM
    
    Originally based on bom_csv_grouped_by_value_with_fp.py
    Components are sorted by ref and grouped by value and footprint
    
    This exporter supports the following custom fields in 
    KiCAD in addition to some normal KiCAD fields. 
    It is recommended to add them to the KiCAD custom
    field settings.
    
    - 'capacitance'             
    - 'coupling'                
    - 'dielectric'              
    - 'ESL'                     
    - 'ESR'                     
    - 'footprint'               
    - 'inductance'              
    - 'impedance'               
    - 'impedance_frequency'     
    - 'manufacturer'            
    - 'manufacturer_part_number'
    - 'max_current'             
    - 'multiplier'              
    - 'note'                    
    - 'power'                   
    - 'resistance'              
    - 'sat_current'             
    - 'SRF'                     
    - 'tempco'                  
    - 'tolerance'               
    - 'voltage'                 
    
    Overall, the exported data includes:
    'capacitance'             
    'coupling'                
    'dielectric'              
    'ESL'                     
    'ESR'                     
    'footprint'               
    'inductance'              
    'impedance'               
    'impedance_frequency'     
    'manufacturer'            
    'manufacturer_part_number'
    'max_current'             
    'multiplier'              
    'note'                    
    'power'                   
    'quantity'                
    'reference_designator'    
    'resistance'              
    'sat_current'             
    'SRF'                     
    'symbol_description'      
    'symbol_lib_name'         
    'tempco'                  
    'tolerance'               
    'value'                   
    'voltage'                 
    
    The 'multiplier' field is a a BOM quantity multiplier
    and not a design multiplier. Some CAD tools support 
    design multipliers ("block instances") but typically 
    assign unique reference designators to each subcomponent 
    of each instance.
    
    This script converts the multiplier from text to an 
    integer based on the following rules:
    ◦ Empty ("") → 1
    ◦ NP → 0
    ◦ DNI → 0
    ◦ DNP → 0
    ◦ Integer → 1xinteger
    
    Since multiplier is annoted for a single design 
    component, the total number of components after 
    deduplication is then the sum of the multipliers.
    
    Script last tested 2023-08-01 in KiCAD 5.1.8 release 
    build
    
    Requires kicad_netlist_reader.py which ships with KiCAD.
    This can be copied or symlinked to the script directory.
    
    Command line (OpenSUSE Leap 15.4 tested):
    python3 "pathToFile/bom_csv_custom.py" "%I" "%O"_BOM.csv
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
        'Multiplier'              ,
        'Note'                    ,
        'Power'                   ,
        'Quantity'                ,
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
        'multiplier'                : self.multiplier              ,
        'note'                      : self.note                    ,
        'power'                     : self.power                   ,
        'quantity'                  : self.quantity                ,
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
        row +=self.multiplier                    + delimiter
        row +=self.note                          + delimiter
        row +=self.power                         + delimiter
        row +=str(self.quantity                ) + delimiter
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
        self.capacitance               = component.getField("capacitance")
        self.coupling                  = component.getField("coupling"   )
        self.dielectric                = component.getField("dielectric" )
        self.ESL                       = component.getField("ESL"        )
        self.ESR                       = component.getField("ESR"        )
        self.footprint                 = component.getFootprint()
        self.inductance                = component.getField("inductance"              )
        self.impedance                 = component.getField("impedance"               )
        self.impedance_frequency       = component.getField("impedance_frequency"     )
        self.manufacturer              = component.getField("manufacturer"            )
        self.manufacturer_part_number  = component.getField("manufacturer_part_number")
        self.max_current               = component.getField("max_current"             )
        self.note                      = component.getField("note"                    )
        self.power                     = component.getField("power"                   )
        self.quantity                  = 1
        self.reference_designator      = component.getRef()
        self.resistance                = component.getField("resistance" )
        self.sat_current               = component.getField("sat_current")
        self.SRF                       = component.getField("SRF"        )
        self.symbol_description        = component.getDescription()
        self.symbol_lib_name           = component.getLibName()+":"+component.getPartName()
        self.tempco                    = component.getField("tempco"   )
        self.tolerance                 = component.getField("tolerance")
        self.value                     = component.getValue()
        self.voltage                   = component.getField("voltage")
        
        
        local_multiplier               = component.getField("multiplier"              )
        if (local_multiplier == ""):
            self.multiplier = 1
        elif (local_multiplier == "DNP"):
            self.multiplier = 0
        elif (local_multiplier == "DNI"):
            self.multiplier = 0
        elif (local_multiplier == "NP"):
            self.multiplier = 0
        else :
            # No error handling for bad input - script crashes
            self.multiplier = int(local_multiplier)
    
    # All except
    # - quantity
    # - reference_designator
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
        if(self.note                     != BOM_component2.note                     ): return False
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
        
        if(self.multiplier == 0 and BOM_component2.multiplier != 0): return False
        if(self.multiplier != 0 and BOM_component2.multiplier == 0): return False
        
        return True
    
    # All except
    # - multiplier
    # - quantity
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
        if(self.note                     != BOM_component2.note                     ): return False
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
    if (duplicate_info[compi].is_duplicate == True):
        # Push to original / non-duplicate    
        # ddcomps[compi].quantity*local_multiplier is not 
        # correct - multiplier applies to a single component
        # instance
        
        if (ddcomps[compi].multiplier == 0):
            local_multiplier = 1
        else:
            local_multiplier = ddcomps[compi].multiplier
        ddcomps[duplicate_info[compi].duplicate_of].quantity += local_multiplier
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

