# WarsAPI
Name Temporary
## [api.um.warszawa.pl](https://api.um.warszawa.pl)
This project is possible thanks to the Capital City of Warsaw's public data API project.

To be able to use 100% of app's functions, include your personal API key in ***.env*** file.  
To gain access to your API key, you must navigate to the [API website](api.um.warszawa.pl), to `Logowanie` bookmark in the topbar.

## Goal for the project
The goal for this project is for me to gain understanding of working with 3rd party API public systems, and possibly create a basis for future, more proffesional project with this data.

## Launching and operating

All dependencies in this project are managed via [UV package manager](https://docs.astral.sh/uv/).
For setup, run `uv sync`.

There are 4 available currently modes of running the app
- buses - displays current position of all buses
- trams - displays current position of all trams
- stops - displays current position of all stops for both modes of transport
- ~~streets - displays points defining the paths for streets (currently only 1000 streets are available)~~ currently **WIP**


To run selected mode, run command:
```
uv run app.py -m <mode>
``` 