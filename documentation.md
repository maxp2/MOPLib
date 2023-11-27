# Description

Managed Open Parts Library (MOPLib)

Previously named Generic High Energy Physics Parts Library (GHEPlib).

This is a CAD data library with support for multiple CAD 
tools.

Not to be confused with Seeed Studio's Open Parts Library

# Objectives

-   Multi-CAD tool support
-   Data reuse where reasonable
-   Quality control: revision controlled, standards 
    compliant, production
    tested
-   Uniform look, size, and style across CAD tools
-   User friendly: good-looking, paper print readable, publication
    ready, documented
-   Low coupling with optimization for different use cases (design
    density, formatting preferences, etc.)
-   Wide manufacturing technology support

# Related Tools and Standards

- https://www.footprintku.com/Home
- https://www.snapeda.com/home/
- https://octopart.com/
- https://www.jedec.org/category/technology-focus-area/jep30

# Dependencies

- Supported CAD tools
  - Siemens PADS VX2.3 or higher
  - Siemens DxDesigner (assumed import ability from PADS)
  - Altium Designer 23 or newer (tested)
  - KiCAD
- Python 3 (Legacy)
  - For management tools
- GCC
  - For management tools
- SQLite
- Qrbot (Android, optional but recommended tool for barcoding)

# Used On

-   Caribou v2 project
-   Internal (confidential) projects at contributor sites

# Primary Developers

-   Brookhaven National Laboratory
-   Carleton University Particle Physics Instrumentation Group

# Installation Instructions

## General Tips

All CAD tools require copying the repository to an accessible location.
It is recommended to choose a central location with no spaces in the path name.

For example when admin/root priviliedges are available:

- "C:\lib\MOPLib"
- "/opt/MOPLib"
- "/usr/local/lib64/MOPLib"
- "/usr/local/lib/MOPLib"
- "/lib/MOPLib"
- "/lib64/MOPLib"

## Siemens

Setup -> Settings -> Project -> Symbol Libraries

Alternately, the .prj file can be edited directly:

```
LIST IndependentLibraries
VALUE "DIR [W] . (symbols)"
VALUE "DIR [R] ${SDD_HOME}\Libraries\xDX_Designer\SymbolLibrary\Globals (Globals)"
[...]
VALUE "DIR [W] C:\lib\MOPLib\Siemens\custom (MOPLib_custom)"
VALUE "DIR [R] C:\lib\MOPLib\Siemens\borders (MOPLib_borders)"
VALUE "DIR [R] C:\lib\MOPLib\Siemens\mfg_import (MOPLib_mfg_import)"
VALUE "DIR [W] C:\lib\MOPLib\Siemens\mfg_mod (MOPLib_mfg_mod)"
ENDLIST
```

TODO DxDatabook integration

## KiCAD (version 5)

It is recommended to add the library as a global library:

Preferences -> Manage Symbol Libraries...
Preferences -> Manage Footprint Libraries...

Alternately, directly edit the text files:

~.config/kicad/sym-lib-table

TODO example

~.config/kicad/fp-lib-table

TODO example

# Porting Designs

This is needed anytime the library name changes or 
for older designs which are meant to transition to this library.

## Siemens

#. Change symbol names to those that are desired from the library
#. Tools -> Update Library Partitions...

## KiCAD

#. Clever text based search and replacements can be done on the schematic and layout files

# Management Instructions

Use dbeaver. See any entry as an example.

# Table Descriptions

Primary keys in each table are indicated with "PK"

-   CAD_table
    -   Relates parts to the **preferred** CAD files. A single part can
        have many CAD models or data files but only a few are preferred
        and/or tested.
    -   MFG = Manufacturer
    -   PN = Part Number. This is the primary manufacturer part number
        (not distributor, not internal)
    -   All symbols, footprints, and simulation models are references to
        CAD files in the Data_table
