#The following text box shows in the KiCAD plugin manager
"""
    @package
    Generate a CSV formatted BOM.
    Originally based on bom_csv_grouped_by_value_with_fp.py
    Components are sorted by ref and grouped by value and footprint
    Fields are (if they exist):
    'Ref', 'Qnty', 'Manufacturer', 'Part_Number', 'Description', 
    'Value', 'Footprint', 'Cmp name'
    
    It is recommended to add the custom fields 
    'Manufacturer', 'Part_Number', 'Multiplier'
    to the KiCAD custom field settings
    This script converts (TODO implementation) the multiplier 
    field is cast from text to an integer based on the following rules
    ◦ Empty ("") → 1
    ◦ NP → 0
    ◦ DNI → 0
    ◦ DNP → 0
    ◦ Integer → 1xinteger
    
    Script last tested 2022-07-19 in KiCAD 5.1.8 release build
    
    Requires kicad_netlist_reader.py which ships with KiCAD.
    This can be copied or symlinked to the script directory.
    
    Command line (OpenSUSE Leap 15.4 tested):
    python3 "pathToFile/bom_csv_custom.py" "%I" "%O"_BOM.csv
"""

# Import the KiCad python helper module and the csv formatter
import kicad_netlist_reader
import csv
import sys

# Generate an instance of a generic netlist, and load the netlist tree from
# the command line option. If the file doesn't exist, execution will stop
net = kicad_netlist_reader.netlist(sys.argv[1])

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
index_row = ['Ref', 'Qnty', 'Multiplier', 'Manufacturer', 'Manufacturer_Part_Number', 'Value', 'Footprint', 'Symbol_Lib:Name', 'Symbol_Description']
out.writerow(index_row)

# grouped = net.groupComponents()
# Original components list
ocomps = net.getInterestingComponents()
# Components list for printing
pcomps = []

# First pass - Format data and group based on hard coded criteria
for comp1i in range(0, len(ocomps)):
    if(type(ocomps[comp1i]) == str):
        continue
    else:
        # Import to a useful dict
        pcomp = {'Ref': ocomps[comp1i].getRef(),
            'Qnty': 1,
            'Multiplier': ocomps[comp1i].getField("Multiplier"),
            'Manufacturer': ocomps[comp1i].getField("Manufacturer"),
            'Manufacturer_Part_Number': ocomps[comp1i].getField("Manufacturer_Part_Number"),
            'Value': ocomps[comp1i].getValue(),
            'Footprint': ocomps[comp1i].getFootprint(),
            'Symbol_Lib:Name': ocomps[comp1i].getLibName()+":"+ocomps[comp1i].getPartName(),
            'Symbol_Description': ocomps[comp1i].getDescription()}
        
        ocomps[comp1i] = ""  # Invalidate before duplicate search
        
        # Deduplication loop
        for comp2i in range(0, len(ocomps)):
            if(type(ocomps[comp2i]) == str):
                continue
            elif(pcomp['Manufacturer']                  == ocomps[comp2i].getField("Manufacturer")
                and (pcomp['Manufacturer_Part_Number']  == ocomps[comp2i].getField("Manufacturer_Part_Number"))
                and (pcomp['Multiplier']                == ocomps[comp2i].getField("Multiplier"))
                and (pcomp['Value']                     == ocomps[comp2i].getValue())
                and (pcomp['Footprint']                 == ocomps[comp2i].getFootprint())
                and (pcomp['Symbol_Description'] == ocomps[comp2i].getDescription())):
                #Multiplier logic not yet implemented
                pcomp["Qnty"] += 1
                pcomp["Ref"]  += ", " + ocomps[comp2i].getRef()
                ocomps[comp2i] = ""  # Invalidate
        pcomps.append(pcomp)

# Second pass - Output all of the component information to the file
for pcomp in pcomps:
    out.writerow(list(pcomp.values()))
