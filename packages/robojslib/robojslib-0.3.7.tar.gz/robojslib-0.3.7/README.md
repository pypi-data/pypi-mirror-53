# roboJSlib
## How to use

###### Install with PIP:
Install pip and run:
```
pip install robojslib
```

###### Manual installation:
download roboJSlib.py and place it on your Python scripts folder or inside your tests.robot folder.
Once done, import in robotframework by running
```
Library       robotJSlib.py
```

###### Dependencies:
Before running, be sure to have installed the dependencies:
````
pip install robotframework-seleniumlibrary
````
````
pip install robotframework
````
for BuiltIn lib

| Keyword                       |  arguments             | Info                                       |   |   |
|   ---                         |---                     |---                                         |---|---|
| Check title                   |  None                  | Checks driver title to not include "http"  |   |   |
| Vanilla click           |  Element ID            | Uses vanillaJS to trigger a click overan element  |   |   |
|Vanilla click by query selector| Selector | Uses vanillaJS to trigger a click overan element
| Modify url string|  "arg1, arg2": Url portion to be changed, url portion to be injected | checks if a url sub-string is available and substitute it with second argument  
| Vanilla input  | "arg1, arg2" Element ID, value | Vanilla input on a given element with the given text
| Vanilla input by query selector | "arg1, arg2" selector, value | Vanilla input on a given element with the given text
|Checkbox control|Element ID| If checkbox is selected it skips, else it clicks it
|Insert phone nr|Element ID| generates a phone nr (es: 351xxxxxxx) & inputs the value inside the element
|Set responsive|Mobile, Tablet| sets resolution for responsive testing: Mobile or Tablet
| Wait until title contains| arg, string be contained | Checks title contains a given string
| Open new tab | arg: "url to be opened" | Note: include "http" or "https" in the url to avoid any bug/problem
|Check if visible and click | arg: id| Checks if an element is displayed and clicks it. Otherwise, it skips.
|Check if visible and click by class|arg: class| Checks if an element by class is displayed and clicks it. Otherwise, it skips.
|Check if visible and click by css selector|arg: css selector| Checks if an element by css selector is displayed and clicks it. Otherwise, it skips.
