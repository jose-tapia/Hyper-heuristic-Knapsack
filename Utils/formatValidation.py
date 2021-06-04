from Utils.IO import loadInstance, obtainFilenames, tapia_path


def validateFormat(path):
    # Verify the correctness of the format for each instance
    n, W, weights, profits = loadInstance(path)
    if n < 0:
        print('Error: Size negative')
        return False
    if W < 0:
        print('Error: Capacity negative')
        return False
    if len(weights) != n or len(profits) != n:
        print('Error: Size does not match')
        return False 
    for w, p in zip(weights, profits):
        if w < 0 or p < 0:
            print('Error: Negative weight or profit')
            return False 
        if w > W:
            print('Error: Weight out of limit.')
            return False 
    return True

if __name__ == '__main__':
    datasets = ['OrtizBayliss_Train', 'OrtizBayliss_Test', 'Pisinger']
    for dataset in datasets:
        filenames = obtainFilenames(tapia_path, dataset)
        if all(map(validateFormat, filenames)) is False:
            print(f'ERROR: A file in {dataset} does not have the correct format.\n')
                            