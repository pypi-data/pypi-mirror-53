# string-color   
   
string-color is just another python module for coloring strings in print statements.   
   
### Installation   
   
`$ pip install string-color`   
   
### Python Module Usage   
   
```python   
from stringcolor import *

# a few examples without background colors.
# for color names see CLI usage above.
print(cs("here we go", "orchid"))
print(cs("away to space!", "DeepPink3"))
print(cs("final fantasy", "#ffff87"))

# bold and underline also available.
print(cs("purple number 4, bold", "purple4").bold())
print(cs("blue, underlined", "blue").underline())
print(bold("bold AND underlined!").underline().cs("red", "gold"))

# yellow text with a red background.
# color names, hex values, and ansi numbers will work.
print(cs("warning!", "yellow", "#ff0000"))
```   
  
![Usage Screep Cap][screencap]

[screencap]: https://believe-it-or-not-im-walking-on-air.s3.amazonaws.com/sc-screen-cap.jpg "Usage Screen Cap"
  
### CLI Usage     
   
```
positional arguments:
  color          show info for a specific color:
                 $ string-color red 
                 $ string-color '#ffff87'
                 $ string-color *grey* # wildcards acceptable

optional arguments:
  -h, --help     show this help message and exit
  -x, --hex      show hex values
  -r, --rgb      show rgb values
  --hsl          show hsl values
  -a, --alpha    sort by name
  -v, --version  show program's version number and exit
```  
  
`$ string-color`   
   
display a list of all 256 colors   
   
`$ string-color yellow`   
   
show color info for the color yellow   
   
`$ string-color "#ff0000"`   
   
show color info for the hex value #ff0000   
   
`$ string-color *grey*`  
  
show all colors with "grey" in the name. also works with "grey\*" and "\*grey"  
  
![CLI Screep Cap][cliscreencap]  
  
[cliscreencap]: https://believe-it-or-not-im-walking-on-air.s3.amazonaws.com/sc-screen-cap2.jpg  "CLI Screen Cap"  
  

