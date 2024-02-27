# Arbovirus on a network

Brilliant work by Shakir! :)

## Installing Pre-requisites

### Curl
```
sudo apt install curl
```

### C++ package manager: vcpkg

```
git clone https://github.com/Microsoft/vcpkg.git
./vcpkg/bootstrap-vcpkg.sh
```

### JSON Reader
```
sudo apt install nlohmann-json*
```
	
### Package cxxopts


```
git clone https://github.com/jarro2783/cxxopts.git

sudo apt install rapidjson-dev	
cd cxxopts
mkdir build && cd build
cmake ..
make -j$(nproc)
sudo make install
```

## Main Installation

```bash
cd cpp-ArboSim
make
```

## Execution

```
cd pythonanalysis
python NetworkSeedingFileCreation.py
```

```
cd cpp-ArboSim
./drive_simulator --output_directory ../outputdir/1/ --NetworkName ScaleFree --NetworkFileHuman NetworkFileHumanScaleFree.json --Nodes 47 --NUM_DAYS 360000 --input_directory ../InputFiles/Senegal/
```