-   Data_table
    -   path: This can be a path to a file or a section of a file.
        -   If this refers to sections of a file, identifiers relevant
            to each CAD tool should be used.
        -   Symbols recognized by the CAD tool can be used. This is
            useful for default libraries.
    -   author: The most recent editor of the data. As soon as the data
        or a file is modified, the author is considered to have changed.
        This is for liability tracing
    -   release_version:
        -   If a default library is used, the exact release version
            should be indicated.
        -   If a file was directly downloaded from a manufacturer, the
            date of the download should be indicated.
    -   sym_group:
        -   Some parts are best represented by multiple separate
            symbols. This indicates that they should be grouped
            together.
    -   deployment_history: A short description of the harshest
        environmental deployment that the design within the file has
        survived. Examples include "not deployed", "functional",
        "functional after shock and vibration testing...", "functional
        after high temperature testing..."

## Database Integrity

By default, SQLite doesn't have Foreign Key constraints enabled.

They were enable with:

```
PRAGMA foreign_keys = ON;
```

No good method found to automatically ensure UUID 
uniqueness in the database directly via the SQLite database 
structure.

A (64 bit integer) UUID can be generated with the following 
SQL for SQlite:

```
select max(parts.UUID), max(CAD_data.UUID)+1 from parts, CAD_data;
select max(max(parts.UUID), max(CAD_data.UUID))+1 from parts, CAD_data;
```

## Useful SQL Queries

```
select 'BOM ID', UUID from parts where (manufacturer_part_number0 = "CRF0805-FZ-R020ELF") or (manufacturer_part_number1 = "CRF0805-FZ-R020ELF") or (manufacturer_part_number2 = "CRF0805-FZ-R020ELF");
```

```BOM ID``` is to be entered for reference to a spreadsheet 

General lookup: 

```
select UUID, manufacturer, manufacturer_part_number0 from parts where 
(UUID = 1532) or
(UUID = 1716) or
...
```


# IP Control

Most content is open source but some confidential information
is inevitable

- Confidential files are stored in dedicated folders and 
  subfolders
  - The existence of files and filenames are always 
    considered non-confidential. Database linking is thus 
    allowed and "tree" file lists are allowed.
  - May be moved to non confidential after this is approved 
    by the manufacturer and this is indicated in the database
- Users can gain access to confidential section with an NDA
  and must be very careful to recognize when information 
  is transferred between the database an a non-confidential area.
  For example, pin numbering from a confidential datasheet
  will be added to the symbol. 
  The symbol may be cached by the project so the project 
  must become confidential.
  It is possible to omit pin numbering for exported PDFs 
  so only the source project remains confidential.

## License

