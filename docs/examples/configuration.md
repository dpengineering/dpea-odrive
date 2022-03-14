---
layout: default
title: Saving Configuration
parent: Examples
nav_order: 6
---

# Saving Configuration (Backing Up, Restoring, and Erasing)
{: .no_toc }

1. TOC
{:toc}
---
## Save the Configuration
If you have an ODrive configuration that you are satisfied with (GPIO settings, velocity/current limits, etc.),
then you can save your settings onto the ODrive board itself. This makes it so that when you reboot the ODrive, your
settings/configuration persist in memory. 

For the most part, you will not have to write any scripts that deal with saving the configuration directly, so you can
simply use `odrivetool` to work with your configuration.

In `odrivetool`, save your configuration by running
```
odrvX.save_configuration()
```
Now, anytime you turn off your ODrive it will turn back on with the configuration you have saved.

## Backup the Configuration
If you have a configuration that you want to save to a file (for example to keep on GitHub or share with others), you
can use the **backup** feature of `odrivetool`. To save the configuration to a file, open your terminal and run
```
odrivetool backup-config <my_config_filename>.json
```

Replace `<my_config_filename>` with your desired filename. Make sure to keep the `.json` extension. Feel free to open
the file that stores your configuration. What do you notice? [Here](https://www.w3schools.com/js/js_json_intro.asp) is a 
brief intro to JSON files to help make sense of all the text you see in the config backup file. 

## Restore the Configuration
A configuration backup would be pretty useless if we have no way to load a configuration file onto the ODrive. To do 
so, open your terminal and run

```
odrivetool restore-config <my_config_filename>.json
```

Make sure to designate the full filepath to your JSON file (e.g. /home/soft-dev/Documents/my_config.json). At this
point, your configuration backup will be restored and saved to the ODrive.

## Erasing the Configuration
If you are starting development on a new ODrive, chances are that it has a configuration that is not compatible
with your motor setup. To start from scratch, open `odrivetool` and erase the existing configuration with

```
odrvX.erase_configuration()
```
Since you are now starting at the default settings, the ODrive will not be recognizing your brake resistor. Ensure
that 

```
odrvX.config.enable_brake_resistor == True
```

Lastly, erasing the configuration does not save the default settings to the ODrive. To keep the default settings after 
rebooting, save your configuration.
```
odrvX.save_configuration()
```
Now you can start developing your ODrive application starting from the default configuration.