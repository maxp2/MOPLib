--//Copied from documentation for convenience 
select max(max(parts.UUID), max(CAD_data.UUID))+1 from parts, CAD_data;