-   See License File
-   Data can be imported from manufacturers into this library only if
    that data is accompanied by a waiver of ownership (stated as "free
    to use for any purpose including sale and open source")
-   Imported data without modification is kept in separate import
    libraries. If data is modified or customized, it should first be
    copied to the custom libraries. The indicated author should also
    change.

## Directory Structure

.
├── Altium
│   ├── custom
│   ├── document_templates
│   └── test_project
├── FreeCAD
│   └── custom
├── golden_BOMs
├── KiCAD
│   ├── custom : full custom by library authors
│   ├── import_variant : import from any external source with modifications
│   ├── mfg_import : direct import from part manufacturers (no changes)
│   └── SnapEDA_import : direct import from SnapEDA (no changes)
├── LTSPice : models
├── mechanical
│   └── custom : fully custom by library authors
├── mfg_supplied : source CAD data that was supplied by manufacturers (any format) 
├── ngspice : models
├── part_specs
├── pin_numbering
├── PSpice : models
├── Siemens : DxDesigner
│   ├── borders
│   ├── custom : fully custom by library authors
│   ├── golden_symbols : known good symbols from legacy projects
│   ├── mfg_import : direct import from manufacturers (no changes)
│   ├── mfg_mod : import from external sources with modifications
│   └── test_project
├── SnapEDA_supplied : source CAD data as provided by SnapEDA
└── tools

# ECAD Conventions 
These are necessary for BOM exporter compatibility
KiCAD:
    1. Custom Fields:
        1. “Part_Number”
            1. Set Value = “PN” when this is used
            2. In general should never be empty unless parts are sourced at construction.
        2. “Manufacturer”
            1. In general should never be empty unless parts are sourced at construction.
            2. “Manufacturer”;”Part_Number” are the primary lookup key in the parts database
        3. “BOM_Multiplier”
            1. Supported aliases: “DNP” = 0 = “DNI”
            2. Supported aliases: “ ” (blank) = 1. This is per standard 1 Refdes per part convention
            3. For other CAD tools, may or may not have native multi-component / arrayed Refdes support
            4. May be fractional (e.g. ¼, ½ ) for ganged parts (subject to how CAD tool handles this)
        4. “Layout_Multiplier”
            1. Supported aliases: “DNL” = 0, “ ” (blank) = “1”
            2. For CAD tools which do not have native layout omission.
    2. Use fiducial place holders for connection-less additional BOM items (gender adapters, screws, mechanical items, if mechanical items are stored in electrical schematics for the given project)
    3. Use resistors and proper connectivity for placeholders of additional BOM items that can be represented as parasitics: pin inserts, wires, etc.

# Inventory Integration

Some options:

https://alternativeto.net/software/inventree/about/
https://alternativeto.net/software/partbolt/about/
https://alternativeto.net/software/partsbox/about/
https://alternativeto.net/software/axt-parts/about/
https://alternativeto.net/software/snipe-it/about/
https://alternativeto.net/software/storedown/about/
https://alternativeto.net/software/part-db/about/
https://alternativeto.net/software/bomist/about/
https://alternativeto.net/software/partkeepr/about/

Top options are InvenTree and PartKeepr

# Planned Work / TODO

- BOM exporter
  - implement merging of components with notes
  - implement new "construction" property applicable to resistors (wirewound, thin film, thick film, etc.)
  - Dual pretty and field names in column titles for quick editing
  - Change to new multiplier strategy (BOM, schematic and/or layout)
  - (s) on Ref designators


# Conventions

## Pin Mapping for CAD Data Reuse / "Generic Parts"

There are multiple ways to handle generic symbols and footprints:

-   part + generic symbol + pin remapped footprints
    -   E.g. PART_NUM, BJT, SOT23_123
    -   In practice this is very challenging to manage
-   part + pin remapped symbol + footprint
    -   E.g. PART_NUM, BJT_123, SOT23
-   part + generic symbol + generic footprint + pin map file to
    associate pin numbers, pin names, or pin IDs between the symbol and
    footprint
    -   Different CAD tools use different values to link schematic and
        layout.
-   Part + one symbol + one footprint, 1 to 1 map
    -   PART_NUM, BJT_123, SOT23_123

Symbols and footprint pin mapping is dictated by the CAD tool (pin names
or pin IDs are sometime used) and symbols and footprints must comply
with this.

However, within this library, linkage by a positive integer is generally
preferred. The reasons for this are

-   This transcends 2D design limits (column+row format)
-   This also applies to virtual / logical pins
-   This is compact to store

The conventions for this are:

-   Pin numbering provided by manufacturer should generally be preferred
-   Alphanumeric pin IDs (such as for BGAs) should be converted by
    sorting alphanumerically and ascending
-   Pins missing a number on manufacturer datasheets (E.g. power pads)
    should be assigned am unused number

**Selected strategy:**

For parts with 3 pins or less (transistors, potentiometers, etc.):

-   generic symbols are available (pin remapping is done at the symbol
    level).
-   2 pins gives 2 unique symbols
-   3 pins gives 6 unique symbols and one unique footprint

123 mapping conventions:

-   BJT CBE E.g. C→ 1 B→ 2 E→ 3
-   MOSFET DGS
-   Potentiometer top wiper bottom
-   TVS diodes vcc signal gnd

For parts with more than 3 pins:

-   It is considered a coincidence that the pinout is identical between
    two given parts. This even applies to fairly standard parts such as
    quad opamps, comparators, etc. since the pinouts usually still vary.
-   If a high (\>3) pin count part is found to have an identical pinout
    to an existing symbol and/or footprint, this CAD data can be
    directly reused without renaming any files and only changing
    properties as needed. This linkage should be indicated in the
    database.

A "drop in" replacement occurs when:

Manufacturer: May vary\
Manufacturer PN: May vary\
Symbol (includes pin numbering / connectivity): No change\
Footprint: No change\
Part specifications: May vary but typically must be close

A "near drop in" replacement occurs when:

Manufacturer: May vary\
Manufacturer PN: May vary\
Symbol (includes pin numbering / connectivity): No change\
Footprint: May vary\
Part specifications: May vary but typically must be close

## **CAD Data Reuse**

-   Note that, due to JEDEC, IEC, ANSI, ISO and other mechanical
    standards, footprint pin numbering is unlikely to change and
    footprint reuse is much more likely than symbol reuse.
    -   It should not be assumed that manufacturers are standards
        compliant: pin numbering on footprints should always be verified
        before using a footprint
-   A symbol which is a superset of another symbol is considered a
    completely different symbol
    -   This is clearer in the schematic and prevents design errors
    -   This is to target DRC cleanliness
    -   E.g. DFN and TSSOP parts have the same pin numbering but the DFN
        has an additional PAD connection
-   A symbol with multiple sub sections (units, heterogenous parts) is
    considered a single symbol
    -   This is partly driven by CAD tool limitations: many CAD tools
        (Altium, KiCAD) actually have the symbols grouped within the
        database.
    -   While some CAD tools (Siemens) have piece-meal symbols that
        could be reused, the symbols must still be linked together with
        properties or other data entry and it is considered best if this
        is included in the symbol.
-   Separate footprints are allowed to accommodate different assembly
    methods (wave, reflow, bonding, etc.)
-   Separate footprints for different design densities are allowed.
    -   If possible, it is recommended to not make a new footprint and
        modify footprints on a per instance basis to meet density needs.
        E.g. Silk screen can be removed.
    -   Separate footprints (schematic based footprint modification) are
        recommended when the CAD tool does not allow modifying footprint
        instances or when parts are very frequently used (passives) and
        manual modifications would be tedious.

## Schematic Symbol Drafting

-   Nominally hard metric except for pin and schematic routing grid
-   Primary scale: 2.5mm = ½ of preferred, print ready, scale
    -   Note that all dimensions are scaled from what are considered
        comfortable in terms of reading on a paper print, hand drawing,
        and hand writing Text without any assistive technologies
        (magnifying glass, digital zoom, etc.).
    -   Text heights for reference:
        -   5mm \~=16pt
        -   4mm \~10pt
        -   3mm \~= 8pt
        -   2.54mm \~=6.7pt
        -   12pt and 10pt are standard publishing font sizes.
    -   Preferred technical drafting paper would be 5mmx5mm course grid
        with a 1mm fine grid (mm paper, 2x the primary scale). This is
        at small handwriting scale (4mm \~=10pt), hand drawing scale
        (\~1mm tolerance), this is a standard grid paper size, and a
        decade increment.
    -   Note that, when drawing by hand, lines have the width of the pen
        or pencil tip. This is assumed to be 1mm (unscaled) and sets a
        minimum spacing on lines and geometry for them to be legible:
        roughly 1mm edge to edge = 2mm center to center = 1mm scaled
        center to center
        -   In contrast, vector graphics on computers can scale and
            rerender lines automatically and allow them to have
            practically a 0 unit width.
        -   This requires a clear distinction between edge to edge and
            center to center dimensions.

+---------------+---------------+--------------+----------------------+
| Grid Name     | Grid          | Use for      | Note                 |
| (relative to  | Dimensions    |              |                      |
| drafting or   |               |              |                      |
| component     |               |              |                      |
| origin)       |               |              |                      |
+---------------+---------------+--------------+----------------------+
| primary       | 2.54mm x      | -            | By observation, a    |
| imperial pin  | 2.54mm        |   components | 0.1" grid is the     |
| grid          |               |     (origin) | de-facto standard    |
|               | 0.100" x      |              | for manufacturer     |
|               | 0.100"        | -   pins     | provided data, data  |
|               |               |              | generated by Ultra   |
|               |               | -   nets     | Librarian, and the   |
|               |               |              | KiCAD libraries.     |
|               |               | -   busses   | This library is made |
|               |               |              | to be compatible.    |
|               |               |              |                      |
|               |               |              | For PADS with metric |
|               |               |              | units, grid must be  |
|               |               |              | entered manually.    |
|               |               |              |                      |
|               |               |              | For a fast library   |
|               |               |              | conversion to a hard |
|               |               |              | metric grid, the     |
|               |               |              | pins lengths can be  |
|               |               |              | resnapped and length |
|               |               |              | rounded to the       |
|               |               |              | nearest 1mm.         |
+---------------+---------------+--------------+----------------------+
| course metric | 2.5mm x 2.5mm | -   boxes    |                      |
| snap grid     |               |              |                      |
|               | \[0.098" x    | -   large    |                      |
|               | 0.098"\]      |     polygons |                      |
|               |               |              |                      |
|               |               | -   text     |                      |
+---------------+---------------+--------------+----------------------+
| text snap     | 1.00mm x      | -   text     | Convenient since     |
| grid          | 1.00mm        |              | font rules are       |
|               |               | -            | specified in mm      |
|               | \[0.039" x    |   properties | increment font       |
|               | 0.039"\]      |              | heights.             |
+---------------+---------------+--------------+----------------------+
| Imperial fine | 0.508mm x     | -   pin end  | Must not be smaller  |
| drawing snap  | 0.508mm       |     point    | than the fine        |
| grid          |               |              | drawing snap grid to |
|               | \[0.020" x    | -   boxes    | ensure readability   |
|               | 0.020"\]      |              | of pin lines.        |
|               |               | -   large    |                      |
|               |               |     polygons |                      |
|               |               |              |                      |
|               |               | -   shapes   |                      |
|               |               |     which    |                      |
|               |               |              |                      |
|               |               |    intersect |                      |
|               |               |     with     |                      |
|               |               |     pins     |                      |
|               |               |              |                      |
|               |               | -   Pin name |                      |
|               |               |     labels   |                      |
|               |               |              |                      |
|               |               | -   Pin      |                      |
|               |               |     number   |                      |
|               |               |     labels   |                      |
+---------------+---------------+--------------+----------------------+
| fine drawing  | 0.5mm x 0.5mm | -   lines    | Smaller grids are    |
| snap grid     |               |              | not allowed --       |
|               | \[0.017" x    | -   polygons | smaller features are |
|               | 0.017"\]      |              | not easily visible.  |
|               |               | -   arcs     |                      |
|               |               |              |                      |
|               |               | -   circles  |                      |
|               |               |              |                      |
|               |               | -   text     |                      |
|               |               |              |                      |
|               |               | -   pin      |                      |
|               |               |     labels   |                      |
|               |               |              |                      |
|               |               | -   special  |                      |
|               |               |     symbols  |                      |
|               |               |              |                      |
|               |               | -   arrows   |                      |
+---------------+---------------+--------------+----------------------+
| intersection  | 0.1mm x 0.1mm | -   arcs     | This is primarily    |
| snap grid     |               |              | needed for           |
|               | \[0.004" x    | -            | aesthetics. Without  |
|               | 0.004"\]      |    line-line | this fine resolution |
|               |               |     i        | grid, gaps between   |
|               |               | ntersections | lines become         |
|               |               |              | visible.             |
+---------------+---------------+--------------+----------------------+
| imperial      | 0.127mm x     | -   pin line |                      |
| intersection  | 0.127mm       |     to       |                      |
| snap grid     |               |     geometry |                      |
|               | \[0.005" x    |     line     |                      |
|               | 0.005"\]      |     i        |                      |
|               |               | ntersections |                      |
+---------------+---------------+--------------+----------------------+

-   Origin should generally be at the lower left of the symbol
-   Imperial metric conversion
    -   Pins are sized on on the fine imperial grid and intersecting
        metric geometry is resnapped.
        -   In some cases, this results in the entire symbol being on an
            imperial grid.
        -   This is much faster to draw than native metric length pins.
    -   Originally metric graphics (text, special symbols) unrelated to
        pins are kept on the metric grids.
-   Text
    -   Pin and net labels and numbers: 2mm \[0.079"\] tall
        -   Goal is to nearly fill all available space between pins and
            nets.
    -   Symbol adjacent text: 2mm \[0.079"\] tall
        -   All uniform
        -   Should generally be at lower left of symbol. Exceptions
            apply to small parts.
    -   General writing text: 2mm \[0.079"\] tall
        -   For printing, text should not be smaller than 4mm in height
            but this value matches the primary scale and users are
            expected to scale as needed for printing.
-   Pin length
    -   Minimum, no pin number label label: 0.5mm \[0.020"\]
    -   Minimum, with pin number label: 2.5mm \[0.098"\]
        -   Fits 3 small handwritten digits giving a highest pin number
            of 999. Prefer longer default if possible for cleanliness.
    -   Typical: 5mm \[0.197"\], 5.08mm \[0.200"\]
    -   Length integer multiples of 2.5mm or 2.54mm
-   Lines
    -   Minimum length: 1mm
    -   Typical width for vector graphics: 1px / vector
    -   Typical width for raster graphics or vector graphics with line
        weight: 0.5mm
    -   Minimum parallel line spacing, center to center: 1mm = 1 fine
        grid point between lines
-   Pin labels
    -   Pin number labels are not mandatory but are recommended for ease
        of use and clarity. E.g. large ICs, multi-component devices,
        etc.
    -   Pin name labels are not mandatory if the connectivity is clear.
-   Triangles
    -   Perfectly equilateral triangles are preferred but have a
        base/height ratio of 2/sqrt(3)=1.1547 so they do not fit well
        onto a grid
    -   Closest preferred base/height ratios are
        -   4/3 = 1.333
        -   6/5 = 1.200
        -   8/7 = 1.142
    -   1/1 triangles are not recommended
-   Circle and arcs
    -   smallest radius, arc, filled circle, or hollow circle: 0.5mm
        \[0.020"\]
    -   digital bubbles: 0.5mm \[0.020"\] radius
    -   testpoints: 0.5mm \[0.020"\] radius
-   Symbols should be as small as possible while maintaining clarity,
    readability, and general good appearance.
    -   Usually, the size is not limited by the geometry but by the
        adjacent text (Ref. Des.) Almost all symbols have at least 2
        lines of text and thus have a minimum height of 2\*2mm=4mm = 2
        grid spaces.
    -   If drawing by hand, a similar approach would be used to not
        waste paper area or drawing time.
    -   Uniformity in scale across symbol types is not mandatory (e.g.
        same size triangle for all amplifiers regardless of feature set,
        e.g. all 2 pin components are the same size). It is recommended
        to size symbols as small as possible while fitting all the
        required information (subsymbols, text, pin labels, etc.) and
        while respecting all the other drafting rules (e.g. minimum and
        default text sizes).
    -   Scaling subsymbols (pin label text, digital bubbles) with
        overall symbol size is not mandatory. Readability is typically
        maintained at the original scale.
-   Symbol variants are allowed to accommodate different display formats
    or preferences (e.g. pin number labels or no pin number labels) but
    one symbol must always be designated a default.
-   Symbol names should
    -   be human readable (no reverse order)
    -   not contain special symbols (URL safe, for compatibility with
        file systems and to be easy to type)
    -   be written from least to most specific
    -   not contain abbreviations

    1.  ## Layout Footprints
-   Nominally metric

    -   Imperial is often what is given by the manufacturers or required
        by a standard. Use the following rules to convert:

+----------------+-----------------+-----------------+-----------------+
| Conversion(s)  | Typical         | Metric grid     | Imperial        |
|                | Applications    | (rounding)      | equivalent      |
+----------------+-----------------+-----------------+-----------------+
| Strict         | Drill sizes     | 1um             | 39.37e-6 inches |
| tolerance      |                 |                 |                 |
|                | RF              |                 |                 |
|                |                 |                 |                 |
|                | Wafer scale     |                 |                 |
|                | dimensions      |                 |                 |
+----------------+-----------------+-----------------+-----------------+
| Standard       | Connectors      | 25um            | \~1mil=0.001    |
| imperial to    |                 |                 | inches          |
| metric         |                 |                 |                 |
+----------------+-----------------+-----------------+-----------------+
| Rounded        | General Purpose | 100um           | 3.937 mil       |
| imperial to    |                 |                 |                 |
| metric         |                 |                 |                 |
+----------------+-----------------+-----------------+-----------------+
| Large rounded  | Copper Fills    | 1mm             | 39.37mil        |
| imperial to    |                 |                 |                 |
| metric         | Mechanical      |                 |                 |
|                | Outlines        |                 |                 |
+----------------+-----------------+-----------------+-----------------+

-   The conversion strategy appropriate for the application should be
    used. Tight tolerances require smaller rounding errors. Note that
    the courser rounding is usually an integer multiple of the finer
    options.

-   For drill size matching between imperial and metric sizes, drills
    should always use strict (1um) conversion

-   Standard passive components footprint names should include whether
    they are imperial or metric to avoid confusion in duplicate names

```{=html}
<!-- -->
```
-   Silkscreen
    -   Polarity indicators included but may be covered after assembly
    -   All footprints should include a bounding box. The primary reason
        for this is to show which pads are grouped when a part is not
        installed. This also serves as a type of layout keepout.
-   Soldermask
    -   Dedicated shapes
-   Solder paste
    -   Dedicated shapes
-   Assembly layers
    -   Dedicated shapes
-   Drill layer
    -   Preferred mechanical drill size: 1.1mm
    -   Preferred microvia /laser drill size: 250um
-   Metal layers (external and internal, general rules for wide
    technology support)
    -   Min metal width, any geometry to any geometry, any net to any
        net, any plating thickness, any layer: 400um
    -   Min metal to metal spacing: same as min metal width

# Device Property Conventions

-   Multiplier Format
    - When the cad tool has native multiple instance support, use this instead
    -   multiplier (integer) = 1xmultiplier
    -   "" (empty) = 1
-   IS_INSTALLED flag
    - "DNI" = "DNP" = "NP" = "0" = "no" = "No" = "NO" = false
	- "" = "1" = "yes" = "Yes" = "YES" = true
	- Previously, this was merged with the muiltiplier property. 
	  This was found to lack clarity and sometimes even be confusing.
-   Unique Resistance, Capacitance, Inductance, ... properties
    -   Many tools typically prefer a single VALUE property that is
        displayed. This is also more convenient for BOM export. However,
        this lacks clarity since the exact property being referred to
        may need to be assumed (e.g. diode forward vs. reverse voltages)
		It is also possible to resolve a part to have undesirable 
		specifications due to the lack of specificity.
	- Using a "spec-string" of text to encode the specifications for 
	  a given part was considered but native CAD tool support is desired.
-   Siemens
    -   Convention for DEVICE = "Symbol Name" without any suffixed that
        are used to identify a part of a heterogenous symbol
        -   Formerly, DEVICE = "Symbol Name"\_PN. As of 2023-03-08, the
            MANUFACTURER_PART_NUMBER property was added to enable the
            use of different symbols for the same part within the same
            design. This property name is also more explicit, clearer,
            and CAD tool independent
        -   DEVICE must be unique since the tool uses this property for
            layout-schematic linkage
    -   MANUFACTURER_PART_NUMBER= "PART_NUMBER" before completion
    -   Property names target the Netlist PADS/DxDesigner flow. The PADS
        documentation indicates that the cases for the properties vary
        between the Netlist and Intgrated design flows. E.g. [Part
        Number
        (PART_NUMBER)](../../MentorGraphics/PADSVX.2.10/docs/htmldocs/attr/topics/General_PartNumberPartNumber_idee3e0fd4.html#idee3e0fd4-f115-4b2d-a24a-fb65ff02efa8__General_PartNumberPartNumber_idee3e0fd4.xml%23idee3e0fd4-f115-4b2d-a24a-fb65ff02efa8)
    -   HETERO property is fully completed if applicable. Symbol
        grouping is not explicitly stored in the database
    -   PKG_TYPE="PKG_TYPE" (unlinked -- determined at PCB layout start)
        -   PCB only parts do not have this property
    -   Only properties necessary for display in the symbol and basic
        packaging are added to the symbol
        -   This is faster to enter and allows direct addition of other
            parameters at the schematic level as preferred by designers,
            assuming that mapping to database fields are managed
            correctly
        -   This is typically, DEVICE, PKG_TYPE, PART_NUMBER, REFDES
        -   Note: For some reason, properties can only be moved if they
            don't contain the default value
            
# Verification Flows

-   PADS example project holds all newly developed symbols
    -   Visual review
    -   Tools→ PCB Interface... (Packaging)
    -   Tools → Diagnostics
        -   Shows if schematic library is out of date
    -   PADS Databook → New hierarchical Verification Window
        -   Shows if library items can't be found
-   Tested on the following CAD tools
    -   Altium 23
    -   PADS VX.2.10

# Debugging Tips

## Siemens

-   Symbols can "break" and exhibit strange behavior when instantiated.
    This may occur if the text of the symbols is directly edited.
    -   One observed symptom of this is that the tool may automatically
        (per an ambiguous / unknown rule set) change the case of
        characters in symbol names in schematics however, references to
        symbol filenames with different case characters still work
    -   Another observed symptom of this was the inability to delete or
        add specific properties, especially ones that are not present in
        the properties list.
    -   The solution to this is to copy and paste the symbol graphics to
        a new symbol -- PADS will generate a new file and therefore
        clean errors
-   All symbols and symbol instances in a HETERO part must have exactly
    the same properties, otherwise packaging fails
    -   The visibility of the property can vary between symbols
-   After Tools→ Update Libraries, pins may become corrupted and fail to
    package. To resolve this, the part must be full replaced: right
    click→ Replace Symbol→ Search for same symbol name→ Replace
-   PADS layout libraries are **not** compatible with DxDesigner
-   Tools → Property Definition Editor
    -   Anytime modifications are made, the project has to be closed and
        reopened for the changes to be visible
    -   This includes the symbol editor -- it must be closed and
        reopened along with the project
    -   Not all properties can be modified from this dialog
    -   The properties available depend on
        -   the selected design flow
        -   the object type (border, composite, etc.)
        -   the tool editing the properties (E.g. symbol editor vs.
            regular schematic editor)
    -   A workaround to get properties available anywhere is to manually
        add them to the properties file.
    -   An example of this is the \@DATETIME property commonly used for
        borders. While it is an official property for a netlist flow
        project, for an unknown reason, it was not available in the
        symbol editor until it was manually added as a user defined
        property.
        -   Note that is is unclear if a custom property was necessary
            or PROPERTY_NAME="@DATETIME" would also work
        -   \@DATETIME function worked correctly with \@DATETIME="" and
            \@DATETIME="@DATETIME". \@DATETIME="@DATETIME" is more
            practical for seeing and placing the property.
- PADS standard library location: "C:\MentorGraphics\PADSVX.2.10\SDD_HOME\Libraries\xDX_Designer\StarterLibrary\StarterLibrary.dbc"

## Altium

This Altium error was encountered: 

[Database error](images/Altium_error.png){width="9.58cm"
height="4.18cm"}

(Image from <https://altiumlibrary.com/GetStarted/Troubleshooting> )

Instructions here were necessary to install a database driver that
Altium recognizes:

<https://www.altium.com/documentation/altium-designer/using-database-libraries-with-32-64-bit-altium-design-software-same-computer>

<http://www.microsoft.com/en-us/download/details.aspx?displaylang=en&id=13255>

As administrator in cmd.exe:

```
AccessDatabaseEngine_X64.exe /passive
```

# TODO

-   Table generators
    -   database to Altium database with dblink file
    -   database to DxDatabook database
-   Cleanup functions
    -   CAD entry deduplicator with reference updates
-   Import functions
    -   Digikey BOM
    -   Mouser BOM
    -   General BOM
