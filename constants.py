masks = {
        0: [[1]*4]*4,  # FULL_BLOCK
        1: [[1,1,1,1],[1,0,0,1],[1,0,0,1],[1,1,1,1]],  # OUTER_BOUNDARY
        2: [[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,1,1,1]],  # EL_SHAPE_BL
    }

type_names = ['FULL_BLOCK', 'OUTER_BOUNDARY', 'EL_SHAPE']
categories = {0: 'FULL_BLOCK', 1: 'OUTER_BOUNDARY', 2: 'EL_SHAPE'}