# Dependencies



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

# MariaDB Setup

```
sudo mysql_install_db --datadir ./
sudo mysqld -u root --datadir=./ --verbose --log_error=./errors.log
sudo mariadb
create user admin;
mariadb -u admin
```

# Planned Work / TODO

- BOM exporter
  - implement merging of components with notes
  - implement new "construction" property applicable to resistors (wirewound, thin film, thick film, etc.)
  - Dual pretty and field names in column titles for quick editing
  - Change to new multiplier strategy (BOM, schematic and/or layout)
  - (s) on Ref designators
