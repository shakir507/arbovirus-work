
cd pythonanalysis
python3 NetworkSeedingFileCreation.py
cd ../cpp-ArboSim

./drive_simulator --output_directory ../OutputFiles/Senegal/ --NetworkName ScaleFree --NetworkFileHuman NetworkFileHumanScaleFree.json --Nodes 47 --NUM_DAYS 30000 --input_directory ../InputFiles/Senegal/