# wxwidgets
Simple widgets for usage with the wxPython library. It includes a table, sizer and input elements for directory, files and text.

## Usage Example SimpleSizer

```python
from wx import Panel, VERTICAL

with SimpleSizer(parent, VERTICAL) as sizer:
    new_element = Panel(parent)
    sizer.Add(new_element)

```