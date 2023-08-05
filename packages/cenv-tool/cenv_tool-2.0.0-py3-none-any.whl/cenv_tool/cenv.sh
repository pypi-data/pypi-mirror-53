source /opt/conda/etc/profile.d/conda.sh
export AUTOACTIVATE=1
export AUTOUPDATE=1
export meta_yaml_path=conda-build/meta.yaml
export meta_yaml_md5_path=conda-build/meta.md5
CYAN='\033[0;94m'
GREEN='\033[1;32m'
RED='\033[1;91m'
COLOR_END='\033[0m'
AS_BOLD='\033[1;37m'



function autoactivate_toggle(){
    if (( $AUTOACTIVATE == 1 )); then
        export AUTOACTIVATE=0
    else
        export AUTOACTIVATE=1
    fi
}


function autoupdate_toggle(){
    if (( $AUTOUPDATE == 1 )); then
        export AUTOUPDATE=0
    else
        export AUTOUPDATE=1
    fi
}


function get_envname_from_meta(){
    if [ -e $meta_yaml_path ]; then
        while IFS='' read -r line || [[ -n "$line" ]]; do
            if [[ $line == *"env_name"* ]]; then
                echo $( echo "$line" | cut -d' ' -f 6-)
            fi
        done < $meta_yaml_path;
    fi
}


function autoactivate_env() {
    if (( $AUTOUPDATE == 1 )); then
        if [ -e $PWD/$meta_yaml_md5_path ]; then
            local new_md5=$(echo "$(md5sum $PWD/$meta_yaml_path)" | cut -d' ' -f1)
            local current_md5="$(head -n 1 $PWD/$meta_yaml_md5_path)"
            if ! [ $new_md5 = $current_md5 ]; then
                conda deactivate
                cenv
            fi
        fi
    fi

    if (( $AUTOACTIVATE == 1 )); then
        if [ -e $PWD/$meta_yaml_path ]; then
            local env="$(get_envname_from_meta)"
            local env="${env%\"}"
            local env="${env#\"}"
            if [[ $PATH != *$env* ]]; then
                if conda activate $env 2>/dev/null && [[ $? -eq 0 ]]; then
                    CONDA_ENV_ROOT="$(pwd)"
                    PYTHONPATH=.:$PYTHONPATH
                    echo -e "${GREEN}"'\u2714'" activated${COLOR_END} $env"
                fi
            fi
        elif [[ $PATH = */envs/* ]] && [[ $(pwd) != $CONDA_ENV_ROOT ]] \
          && [[ $(pwd) != $CONDA_ENV_ROOT/* ]]; then
            CONDA_ENV_ROOT=""
            conda deactivate
            unset PYTHONPATH
            echo -e "${RED}"'\u2718'" deactivated${COLOR_END} env"
        fi
    fi
}
