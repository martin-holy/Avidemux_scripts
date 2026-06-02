# Avidemux scripts
ExportSegments.py - Script for exporting segments using copy codec if possible

SplitSegment.py - Script to split video at current time

## Install
- Copy *.py files to ```c:\Users\user_name\AppData\Roaming\avidemux\custom\``` or ```...\settings\custom\``` (portable version).

- Or make symbolic link if you want to keep files elsewhere and make changes to them.

```mklink "c:\Programs\avidemux64\settings\custom\ExportSegments.py" "d:\Dev\Python\Avidemux_scripts\ExportSegments.py"```

```mklink "c:\Programs\avidemux64\settings\custom\SplitSegment.py" "d:\Dev\Python\Avidemux_scripts\SplitSegment.py"```

- Don't forget to create output directory used in ```ExportSegments.py```
- Copy your decode profile to ```"pluginSettings\x264\1"``` and ```"pluginSettings\x264\3"``` and set it in ```ExportSegments.py```.