from ssd_check import check_func
from final_paths import gen_paths
from manager import manager_func

import constants
import json

#change this negation of if statement while dealing with actual ssd
if not check_func():
    with open(constants.TEST_CONFIG_PATH) as f:
        config = json.load(f)

    main_paths = config.get("watched_dir")

    if not isinstance(main_paths, list):
        raise ValueError("watched_dir must be a list of paths")

    final_paths = gen_paths(main_path=main_paths)
    
    for path in final_paths:
        manager_func(path)

else:
    print("SSD Disconnected")
