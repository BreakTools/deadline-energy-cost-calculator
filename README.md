# Deadline energy cost calculator

This simple Deadline event plugin calculates the total costs of a render and adds it to one of the job extra info keys. Costs are calculated based on a configurable average render hour price.
<p align="center">
  <img src="https://github.com/BreakTools/deadline-energy-cost-calculator/assets/63094424/f31d05b8-d0d7-4d35-a370-081c20ba9345" />
</p>

## Event config

<p align="center">
  <img src="https://github.com/BreakTools/deadline-energy-cost-calculator/assets/63094424/5b155d01-02dd-43b4-a29d-4276fdf9af92" />
</p>

## Installation instructions

1. Download this repository
2. Move the `EnergyCostCalculator` folder to your Deadline installation custom events folder, which you can find at `{deadline_install_root}/custom/events/`.
3. You will have to change the name of one of your Job Extra Info fields. You can configure this in the Deadline Monitor by going to `Tools > Configure Repository Options > Job Settings > Job Extra Properties`.
   ![deadlinemonitor_SasRsjRg86](https://github.com/BreakTools/deadline-energy-cost-calculator/assets/63094424/160a8e40-fb1c-4124-b32c-8ef85e2f6da1)
4. You can now configure the plugin by going to `Tools > Configure Events > EnergyCostCalculator`. Be sure to set the extra info field number to the field whose name you changed in the previous step. An example calculation for the render hour price: With a computer wattage average of 750 watts while rendering and an energy price of 0.35 EUR per kWh, the render hour price would be `750 / 1000 * 0.35 = 0.2625`.

The event plugin should now work! I've also provided a simple script for setting the costs on already existing jobs.

While not enterily accurate, seeing the price skyrocketing on some unoptimized renders should certainly motivate artists to maybe spend a little more effort on optimization before they toss their render onto the farm :)
