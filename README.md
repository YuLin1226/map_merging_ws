# map_merging_ws

The rf2o pkg was supported in indigo version, and today I cannot sucessfully compile it.
But to finish mapping work, that pkg is not necessary.

## gmapping

```$ roslaunch cb_gazebo cb_omni.launch```
```$ roslaunch solabot_navigation solabot_gmapping.launch```
```$ rosrun map_server map_saver -f [map_name]```
