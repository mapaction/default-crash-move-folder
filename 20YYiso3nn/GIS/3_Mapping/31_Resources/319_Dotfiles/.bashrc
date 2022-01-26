mapaction_code_directory="~/Documents/code"

# alias for ArcGIS propy python script location
alias propy='/d/Program\ Files/ArcGIS/Pro/bin/Python/Scripts/propy.bat'
# alias for ArcGIS proenv python script location
alias proenv='/d/Program\ Files/ArcGIS/Pro/bin/Python/Scripts/proenv.bat'
# bash alias to move to mapaction code directory
alias mtma="cd $mapaction_code_directory"

# bash function to run mapElementLocationsPro script
function exportAprxTemplateData {
    mapElementLocationsPro="20YYiso3nn/GIS/3_Mapping/31_Resources/318_Python_scripts/mapElementLocationsPro.py"

    mtma
    cd default-crash-move-folder
    if [ "$1" == "development" ]; 
    then  
    	nodemon --exec propy $mapElementLocationsPro
    else 
 	    propy $mapElementLocationsPro
    fi
}